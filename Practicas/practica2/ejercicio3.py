"""
Elige una de las dos imágenes oscuras que te proporcionamos: calle.png o templo.png.
Como puedes observar, se trata de imágenes en color. También puedes utilizar cualquier
otra imagen oscura que tengas. Consulta a tu profesor si vas a utilizar una imagen distinta
de las proporcionadas.

Intenta mejorar el contraste de la imagen elegida de las siguientes formas:

    Usando las dos funciones de aclarado que hemos estudiado en la asignatura.
    Mediante la ecualización del histograma (equalize_hist).
    Mediante la ecualización adaptativa del histograma (equalize_adapthist).

Ten en cuenta que las funciones de ecualización del histograma solo admiten imágenes en
niveles de gris. Para aplicarlas sobre imágenes en color tendrás que programar tú explícitamente
que cada función se aplique sobre cada canal de color R, G, B independientemente.

Muestra los resultados obtenidos en 5 filas (original, aclarada1, aclarada2, ecualizada y CLAHE)
y, en cada fila, muestra la imagen correspondiente junto con los histogramas de cada plano de color.

¿Consideras que tiene sentido hacer una ecualización de histograma en una imagen en color aplicando
el proceso a cada banda por separado? ¿Cómo puede afectar esto a los colores que aparecen en la imagen?
"""

import matplotlib.pyplot as plt
from ImageProcessor import ImageProcessor


def process_image(image_path):
    ip = ImageProcessor(image_path, color=True)
    img_original = ip.img_original
    h_c_color = ip.histograma_color()

    img_clara1, h_clara1, c_clara1 = ip.aclarado()
    img_clara2, h_clara2, c_clara2 = ip.aclarado(n=3)
    img_eq, h_eq, c_eq = ip.ecualizada()
    img_eq_CLAHE, h_eq_CLAHE, c_eq_CLAHE = ip.clahe()

    fig, axs = plt.subplots(5, 4, layout="constrained", figsize=(10, 15))
    axs[0, 0].imshow(img_original)
    axs[0, 0].set_title("Original")
    axs[0, 1].bar(h_c_color[0], h_c_color[2], 1.1)
    axs[0, 1].set_title("Histograma Original, Rojo")
    axs[0, 2].bar(h_c_color[0], h_c_color[4], 1.1)
    axs[0, 2].set_title("Histograma Original, Verde")
    axs[0, 3].bar(h_c_color[0], h_c_color[6], 1.1)
    axs[0, 3].set_title("Histograma Original, Azul")

    axs[1, 0].imshow(img_clara1)
    axs[1, 0].set_title("Aclarada")
    axs[1, 1].bar(c_clara1[0], h_clara1[0], 1.1)
    axs[1, 1].set_title("Histograma Aclarada, Rojo")
    axs[1, 2].bar(c_clara1[1], h_clara1[1], 1.1)
    axs[1, 2].set_title("Histograma Aclarada, Verde")
    axs[1, 3].bar(c_clara1[2], h_clara1[2], 1.1)
    axs[1, 3].set_title("Histograma Aclarada, Azul")

    axs[2, 0].imshow(img_clara2)
    axs[2, 0].set_title("Aclarada (n=3)")
    axs[2, 1].bar(c_clara2[0], h_clara2[0], 1.1)
    axs[2, 1].set_title("Histograma Aclarada (n=3), Rojo")
    axs[2, 2].bar(c_clara2[1], h_clara2[1], 1.1)
    axs[2, 2].set_title("Histograma Aclarada (n=3), Verde")
    axs[2, 3].bar(c_clara2[2], h_clara2[2], 1.1)
    axs[2, 3].set_title("Histograma Aclarada (n=3), Azul")

    axs[3, 0].imshow(img_eq)
    axs[3, 0].set_title("Ecualizada")
    axs[3, 1].bar(c_eq[0], h_eq[0], 1.1)
    axs[3, 1].set_title("Histograma Ecualizada, Rojo")
    axs[3, 2].bar(c_eq[1], h_eq[1], 1.1)
    axs[3, 2].set_title("Histograma Ecualizada, Verde")
    axs[3, 3].bar(c_eq[2], h_eq[2], 1.1)
    axs[3, 3].set_title("Histograma Ecualizada, Azul")

    axs[4, 0].imshow(img_eq_CLAHE)
    axs[4, 0].set_title("CLAHE")
    axs[4, 1].bar(c_eq_CLAHE[0], h_eq_CLAHE[0], 1.1)
    axs[4, 1].set_title("Histograma CLAHE, Rojo")
    axs[4, 2].bar(c_eq_CLAHE[1], h_eq_CLAHE[1], 1.1)
    axs[4, 2].set_title("Histograma CLAHE, Verde")
    axs[4, 3].bar(c_eq_CLAHE[2], h_eq_CLAHE[2], 1.1)
    axs[4, 3].set_title("Histograma CLAHE, Azul")

    axs_lineal = axs.ravel()
    for i in range(0, axs_lineal.size, 2):
        axs_lineal[i].set_axis_off()
        axs_lineal[i + 1].set_xticks([0, 64, 128, 192, 255])
    plt.show()


if __name__ == "__main__":
    process_image("../images/calle.png")
    process_image("../images/templo.png")