"""
Ejercicio 2

Para la imagen medica.pgm muestra la imagen original junto con los resultados obtenidos al
realizar una ecualización CLAHE combinando los siguientes parámetros:

    kernel_size: valor por defecto (None), 8 y 2.
    clip_limit: valor por defecto (0.01), 0.05, 0.1 y 1.

"""

import matplotlib.pyplot as plt
from ImageProcessor import ImageProcessor

def process_image(image_path):
    ip = ImageProcessor(image_path)

    img_original = ip.img_original
    h_orig, c_orig = ip.h_orig, ip.c_orig

    # Parámetros para CLAHE
    kernel_sizes = [None, 8, 2]
    clip_limits = [0.01, 0.05, 0.1, 1]

    # Mostrar la imagen original
    fig, axs = plt.subplots(1, 2, layout="constrained")
    axs[0].imshow(img_original, cmap='gray')
    axs[0].set_title("Original")
    axs[1].bar(c_orig, h_orig, 1.1)
    plt.show()

    fig, axs = plt.subplots(len(kernel_sizes), len(clip_limits) * 2, figsize=(15, 10), layout="constrained")
    for i, kernel_size in enumerate(kernel_sizes):
        for j, clip_limit in enumerate(clip_limits):
            img_eq_CLAHE, h_eq_CLAHE, c_eq_CLAHE = ip.clahe(kernel_size=kernel_size, clip_limit=clip_limit)
            axs[i, j * 2].imshow(img_eq_CLAHE, cmap='gray')
            axs[i, j * 2].set_title(f"Kernel: {kernel_size}, Clip: {clip_limit}")
            axs[i, j * 2 + 1].bar(c_eq_CLAHE, h_eq_CLAHE, 1.1)

    for ax in axs.ravel():
        ax.set_axis_off()

    plt.show()


if __name__ == "__main__":
    process_image("../images/medica.pgm")