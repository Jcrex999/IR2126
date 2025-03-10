# En este ejercio tengo que usar los filtros para eliminar el ruido.
# Considera la imagen hombre_con_ruido.png. Muestra los resultados de aplicar sobre ella los siguientes filtros:

#    Filtro media 3x3, 5x5 y 7x7
#    Filtro gaussiano con desviación típica 1, 1.25 y 1.75
#    Filtro mediana 3x3, 5x5 y 7x7

#Comenta los resultados obtenidos en cada caso desde el punto de vista de la eliminación del ruido y cómo se ven
# afectados los detalles de la imagen (las rayas de la camisa, la textura del jersey, etc).

import skimage as ski
import matplotlib.pyplot as plt
import math

class FiltroRuido:
    def __init__(self):
        self.imagen = ski.io.imread("../images/hombre_con_ruido.png")
        self.mean_filters = (3, 5, 7)
        self.gaussian_filters = (1, 1.25, 1.75)
        self.median_filters = (3, 5, 7)
        self.mean_filtered = []
        self.gaussian_filtered = []
        self.median_filtered = []

    def add_mean_filter(self):
        for i in range(len(self.mean_filters)):
            filtered_image = ski.filters.rank.mean(ski.util.img_as_ubyte(self.imagen), footprint=ski.morphology.footprint_rectangle((self.mean_filters[i], self.mean_filters[i])))
            self.mean_filtered.append(filtered_image)

    def add_gaussian_filter(self):
        for i in range(len(self.gaussian_filters)):
            filtered_image = ski.filters.gaussian(self.imagen, sigma=self.gaussian_filters[i])
            self.gaussian_filtered.append(filtered_image)

    def add_median_filter(self):
        for i in range(len(self.median_filters)):
            filtered_image = ski.filters.median(self.imagen, footprint=ski.morphology.footprint_rectangle((self.median_filters[i], self.median_filters[i])))
            self.median_filtered.append(filtered_image)

    def show_images(self):
        fig, axs = plt.subplots(3, len(self.mean_filters) + 1, layout="constrained")
        fig.suptitle("Filtros de ruido", size=24)
        axs[0, 0].imshow(self.imagen, cmap=plt.cm.gray)
        axs[0, 0].set_title("Imagen original")

        for i in range(len(self.mean_filters)):
            axs[0, i+1].imshow(self.mean_filtered[i], cmap=plt.cm.gray)
            axs[0, i+1].set_title(f"Filtro media {self.mean_filters[i]}x{self.mean_filters[i]}")

        for i in range(len(self.gaussian_filters)):
            axs[1, i+1].imshow(self.gaussian_filtered[i], cmap=plt.cm.gray)
            axs[1, i+1].set_title(f"Filtro gaussiano $\sigma$ = {self.gaussian_filters[i]:0.2f}")

        for i in range(len(self.median_filters)):
            axs[2, i+1].imshow(self.median_filtered[i], cmap=plt.cm.gray)
            axs[2, i+1].set_title(f"Filtro mediana {self.median_filters[i]}x{self.median_filters[i]}")

        ax = axs.ravel()
        for a in ax:
            a.set_axis_off()
        plt.show()

    def run(self):
        self.add_mean_filter()
        self.add_gaussian_filter()
        self.add_median_filter()
        self.show_images()


if __name__ == "__main__":
    fr = FiltroRuido()
    fr.run()

# En el caso de los filtros de media, se puede observar que a medida que aumenta el tamaño del filtro, la imagen se va
# difuminando. En el caso del filtro de media 3x3, la imagen se ve bastante difuminada, mientras que en el caso del filtro
# de media 7x7, la imagen se ve bastante borrosa. En cuanto a los detalles de la imagen, se pueden observar que los detalles
# se van perdiendo a medida que aumenta el tamaño del filtro. En el caso del filtro de media 3x3, se pueden observar los detalles
# de la imagen, pero se ven bastante difuminados. En el caso del filtro de media 7x7, los detalles de la imagen se ven muy
# difuminados y casi no se pueden observar.

# En el caso de los filtros gaussianos, se puede observar que a medida que aumenta la desviación típica, la imagen se va
# difuminando. En el caso del filtro gaussiano con $\sigma$ = 1, la imagen se ve bastante difuminada, mientras que en el caso
# del filtro gaussiano con $\sigma$ = 1.75, la imagen se ve bastante borrosa. En cuanto a los detalles de la imagen, se pueden
# observar que los detalles se van perdiendo a medida que aumenta la desviación típica. En el caso del filtro gaussiano con
# $\sigma$ = 1, se pueden observar los detalles de la imagen, pero se ven bastante difuminados. En el caso del filtro gaussiano
# con $\sigma$ = 1.75, los detalles de la imagen se ven muy difuminados y casi no se pueden observar.

# En el caso de los filtros de mediana, se puede observar que a medida que aumenta el tamaño del filtro, la imagen se va
# difuminando. En el caso del filtro de mediana 3x3, la imagen se ve bastante difuminada, mientras que en el caso del filtro
# de mediana 7x7, la imagen se ve bastante borrosa. En cuanto a los detalles de la imagen, se pueden observar que los detalles
# se van perdiendo a medida que aumenta el tamaño del filtro. En el caso del filtro de mediana 3x3, se pueden observar los detalles
# de la imagen, pero se ven bastante difuminados. En el caso del filtro de mediana 7x7, los detalles de la imagen se ven muy
# difuminados y casi no se pueden observar.

# En general, para el caso del filtro media = 3x3, filtro gaussiano $\sigma$ = 1 y filtro mediana = 3x3, se pueden observar
# que las diferencias son mínimas, pero se puede observar que el filtro gaussiano $\sigma$ = 1 es el que mejor conserva los
# detalles de la imagen.