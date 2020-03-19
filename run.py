import os
import cv2
import argparse
import numpy as np


os.makedirs('output', exist_ok=True)


TAB10 = [
    (180, 119, 31), (14, 127, 255), (44, 160, 44),
    (40, 39, 214), (189, 103, 148), (75, 86, 140),
    (194, 119, 227), (34, 189, 188), (207, 190, 23)
]


def first_image_callback(event, x, y, flags, param):
    global kp1
    if event == cv2.EVENT_LBUTTONDOWN:
        if hasattr(first_image_callback, 'i'):
            first_image_callback.i = (first_image_callback.i % 8) + 1
        else:
            first_image_callback.i = 0
        kp1.append((x, y))

        cv2.circle(first_image, (x, y), 7, TAB10[first_image_callback.i], -1)
        cv2.imshow('first_image', first_image)


def second_image_callback(event, x, y, flags, param):
    global kp2
    if event == cv2.EVENT_LBUTTONDOWN:
        if hasattr(second_image_callback, 'i'):
            second_image_callback.i = (second_image_callback.i % 8) + 1
        else:
            second_image_callback.i = 0
        kp2.append((x, y))

        cv2.circle(second_image, (x, y), 7, TAB10[second_image_callback.i], -1)
        cv2.imshow('second_image', second_image)


parser = argparse.ArgumentParser()
parser.add_argument('first_image')
parser.add_argument('second_image')
args = parser.parse_args()

first_image = cv2.imread(args.first_image)
output = first_image.copy()
second_image = cv2.imread(args.second_image)

kp1 = []
kp2 = []

cv2.namedWindow('first_image')
cv2.setMouseCallback('first_image', first_image_callback)
cv2.imshow('first_image', first_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.namedWindow('second_image')
cv2.setMouseCallback('second_image', second_image_callback)
cv2.imshow('second_image', second_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

if len(kp1) > len(kp2):
    kp1 = kp1[:len(kp2)]
else:
    kp2 = kp2[:len(kp1)]

kp1 = np.array(kp1)
kp2 = np.array(kp2)

h, status = cv2.findHomography(kp1, kp2)
first_image_warped = cv2.warpPerspective(output, h, second_image.shape[:2][::-1])

cv2.imwrite(os.path.join('output', 'output.png'), first_image_warped)
np.save(os.path.join('output', 'h.npy'), h)
