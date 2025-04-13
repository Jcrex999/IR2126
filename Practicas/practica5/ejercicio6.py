from Practicas.practica5.ejercicio5 import Filtros
import matplotlib.pyplot as plt
import numpy as np
import skimage as ski


def mostrar_filtros(filtro_bajo, filtro_alto):
    """
    Muestra los filtros de paso bajo, paso alto y paso banda.
    """
    fig, axs = plt.subplots(1, 2, layout="constrained")
    axs[0].imshow(filtro_bajo, cmap=plt.cm.gray)
    axs[1].imshow(filtro_alto, cmap=plt.cm.gray)

    for a in axs.ravel():
        a.set_axis_off()
    plt.show()

def sumar_imagenes(img1, img2):
    """
    Suma dos imágenes de la misma dimensión.
    """
    if img1.shape != img2.shape:
        raise ValueError("Las imágenes deben tener la misma dimensión.")

    obj1 = Filtros(img1, 20)
    obj2 = Filtros(img2, 20)

    filtro_bajo = obj1.filtro_paso_bajo()
    filtro_alto = obj2.filtro_paso_alto()
    mostrar_filtros(filtro_bajo, filtro_alto)

    filtro_bajo_fft = obj1.calcular_transformada(filtro_bajo)
    filtro_alto_fft = obj2.calcular_transformada(filtro_alto)
    mostrar_filtros(filtro_bajo_fft, filtro_alto_fft)

    filtro_bajo_fft_vis = np.log(np.absolute(filtro_bajo_fft) + 1)
    filtro_alto_fft_vis = np.log(np.absolute(filtro_alto_fft) + 1)
    mostrar_filtros(filtro_bajo_fft_vis, filtro_alto_fft_vis)

    return filtro_bajo_fft + filtro_alto_fft

def main():
    img1 = ski.io.imread("images/Einstein.png")
    img2 = ski.io.imread("images/Marilyn.png")

    img1 = ski.util.img_as_float(img1)
    img2 = ski.util.img_as_float(img2)

    suma_imgs = sumar_imagenes(img1, img2)

    plt.imshow(suma_imgs, cmap=plt.cm.gray)
    plt.show()

if __name__ == "__main__":
    main()