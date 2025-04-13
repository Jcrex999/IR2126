"""
En el ejemplo 4 de teoría se muestra cómo aplicar un filtro de paso bajo y un filtro de paso
alto sobre una imagen para una frecuencia de corte dada. Modifica una copia de dicho programa
para que, a partir de dos frecuencias de corte dadas, por ejemplo, 40 y 100, cree un filtro de
paso bajo, un filtro de paso banda y un filtro de paso alto. Debes mostrar por pantalla los tres
filtros diseñados, los resultados de aplicar los mismos a la transformada de Fourier, y la
transformada inversa de las frecuencias seleccionadas en cada caso, es decir, debes mostrar
los resultados de forma similar a como se hace en el ejemplo, pero teniendo en cuenta que ahora
tendrás tres filtros en lugar de dos.

Para terminar, debes sumar los resultados de las tres transformadas inversas para obtener una
sola imagen. Comprueba con la función np.allclose que la imagen obtenida tras sumar los tres
resultados es exactamente la misma que la imagen original. ¿A qué propiedad de la transformada
de Fourier se debe este resultado?
"""

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.fft as fft

class Filtros():
    def __init__(self, imagen, radio=100):
        self.imagen = imagen
        self.FTimagen_centrada = None
        self.radio = radio

    def crear_circulo_centrado(self):
        filas = np.matrix(list(range(self.imagen.shape[0]))).T - self.imagen.shape[0] // 2
        cols = np.matrix(list(range(self.imagen.shape[1]))) - self.imagen.shape[1] // 2
        indices_dentro = np.power(filas, 2) + np.power(cols, 2) < self.radio ** 2
        circulo = np.zeros(self.imagen.shape)
        circulo[indices_dentro] = 1
        return circulo

    def filtro_paso_bajo(self):
        return self.crear_circulo_centrado()

    def filtro_paso_alto(self):
        return 1 - self.filtro_paso_bajo()

    def filtro_paso_banda(self):
        return self.crear_circulo_centrado() - self.crear_circulo_centrado()

    def calcular_transformada(self, filtro):
        FTimagen = fft.fft2(self.imagen)
        self.FTimagen_centrada = fft.fftshift(FTimagen)
        FT_imagen_filtrada = self.FTimagen_centrada * filtro
        imagen_filtrada = fft.ifft2(fft.ifftshift(FT_imagen_filtrada))
        imagen_filtrada_real = np.real(imagen_filtrada)
        imagen_filtrada_imag = np.imag(imagen_filtrada)
        if not np.allclose(imagen_filtrada_imag, np.zeros(self.imagen.shape)):
            print("Warning. Algo no está yendo bien!!")
        return imagen_filtrada_real

    def mostrar_resultados(self):
        fig, axs = plt.subplots(2, 4, layout="constrained")
        axs[0, 0].imshow(self.imagen, cmap=plt.cm.gray)
        axs[0, 1].imshow(self.filtro_paso_bajo(), cmap=plt.cm.gray)
        axs[0, 2].imshow(np.log(np.absolute(self.calcular_transformada(self.filtro_paso_bajo())) + 1), cmap=plt.cm.gray)
        axs[0, 3].imshow(self.calcular_transformada(self.filtro_paso_bajo()), cmap=plt.cm.gray)

        axs[1, 0].imshow(np.log(np.absolute(self.FTimagen_centrada) + 1), cmap=plt.cm.gray)
        axs[1, 1].imshow(self.filtro_paso_alto(), cmap=plt.cm.gray)
        axs[1, 2].imshow(np.log(np.absolute(self.calcular_transformada(self.filtro_paso_alto())) + 1), cmap=plt.cm.gray)
        axs[1, 3].imshow(self.calcular_transformada(self.filtro_paso_alto()), cmap=plt.cm.gray)

        for a in axs.ravel():
            a.set_axis_off()
        plt.show()

    def sumar_resultados(self):
        suma = self.calcular_transformada(self.filtro_paso_bajo()) + self.calcular_transformada(self.filtro_paso_alto()) + self.calcular_transformada(self.filtro_paso_banda())
        print("¿Obtenemos el mismo resultado?", np.allclose(suma, self.imagen))

        fig, axs = plt.subplots(1, 2, layout="constrained")
        axs[0].imshow(suma, cmap=plt.cm.gray)
        axs[1].imshow(self.imagen, cmap=plt.cm.gray)

        for a in axs.ravel():
            a.set_axis_off()

        plt.show()

def crear_filtros(imagen, radio1, radio2):
    """
    Crea los filtros de paso bajo, paso alto y paso banda para una imagen dada.
    """
    filtro1 = Filtros(imagen, radio1)
    filtro2 = Filtros(imagen, radio2)

    filtro_bajo = filtro1.filtro_paso_bajo()
    filtro_banda = filtro2.filtro_paso_bajo() - filtro1.filtro_paso_bajo()
    filtro_alto = filtro2.filtro_paso_alto()
    mostrar_filtros(filtro_bajo, filtro_banda, filtro_alto)

    filtro_bajo_fft = filtro1.calcular_transformada(filtro_bajo)
    filtro_banda_fft = filtro2.calcular_transformada(filtro_banda)
    filtro_alto_fft = filtro2.calcular_transformada(filtro_alto)
    mostrar_filtros(filtro_bajo_fft, filtro_banda_fft, filtro_alto_fft)

    filtro_bajo_fft_vis = np.log(np.absolute(filtro_bajo_fft) + 1)
    filtro_banda_fft_vis = np.log(np.absolute(filtro_banda_fft) + 1)
    filtro_alto_fft_vis = np.log(np.absolute(filtro_alto_fft) + 1)
    mostrar_filtros(filtro_bajo_fft_vis, filtro_banda_fft_vis, filtro_alto_fft_vis)

    suma_imgs = filtro_bajo_fft + filtro_banda_fft + filtro_alto_fft
    print("¿Obtenemos el mismo resultado?", np.allclose(suma_imgs, imagen))
    mostrar_filtros(suma_imgs, imagen, imagen)



def mostrar_filtros(filtro_bajo, filtro_banda, filtro_alto):
    """
    Muestra los filtros de paso bajo, paso alto y paso banda.
    """
    fig, axs = plt.subplots(1, 3, layout="constrained")
    axs[0].imshow(filtro_bajo, cmap=plt.cm.gray)
    axs[1].imshow(filtro_banda, cmap=plt.cm.gray)
    axs[2].imshow(filtro_alto, cmap=plt.cm.gray)

    for a in axs.ravel():
        a.set_axis_off()

    plt.show()

def main():
    imagen = ski.io.imread("images/boat.511.tiff")
    imagen = ski.util.img_as_float(imagen)

    radio1 = 40
    radio2 = 100

    crear_filtros(imagen, radio1, radio2)



if __name__ == "__main__":
    main()