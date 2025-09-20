import numpy as np

def convolve(img, kernel):
    kernel = np.array(kernel, dtype=float)
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2

    height, width, channels = img.shape
    output = np.zeros_like(img, dtype=float)

    # Pad the image to handle borders
    padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w), (0, 0)), mode='edge')

    # Loop over channels
    for c in range(channels):
        for y in range(height):
            for x in range(width):
                region = padded[y:y+kh, x:x+kw, c]
                output[y, x, c] = np.sum(region * kernel)

    return np.clip(output, 0, 255).astype(np.uint8)
