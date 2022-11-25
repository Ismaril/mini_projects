import os.path

import requests
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


class Pixelize:
    def __init__(self,
                 pixel_density=20,
                 bit_depth=3,
                 path=None,
                 url=None,
                 name_of_image=None,
                 save_image=True):
        """
        Convert image to pixel art.

        :param pixel_density: How many pixels to skip in each axis.
        :param bit_depth: specify number of colors by bit depth (3, 6, 9)
        :param path: Insert path from local machine else None.
        :param url: Insert url from internet else None.
        :param name_of_image: Chose name of the image.
        :param save_image: True to save locally, False not to save.
        """
        self.pixel_density = pixel_density
        self.bit_depth = bit_depth
        self.path = path
        self.url = url
        self.name_of_image = name_of_image
        self.width, self.height, self.pixels = self.get_raw_image()
        self.save_image = save_image

    def get_raw_image(self) -> (int, int, object):
        assert self.path or self.url, "You must specify the path to image " \
                                      "either locally or through url."
        # exclude path to image that is not used
        if self.url:
            image_location = requests.get(self.url, stream=True).raw
        else:
            image_location = self.path

        # get raw image
        with Image.open(image_location) as image:
            width, height = image.size  # get image size like 1920x1080 etc
            pixels = image.load()  # pixels object has x and y coordinates for each pixel
            return width, height, pixels

    def get_pixel_array(self) -> np.array:
        """
        Get a tuple which represents (R, G, B)(0-255 for each)
        Loop starts at [0, 0] -> X, Y coordinates and continues till the last pixel of the same row
        is appended, then next row and on...
        """
        rgb_array = []
        counter = 0
        while counter < self.height:
            for i, y in enumerate(range(self.width)):
                rgb_array.append(self.pixels[i, counter])
            counter += 1

        return np.array(rgb_array).flatten()

    def convert_to_9_bit(self, rgb_array):
        """Reduce 255 colors to 8 for each channel. Have 512 colors per pixel"""
        # iteration below cannot be performed directly on a function parameter (rgb_array)???
        # have to assign it to a variable:
        rgb_array = rgb_array()
        flattened_9bit = []

        # return 8 color variants out of 255 colors
        for color in rgb_array:
            if color < 32:
                flattened_9bit.append(0)
            elif color < 63:
                flattened_9bit.append(32)
            elif color < 95:
                flattened_9bit.append(64)
            elif color < 127:
                flattened_9bit.append(96)
            elif color < 159:
                flattened_9bit.append(128)
            elif color < 191:
                flattened_9bit.append(160)
            elif color < 223:
                flattened_9bit.append(192)
            elif color < 256:
                flattened_9bit.append(255)

        rgb_9bit = self.convert_flattened_to_3_items(flattened_9bit)
        return np.array(rgb_9bit, dtype=int)

    def convert_to_6_bit(self, rgb_array):
        """Reduce 255 colors to 4 for each channel. Have 64 colors per pixel"""
        rgb_array = rgb_array()
        flattened_6bit = []

        # return 4 color variants out of 255 colors
        for color in rgb_array:
            if color < 63:
                flattened_6bit.append(0)
            elif color < 127:
                flattened_6bit.append(64)
            elif color < 191:
                flattened_6bit.append(128)
            elif color < 256:
                flattened_6bit.append(255)

        rgb_6bit = self.convert_flattened_to_3_items(flattened_6bit)
        return np.array(rgb_6bit, dtype=int)

    def convert_to_3_bit(self, rgb_array):
        """Reduce 255 colors to 1 for each channel. Have 8 colors per pixel"""
        rgb_array = rgb_array()
        flattened_3bit = []

        # return 1 color variant out of 255 colors
        for color in rgb_array:
            if color < 128:
                flattened_3bit.append(0)
            elif 128 <= color:
                flattened_3bit.append(255)

        rgb_3bit = self.convert_flattened_to_3_items(flattened_3bit)
        return np.array(rgb_3bit, dtype=int)

    @staticmethod
    def convert_flattened_to_3_items(flattened):
        """Convert flattened array back to 3 item object [[R,G,B], ... [R,G,B]]"""
        result = []
        rgb_container = []  # here are temporarily set RGB colors as one item
        for item in flattened:
            rgb_container.append(item)
            if len(rgb_container) == 3:
                result.append(rgb_container)
                rgb_container = []
        return result

    def reshape(self) -> np.ndarray:
        """
        Reshape the array to 2D.
        (Actually 3D if counting also RGB.)
        Slicing with steps [::self.pixel_density] -> Take only each x pixel of given X and Y array.
        """
        if self.bit_depth == 9:
            rgb_n_bit = self.convert_to_9_bit(rgb_array=self.get_pixel_array)
        elif self.bit_depth == 6:
            rgb_n_bit = self.convert_to_6_bit(rgb_array=self.get_pixel_array)
        elif self.bit_depth == 3:
            rgb_n_bit = self.convert_to_3_bit(rgb_array=self.get_pixel_array)

        reshaped = np.reshape(rgb_n_bit,
                              (self.height, self.width, 3))  # (Y, X, (R,G,B))
        sliced = reshaped[::self.pixel_density, ::self.pixel_density]
        return sliced

    def plot_prepare(self, divisor=30):
        """Display using matplotlib."""
        plt.figure(figsize=(self.width / divisor, self.height / divisor))
        plt.imshow(self.reshape())
        plt.axis("off")  # get rid of axis numbers around plot

    def plot_save(self):
        # last two parameters to remove the rest of padding etc around plot
        if self.save_image:
            plt.savefig(os.path.join("finished images", f"{self.name_of_image}.png"),
                        bbox_inches='tight',
                        pad_inches=0)

    def main(self):
        self.get_raw_image()
        print("Get raw img - done")
        self.get_pixel_array()
        print("Get pixel array - done")
        self.reshape()
        print("Reshaped - done")
        self.plot_prepare()
        print("Prepare plot - done")
        self.plot_save()
        print("Plot saved")
        plt.show()  # display figure


if __name__ == '__main__':
    set_pixel_density = 10
    set_bit_depth = 3
    set_url = None
    set_local_path = os.path.join('raw images', 'galaxy.jpg')
    set_name_of_image = 'galaxy'  # will be saved automatically as png
    set_save_image = True
    pix = Pixelize(
        pixel_density=set_pixel_density,
        bit_depth=set_bit_depth,
        path=set_local_path,
        url=set_url,
        name_of_image=set_name_of_image,
        save_image=set_save_image
    )
    pix.main()
