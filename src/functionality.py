from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy import signal
from helpers import convolve

class Editor():
    def __init__(self):
        self.pixels = None
        self.brightnes = 50

    def load(self, address):
        img = Image.open(address)
        self.pixels = np.array(img)
        
    def show(self):
        plt.imshow(self.pixels)
        plt.axis('off')  # hide axes
        plt.show()

    def color_boost(self, amount, channel):
        """
        channel: 0-R, 1-G, 2-B
        """
        arr = self.pixels.astype(float)

        factor = (amount - 50) / 50 if amount > 50 else (50 - amount) / 50
        if amount > 50:
            arr[:, :, channel] += (255 - arr[:, :, channel]) * factor
        else:
            arr[:, :, channel] -= arr[:, :, channel] * factor

        self.pixels = np.clip(arr, 0, 255).astype(np.uint8)

    def black_and_white(self):
        gray = self.pixels[:, :, :3].mean(axis=2)  # average R,G,B per pixel
        mask = gray < 128                          # boolean mask
        self.pixels[:, :, :3] = np.where(mask[:, :, None], 0, 255)
 
    def edge_enhancer(self):    
        kernel = [
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ]
        self.pixels = convolve(self.pixels, kernel)

    def sharpen(self):
        kernel = [
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ]
        self.pixels = convolve(self.pixels, kernel)

    def box_blur(self, size):
        kernel = np.ones((size, size), dtype=float) / size**2
        self.pixels = convolve(self.pixels, kernel)
    
    def saturation(self, amount):
        """
        amount == a scale from 0-100, amounting to the intensity of the filter, default = 50
        not linear
        """
        
        arr = cv2.cvtColor(self.pixels, cv2.COLOR_RGB2HSV)
        arr = arr.astype(np.float32)

        factor = (amount - 50) / 50 if amount > 50 else (50 - amount) / 50
        if amount > 50:
            arr[:, :, 1] += (255 - arr[:, :, 1]) * factor
        else:
            arr[:, :, 1] -= arr[:, :, 1] * factor

        arr = cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_HSV2RGB)  # convert back from HSV

        self.pixels = np.clip(arr, 0, 255).astype(np.uint8)

    def brightness(self, amount):
        """
        amount == a scale from 0-100, amounting to the intensity of the filter, default = 50
        the brightening is not linear, it changes based of off the "brightness" of inidividual pixels
        """

        arr = self.pixels.astype(float)

        factor = (amount - 50) / 50 if amount > 50 else (50 - amount) / 50
        if amount > 50:
            arr[:, :, :3] += (255 - arr[:, :, :3]) * factor
        else:
            arr[:, :, :3] -= arr[:, :, :3] * factor

        self.pixels = np.clip(arr, 0, 255).astype(np.uint8)

