import skimage as ski
import numpy as np
import matplotlib.pyplot as plt
import math

class FiltroRuido:
    def __init__(self):
        self.imagen = ski.io.imread("../images/borrosa.png")
        self.imagen = ski.util.img_as_float(self.imagen)
        self.gaussian_filters = 3
        self.alpha = (0.5, 1.5)

    def add_gaussian_filter(self):
        return ski.filters.gaussian(self.imagen, sigma=self.gaussian_filters)

    def ecuacion(self):
        alpha_random = np.random.uniform(self.alpha[0], self.alpha[1])
        print("Alpha es: ", alpha_random)
        return self.imagen + alpha_random * (self.imagen - self.add_gaussian_filter())


if __name__ == "__main__":
    fr = FiltroRuido()
    R = fr.ecuacion()

    # Mostrar la imagen original y la imagen resultante

    fig, axs = plt.subplots(1, 2, layout="constrained")
    axs[0].imshow(fr.imagen, cmap=plt.cm.gray)
    axs[0].set_title("Imagen original")
    axs[1].imshow(R, cmap=plt.cm.gray)
    axs[1].set_title("Imagen resultante")

    for a in axs:
        a.set_axis_off()
    plt.show()
