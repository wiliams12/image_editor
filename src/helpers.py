import numpy as np

import cv2

def convolve(image, kernel):
    return cv2.filter2D(image, -1, np.array(kernel, dtype=np.float32))

