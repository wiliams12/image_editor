from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy import signal
from helpers import convolve
import copy

class Editor():
    def __init__(self):
        self.current = None
        self.state = []

    def load(self, address):
        img = Image.open(address)
        self.state.append(np.array(img))
        self.current = 0
        
    def show(self):
        pil_image = Image.fromarray(self.state[self.current])
        return pil_image

    def new_edit(self):
        max_index = len(self.state) - 1
        if self.current != (max_index):
            for i in range(max_index - self.current):
                self.state.pop()

        self.state.append(copy.deepcopy(self.state[self.current]))
        self.current += 1
            
    def go_back(self):
        if self.current > 0:
            self.current -= 1

    def go_forward(self):
        if self.current < len(self.state):
            self.current += 1


    def draw(self, pixel_set):
        """
        pixel_set is the set of pixels to be colored. in this format: ((x,y), (r,g,b)), 
        the pixels are colored by the GUI in real time. After the release of the button, 
        it will be altered in the actuall image with this function.
        """
        for i in pixel_set:
            self.state[self.current][i[0][1]][i[0][0]] = i[1]


    def crop(self, new_size, top_left):
        """
        new_size gives the new proportions, top_left indicates from where should the image be cut
        top_left starts at (0, 0)
        """
        new_width, new_height = new_size
        height, width = self.state[self.current].shape[:2]

        if new_width > width or new_height > height:
            return

        self.state[self.current] = self.state[self.current][top_left[1]:top_left[1]+new_size[1], top_left[0]:top_left[0]+new_size[0], :]
        

    def color_boost(self, amount, channel):
        """
        channel: 0-R, 1-G, 2-B
        """
        arr = self.state[self.current].astype(float)

        factor = (amount - 50) / 50 if amount > 50 else (50 - amount) / 50
        if amount > 50:
            arr[:, :, channel] += (255 - arr[:, :, channel]) * factor
        else:
            arr[:, :, channel] -= arr[:, :, channel] * factor

        self.state[self.current] = np.clip(arr, 0, 255).astype(np.uint8)

    def black_and_white(self):
        gray = self.state[self.current][:, :, :3].mean(axis=2)  # average R,G,B per pixel
        mask = gray < 128                          # boolean mask
        self.state[self.current][:, :, :3] = np.where(mask[:, :, None], 0, 255)
 
    def edge_enhancer(self):    
        kernel = [
            [-1, -1, -1],
            [-1,  8, -1],
            [-1, -1, -1]
        ]
        self.state[self.current] = convolve(self.state[self.current], kernel)

    def sharpen(self):
        kernel = [
            [ 0, -1,  0],
            [-1,  5, -1],
            [ 0, -1,  0]
        ]
        self.state[self.current] = convolve(self.state[self.current], kernel)

    def box_blur(self, size):
        kernel = np.ones((size, size), dtype=float) / size**2
        self.state[self.current] = convolve(self.state[self.current], kernel)
    
    def saturation(self, amount):
        """
        amount == a scale from 0-100, amounting to the intensity of the filter, default = 50
        not linear
        """
        
        arr = cv2.cvtColor(self.state[self.current], cv2.COLOR_RGB2HSV)
        arr = arr.astype(np.float32)

        factor = (amount - 50) / 50 if amount > 50 else (50 - amount) / 50
        if amount > 50:
            arr[:, :, 1] += (255 - arr[:, :, 1]) * factor
        else:
            arr[:, :, 1] -= arr[:, :, 1] * factor

        arr = cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_HSV2RGB)  # convert back from HSV

        self.state[self.current] = np.clip(arr, 0, 255).astype(np.uint8)

    def brightness(self, amount):
        """
        amount == a scale from 0-100, amounting to the intensity of the filter, default = 50
        the brightening is not linear, it changes based of off the "brightness" of inidividual pixels
        """

        arr = self.state[self.current].astype(float)

        factor = (amount - 50) / 50 if amount > 50 else (50 - amount) / 50
        if amount > 50:
            arr[:, :, :3] += (255 - arr[:, :, :3]) * factor
        else:
            arr[:, :, :3] -= arr[:, :, :3] * factor

        self.state[self.current] = np.clip(arr, 0, 255).astype(np.uint8)

