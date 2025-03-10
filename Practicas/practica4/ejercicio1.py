# Version definitiva del ejercicio 1 pero usando clases y las funciones necesarias para mostrar las imagenes

import skimage as ski
import matplotlib.pyplot as plt
import math

class ImagenesRuido():
    def __init__(self):
        self.imagen = ski.io.imread("../images/ojo_azul.png")
        self.sp_values = (0.01,  # 1%
                          0.05,  # 5%
                          0.25)
        self.gaussian_values = (0.001,  # sigma = 0.032
                                0.005,  # sigma = 0.071
                                0.010)  # sigma = 0.1
        self.sp_noise = []
        self.gaussian_noise = []

    def add_sp_noise(self):
        for i in range(len(self.sp_values)):
            img_noise = ski.util.random_noise(self.imagen, mode="s&p", amount=self.sp_values[i])
            self.sp_noise.append(img_noise)

    def add_gaussian_noise(self):
        for i in range(len(self.gaussian_values)):
            img_noise = ski.util.random_noise(self.imagen, mode="gaussian", var=self.gaussian_values[i])
            self.gaussian_noise.append(img_noise)

    def show_images(self, titulo="Imagenes con ruido"):
        fig, axs = plt.subplots(2, len(self.sp_values) + 1, layout="constrained")
        fig.suptitle(titulo, size=24)
        axs[0, 0].imshow(self.imagen)
        axs[0, 0].set_title("Imagen original")

        for i in range(len(self.sp_values)):
            axs[0, i+1].imshow(self.sp_noise[i])
            axs[0, i+1].set_title(f"Ruido Sal y Pimienta: {self.sp_values[i] * 100:0.0f}%")

        for i in range(len(self.gaussian_values)):
            axs[1, i+1].imshow(self.gaussian_noise[i])
            axs[1, i+1].set_title(f"Ruido Gaussiano: {math.sqrt(self.gaussian_values[i]):0.2f}")

        ax = axs.ravel()
        for a in ax:
            a.set_axis_off()
        plt.show()

    def run(self):
        self.add_sp_noise()
        self.add_gaussian_noise()
        self.show_images()


if __name__ == "__main__":
    ir = ImagenesRuido()
    ir.run()