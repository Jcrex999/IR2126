# En el ejemplo 3 de teoría se puede ver que cuando una máscara de convolución 2D es separable, obtenemos el mismo
# resultado aplicando dos convoluciones con vectores unidimensionales.

# En este ejercicio debes aplicar el filtro media, tanto con máscaras bidimensionales como unidimensionales de
# tamaños impares de 3 a 21 (ambos incluidos), sobre una imagen cualquiera, por ejemplo, boat.512.tiff.

# Como puedes ver, aparece la imagen utilizada en la prueba y dos gráficas: la línea roja muestra el tiempo empleado en
# la convolución bidimensional para cada tamaño de máscara, mientras que la línea azul muestra el tiempo empleado por
# las convoluciones unidimensionales.

# Para evitar fluctuaciones extrañas en las gráficas, debes repetir cada convolución un cierto número de veces y
# considerar su tiempo de ejecución como el promedio de todas las repeticiones. En la gráfica anterior, cada
# convolución se repitió 10 veces.

# Comenta las gráficas obtenidas. Céntrate en la diferencia de tiempos de ejecución entre la convolución 2D y las
# dos convoluciones 1D.

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import time

class Convuluciones():
    def __init__(self):
        self.imagen = ski.io.imread("../images/boat.512.tiff")
        self.imagen = ski.util.img_as_float(self.imagen)
        self.mask_size = 21
        self.std_dev = 3
        self.vector = 0
        self.vectorH = 0
        self.vectorV = 0
        self.matriz = 0
        self.res1D = 0
        self.res2D = 0
        self.tiempos2D = []
        self.tiempos1D = []

    def convolucion_2D(self):
        inicio2D = time.time()
        self.res2D = scipy.ndimage.convolve(self.imagen, self.matriz)
        fin2D = time.time()
        tiempo2D = fin2D - inicio2D
        self.tiempos2D.append(tiempo2D)

    def convolucion_1D(self):
        inicio1D = time.time()
        resH = scipy.ndimage.convolve(self.imagen, self.vectorH)
        self.res1D = scipy.ndimage.convolve(resH, self.vectorV)
        fin1D = time.time()
        tiempo1D = fin1D - inicio1D
        self.tiempos1D.append(tiempo1D)

    def convolucion_varios_tam(self):
        for i in range(3, self.mask_size+1, 2):
            self.vector = scipy.signal.windows.gaussian(i, self.std_dev)
            self.vector /= np.sum(self.vector)
            self.vectorH = self.vector.reshape(1, i)
            self.vectorV = self.vector.reshape(i, 1)
            self.matriz = self.vectorV @ self.vectorH
            for _ in range(10):
                self.convolucion_2D()
                self.convolucion_1D()

    def show_graph(self):
        fig, axs = plt.subplots(1, 3, layout="constrained")
        axs[0].imshow(self.imagen, cmap='gray')
        axs[0].set_title("Original")
        axs[1].imshow(self.res2D, cmap='gray')
        axs[1].set_title("Convolución 2D")
        axs[2].imshow(self.res1D, cmap='gray')
        axs[2].set_title("Convoluciones 1D")
        for a in axs:
            a.set_axis_off()
        plt.show()

        # Gráfica de tiempos en el eje x los tamaños de las máscaras y en el eje y los tiempos de ejecución
        tiempo2D_mean = np.mean(self.tiempos2D)
        tiempo1D_mean = np.mean(self.tiempos1D)
        plt.plot(self.tiempos2D, color='red')
        plt.plot(self.tiempos1D, color='blue')
        plt.axhline(y=tiempo2D_mean, color='red', linestyle='--')
        plt.axhline(y=tiempo1D_mean, color='blue', linestyle='--')
        plt.xlabel("Tamaño de la máscara")
        plt.ylabel("Tiempo de ejecución")
        plt.show()

    def run(self):
        self.convolucion_varios_tam()
        self.show_graph()

        print("¿Obtenemos el mismo resultado?", np.allclose(self.res2D, self.res1D))
        print(f"Tiempo empleado con máscara  2D: {np.mean(self.tiempos2D):0.9f}")
        print(f"Tiempo empleado con máscaras 1D: {np.mean(self.tiempos1D):0.9f}")
        print(f"Factor 2D/1D: {np.mean(self.tiempos2D) / np.mean(self.tiempos1D):0.2f}")



if __name__ == "__main__":
    c = Convuluciones()
    c.run()