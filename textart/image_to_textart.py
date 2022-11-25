import os.path
import numpy as np

from PIL import Image
from PIL import ImageOps


class ImgToText:
    def __init__(self, path):
        """
        Convert image to text.
        """
        self.path = path
        self.STRING_MATRIX = {
            0: "@",
            1: "W",
            2: "#",
            3: "S",
            4: "?",
            5: "O",
            6: "/",
            7: "x",
            8: "<",
            9: ":",
            10: ",",
            11: ".",
            12: " "
        }

    def get_img_name(self):
        """
        Return name of file which ends before extension .jpg .png etc...

        :return: str
        """
        img_name = self.path.split("\\")
        img_name_no_extension = img_name[-1].split(".")
        return img_name_no_extension[0]

    def image_to_text(self, width_density=10, height_density=4):
        """
        :param width_density: Specify how many pixel columns to skip.
        :param height_density: Specify how many pixel rows to skip.
        :return: None
        """
        with Image.open(self.path) as image:  # open photo
            width, height = image.size  # get image size
            image = ImageOps.grayscale(image)  # convert to grayscale
            pixels = image.load()  # pixels object has x and y coordinates for each pixel

            # get a number which represents shade of gray (by x and y coordinates of each pixel)
            # loop starts at [0, 0] and continues till the last pixel of the same row is appended
            #   then next row and on...
            pixel_array = []
            counter = 0
            while counter < height:
                for i, y in enumerate(range(width)):
                    pixel_array.append(pixels[i, counter])
                counter += 1

            # floor divide 255 shades to match the number of categories of string matrix
            reduced_gray = np.array(pixel_array) // (255 / len(self.STRING_MATRIX))

            # replace integers by string chars from string matrix
            string_array = []
            for item in reduced_gray:
                string_array.append(self.STRING_MATRIX.get(item))

            # reshape the array to 2D
            reshaped = np.reshape(string_array, (height, width))

            # specify density of string characters in the resulting image
            reduced = np.array(reshaped[::width_density, ::height_density]).tolist()

            # write to text file
            with open(os.path.join("finished images", f"{self.get_img_name()}.txt"), "w") as txt:
                for line in reduced:
                    txt.writelines(f"{''.join(line)}\n")

            print(f"Resulting shape: {np.array(reduced).shape}", "Done", sep="\n" * 2)


if __name__ == '__main__':
    # Operate here:
    instance = ImgToText(path=os.path.join('raw images', 'eagle.jpeg'))
    instance.image_to_text(width_density=10, height_density=5)
