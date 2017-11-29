#include <stdlib.h>
#include <stdio.h>
#include <omp.h>
#include <string.h>
#include <math.h>
#include <time.h>

#include "args.h"
#include "helpers.c"

#define PRECISION 10

static inline float subpixel_value(float u, float v, float a, float b, float c, float d) {
    return (1 - v) * ((1 - u) * a + u * b) + v * ((1 - u) * c + u * d);
}

float unwrap(float ref, float val) {
    float diff = INFINITY;
    float new_diff;
    // FIXME : modulo 2PI seulement
    for(int i = -2; i <= 2; i++) {
        new_diff = fabs(ref - (val + i * PI));
        
        if(new_diff > diff) {
            return val + (i - 1) * PI;
        }

        diff = new_diff;
    }
    
    return val + 2 * PI;
}

int main(char argc, char** argv) {

    int nthreads = 4, i, j, from_w, from_h, to_w, to_h, foo, nb_shifts, nb_patterns;
    char* ref_format = "leo_%d_%d_%03d_%02d.pgm";
    char* cam_format = "%03d.pgm";

    FILE* info = fopen("sines.txt", "r");

    // Check file size to avoid problems if sines.txt is empty
    fseek(info, 0, SEEK_END);
    if(!ftell(info)) {
        printf("error: empty sines.txt\n");
        exit(-1);
    }
    fseek(info, 0, SEEK_SET);

    // Args parsing
    for(i=1; i < argc - 1; i++) {
        if(strcmp(argv[i], "-t") == 0) {
            nthreads = atoi(argv[i + 1]); i++;
        } else {
        usage:
            printf("usage: %s [-t nb_threads=%d] filename\n",
                   argv[0], nthreads);
            exit(1);
        }
    }
    if(i != argc - 1) goto usage;

    omp_set_num_threads(nthreads);
    
    srand(time(NULL));
    
    fscanf(info, "%d %d %d %d %d", &to_w, &to_h, &foo, &nb_patterns, &nb_shifts);
    fclose(info);
    
    char* ref_phase_format = "phase_ref_%d_%d_%03d.pgm";
    char* cam_phase_format = "phase_cam_%d_%d_%03d.pgm";
    
    float*** matches = load_ppm(argv[argc - 1], &from_w, &from_h);
    
    #pragma omp parallel for private(i, j)
    for(i=0; i<from_h; i++)
        for(j=0; j<from_w; j++) {
            
            if(matches[X][i][j] == 65535.0) {
                matches[X][i][j] = matches[Y][i][j] = matches[DIST][i][j] = -1.0;
            } else {
                matches[X][i][j] = round(matches[X][i][j] / 65535.0 * to_w);
                matches[Y][i][j] = round(matches[Y][i][j] / 65535.0 * to_h);
                matches[DIST][i][j] = matches[DIST][i][j] / 65535.0 * (nb_patterns * PI / 2.0);
            }
        }
    
    float*** subpixel = malloc_f32cube(3, from_w, from_h);

    float*** cam_codes = load_codes(cam_phase_format, cam_format, 1, nb_patterns, nb_shifts, from_w, from_h);
    float*** ref_codes = load_codes(ref_phase_format, ref_format, 0, nb_patterns, nb_shifts, to_w, to_h);
    
    float** colormap = malloc_f32matrix(from_w, from_h);

    // Up-left, Up-right, Down-left, down-right
    int pos_x[] = {-1, +1, -1, +1};
    int pos_y[] = {-1, -1, +1, +1};
    
    for(int n=0; n<1; n++) {
        j = rand() % (from_w - 2) + 1;
        i = rand() % (from_h - 2) + 1;

        int x = matches[X][i][j];
        int y = matches[Y][i][j];

        fprintf(stderr, "%d %d => %d %d\n", j, i, x, y);

        float* match = malloc(sizeof(float) * nb_patterns);

        for(int k=0; k<nb_patterns; k++) {
            match[k] = cam_codes[k][i][j];
        }

        float** costs = malloc_f32matrix(PRECISION * 2, PRECISION * 2);

        for(int q=0; q<4; q++) {
            
            int decalage_x = (q % 2) * PRECISION;
            int decalage_y = (q >= 2) * PRECISION;
            
            for(int k=0; k<nb_patterns; k++) {
            
                float m = match[k],
                    a = unwrap(m, ref_codes[k][y][x]),
                    b = unwrap(m, ref_codes[k][y][x + pos_x[q]]),
                    c = unwrap(m, ref_codes[k][y + pos_y[q]][x]),
                    d = unwrap(m, ref_codes[k][y + pos_y[q]][x + pos_x[q]]);
            
                /* if((m > a && m > b && m > c && m > d) || */
                /*    (m < a && m < b && m < c && m < d)) { */
                /*     /\* Si la phase matchée n'est pas dans les bornes du pixel */
                /*        considéré, on augmente arbitrairement le coût */
                /*        (influance le choix du meilleur quadrant). *\/ */
                /*     for(int u=0; u<PRECISION; u++) */
                /*         for(int v=0; v<PRECISION; v++) */
                /*             costs[decalage_y + u][decalage_x + v] = 1.0; */

                /*     continue; */
                /* } */
                    
                for(int u=0; u<PRECISION; u++) {
                    for(int v=0; v<PRECISION; v++) {
                        float vall = fabsl(m - subpixel_value(u / (float)PRECISION, v / (float)PRECISION,
                                                              a,b,c,d));
                        
                        costs[decalage_x + u][decalage_y + v] += vall;
                    }
                }
            }
        }
        
        for(int u=0; u<PRECISION * 2; u++) {
            for(int v=0; v<PRECISION * 2; v++) {
                printf("%.5f ", costs[u][v]);
            }
                
            putchar('\n');
        }
    }
    
    return EXIT_SUCCESS;
}
