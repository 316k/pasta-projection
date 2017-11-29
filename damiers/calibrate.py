#!/usr/bin/python

from __future__ import print_function

import numpy as np
import cv2
import glob

W, H = 9, 6

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((H*W,3), np.float32)
objp[:,:2] = np.mgrid[0:W,0:H].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('test1/checkerboard*.png')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (W,H), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)

        # Draw and display the corners

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        cv2.drawChessboardCorners(img, (W,H), corners ,ret)

        # Pour visu
        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        cv2.imwrite('/cv-'.join(fname.split('/')), img)
    else:
        print("No match for :", fname)

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

def print_arr(arr):
    for line in arr:
        print('\t'.join(map(str, line)))
    print()

print("Matrix")
print_arr(mtx)

print("Rotations")
for r in rvecs:
    print_arr(cv2.Rodrigues(r)[0])

print("Translations")
for t in tvecs:
    print_arr(t)

cv2.destroyAllWindows()

mean_error = 0
for i in xrange(len(objpoints)):
    imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
    mean_error += error

print("total error: ", mean_error/len(objpoints))
