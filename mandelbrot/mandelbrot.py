# This code was not created by me, only adjusted
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

RE_SCALE = 4
# WIDTH = 1920 * RE_SCALE
# HEIGHT = 1080 * RE_SCALE
WIDTH = 600
HEIGHT = 400
# _zoomGlobal = 1


# def mandelbrot_rows(args):
#     y_start, y_end, width, height, max_iteration, r, x_min, x_max, y_min, y_max = args
#     x = np.linspace(x_min, x_max, width)
#     y = np.linspace(y_min, y_max, height)[y_start:y_end]
#     a, b = np.meshgrid(x, y)
#     c = a + b * 1j
#     z = np.zeros_like(c)
#     divtime = max_iteration + np.zeros(z.shape, dtype=int)
#     for i in range(max_iteration):
#         z = z ** 2 + c
#         diverge = abs(z) > r
#         div_now = diverge & (divtime == max_iteration)
#         divtime[div_now] = i
#         z[diverge] = r
#     return (y_start, y_end, divtime)

# with smoothing
def mandelbrot_rows(args):
    y_start, y_end, width, height, max_iteration, r, x_min, x_max, y_min, y_max = args
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)[y_start:y_end]
    a, b = np.meshgrid(x, y)
    c = a + b * 1j
    z = np.zeros_like(c)
    divtime = np.full(z.shape, max_iteration, dtype=float)
    m = np.full(z.shape, True, dtype=bool)
    for i in range(max_iteration):
        z[m] = z[m] ** 2 + c[m]
        escaped = np.abs(z) > r
        just_escaped = escaped & m
        # Smoothing
        divtime[just_escaped] = i + 1 - np.log2(np.log(np.abs(z[just_escaped])))
        m[just_escaped] = False
    return (y_start, y_end, divtime)


def mandelbrot_parallel(width, height, max_iteration=20, r=2, processes=None, zoom=1):
    center_x = -0.55
    center_y = 0.55
    x_min = center_x - 2.5 / zoom
    x_max = center_x + 1.5 / zoom
    y_min = center_y - 1.5 / zoom
    y_max = center_y + 1.5 / zoom
    chunk_size = 100
    args_list = []
    for y_start in range(0, height, chunk_size):
        y_end = min(y_start + chunk_size, height)
        args_list.append((y_start, y_end, width, height, max_iteration, r, x_min, x_max, y_min, y_max))
    result = np.zeros((height, width), dtype=float)  # previously dtype=int
    with mp.Pool(processes=processes) as pool:
        for y_start, y_end, divtime in pool.map(mandelbrot_rows, args_list):
            result[y_start:y_end, :] = divtime
    return result


# Example of zooming/animating
if __name__ == "__main__":
    import os
    from time import perf_counter
    import math

    folder = f"finished images/ser9"
    nr_of_images = 50
    os.makedirs(folder, exist_ok=True)
    iterations_start = 100
    iterations = iterations_start
    _zoomGlobal = 1
    # linspace = np.linspace(1.15, 1.01, nr_of_images)
    linspace = [1.25] * 10 #, 1.20, 1.20, 1.20, 1.20, 1.20, 1.20, 1.20, 1.20, 1.20]
    k = [1.00] * 10
    l = [1.03] * 10
    m =  [1.01] * 10
    n = [1.00] * 10
    linspace = linspace + k + l + m + n
    # 1.01, 1.01, 1.01, 1.01, 1.05, 1.05, 1.05, 1.05, 1.05, 1.05,
    # 1.04, 1.04, 1.04, 1.04, 1.04, 1.03, 1.03, 1.03, 1.03, 1.03,
    # 1.02, 1.02, 1.02, 1.02, 1.02, 1.01, 1.01, 1.01, 1.01, 1.01,
    # 1.00, 1.00, 1.00, 1.00, 1.00, 0.99, 0.99, 0.99, 0.99, 0.99,
    # ]

    for i in range(nr_of_images):
        start = perf_counter()
        print("Zoom", _zoomGlobal)
        print("Iterations", int(iterations))
        plt.imsave(
            f"{folder}/mandel{i}.png",
            mandelbrot_parallel(WIDTH, HEIGHT, max_iteration=int(iterations), zoom=_zoomGlobal),
            # cmap="RdGy",
            cmap="seismic",
        )
        # tohle je docela good --------------------------------------
        _zoomGlobal *= 2
        iterations = iterations_start * math.log2(_zoomGlobal + 1)
        # iterations *= 1.051
        # -----------------------------------------------------------
        # _zoomGlobal *= 1.01
        # iterations *= 1.0006
        end = perf_counter()
        print(f"Image done {i} in time {end - start}\n", "-" * 50)


# ======================================================================================================
# CODE THAT IS WORKING
# import numpy as np
# import matplotlib.pyplot as plt
#
# RE_SCALE = 4
# WIDTH = 1920 * RE_SCALE
# HEIGHT = 1080 * RE_SCALE
# _zoomGlobal = 1
#
#
# def mandelbrot(width, height, max_iteration=20, r=2):
#     """Returns an image of the Mandelbrot fractal of size (h,w)."""
#
#     center_x = -0.55
#     center_y = -0.55
#     zoom = _zoomGlobal
#
#     x_min = center_x - 2.5 / zoom
#     x_max = center_x + 1.5 / zoom
#     y_min = center_y - 1.5 / zoom
#     y_max = center_y + 1.5 / zoom
#
#     # Make X and Y axes by linearly spaced numbers
#     x = np.linspace(x_min, x_max, width)
#     y = np.linspace(y_min, y_max, height)
#
#     # A and B are 2D arrays of the same shape, that will be used to create coordinates
#     a, b = np.meshgrid(x, y)
#
#     # Combine A (
#     c = a + b * 1j
#     z = np.zeros_like(c)
#
#     divtime = max_iteration + np.zeros(z.shape, dtype=int)
#     # print("first section done")
#
#     for i in range(max_iteration):
#         z = z ** 2 + c
#         diverge = abs(z) > r
#         # print("working", i)
#
#         div_now = diverge & (divtime == max_iteration)  # who is diverging now
#         divtime[div_now] = i  # note when
#         z[diverge] = r  # avoid diverging too much
#
#     print("done")
#     return divtime
#
# iterations = 80
# # def main():
# for i in range(100):
#     print("Zoom", _zoomGlobal)
#     print("Iterations", int(iterations))
#     plt.imsave(
#         f"finished images/ser/mandel{i}.png",
#         mandelbrot(WIDTH, HEIGHT, max_iteration=int(iterations)),
#         cmap="seismic",
#     )
#     _zoomGlobal *= 1.5
#     iterations *= 1.1
#     print("Image done", i, "-"*120)

# ======================================================================================================
# import numpy as np
# import matplotlib.pyplot as plt
#
# width, height = 600, 400
# xmin, xmax = -1.0, 0.0
# ymin, ymax = -0.5, 0.5
# max_iter = 100
#
# image = np.zeros((height, width))
#
# for x in range(width):
#     for y in range(height):
#         real = xmin + (x / width) * (xmax - xmin)
#         imag = ymin + (y / height) * (ymax - ymin)
#         complex_nrs = complex(real, imag)
#         z = 0
#         n = 0
#         while abs(z) <= 2 and n < max_iter:
#             z = z**2 + complex_nrs
#             n += 1
#         image[y, x] = n
#
# print(image.shape)
# # remove all the borders and paading
# # plt.imshow(image, cmap='hot') #, extent=(xmin, xmax, ymin, ymax))
# # # Show only image without axis, ticks, etc.
# # plt.axis('off')
# # # plt.colorbar()
# # # plt.title("Mandelbrot Fractal")
# # # plt.xlabel("Real")
# # # plt.ylabel("Imaginary")
# # # plt.show()
# plt.imshow(image)
# plt.axis("off")
# plt.savefig("mandelbrot.png")#, bbox_inches='tight', pad_inches=0)