#!/bin/bash
cd leo
playPattern -x 1280 -y 720 -n 200
ffmpeg -framerate 1 -i leo/leopard_1280_720_32B_%03d.png ../leos.mp4
