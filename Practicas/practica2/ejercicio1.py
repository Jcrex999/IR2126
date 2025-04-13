"""
Para las imágenes medica.pgm y fachada_iglesia.pgm obtén sus correspondientes versiones:

    Aclarada (usando la primera transformación estudiada en clase).
    Ecualizada.
    CLAHE (empleando sus parámetros por defecto).

Visualiza en cada caso 4 imágenes (original, aclarada, ecualizada y CLAHE) y, debajo de cada una de ellas, su histograma.

"""

import matplotlib.pyplot as plt
from ImageProcessor import ImageProcessor


def process_image(image_path):
    ip = ImageProcessor(image_path)

    img_clara, h_clara, c_clara = ip.aclarado()
    img_eq, h_eq, c_eq = ip.ecualizada()
    img_eq_CLAHE, h_eq_CLAHE, c_eq_CLAHE = ip.clahe()
    img_original = ip.img_original
    h_orig, c_orig = ip.h_orig, ip.c_orig

    fig, axs = plt.subplots(4, 2, layout="constrained")

    axs[0, 0].imshow(img_original, cmap='gray')
    axs[0, 0].set_title("Original")
    axs[0, 1].bar(c_orig, h_orig, 1.1)

    axs[1, 0].imshow(img_clara, cmap='gray')
    axs[1, 0].set_title("Aclarada")
    axs[1, 1].bar(c_clara, h_clara, 1.1)

    axs[2, 0].imshow(img_eq, cmap='gray')
    axs[2, 0].set_title("Ecualizada")
    axs[2, 1].bar(c_eq, h_eq, 1.1)

    axs[3, 0].imshow(img_eq_CLAHE, cmap='gray')
    axs[3, 0].set_title("CLAHE")
    axs[3, 1].bar(c_eq_CLAHE, h_eq_CLAHE, 1.1)

    axs_lineal = axs.ravel()
    for i in range(0, axs_lineal.size, 2):
        axs_lineal[i].set_axis_off()
        axs_lineal[i + 1].set_xticks([0, 64, 128, 192, 255])
    plt.show()

if __name__ == "__main__":
    process_image("../images/medica.pgm")
    process_image("../images/fachada_iglesia.pgm")