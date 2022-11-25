# This code was not created by me, only adjusted

import numpy as np
import matplotlib.pyplot as plt

RE_SCALE = 1
WIDTH = 1920*RE_SCALE
HEIGHT = 1080*RE_SCALE


def mandelbrot(width, height, max_iteration=20, r=2):
    """Returns an image of the Mandelbrot fractal of size (h,w)."""
    x = np.linspace(-2.5, 1.5, width)
    y = np.linspace(-1.5, 1.5, height)
    a, b = np.meshgrid(x, y)
    c = a + b * 1j
    z = np.zeros_like(c)

    divtime = max_iteration + np.zeros(z.shape, dtype=int)
    print("first section done")

    for i in range(max_iteration):
        z = z ** 2 + c
        diverge = abs(z) > r
        print("working", i)

        div_now = diverge & (divtime == max_iteration)  # who is diverging now
        divtime[div_now] = i  # note when
        z[diverge] = r  # avoid diverging too much

    print("done")
    return divtime


plt.imsave("C:/Users/lazni/PycharmProjects/Training/Mini projects/mandelbrot/finished images/mandel4.png",
           mandelbrot(WIDTH, HEIGHT))
