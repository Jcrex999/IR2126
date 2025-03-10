# Objetivos:
# - Añadir ruido con random_noise
# - Filtros media, gaussiano y mediana (rank.mean, gaussian, median)

# Ejercicio 1
# En los programas de ejemplo hemos utilizado la función random_noise para añadir ruido a una imagen en niveles de gris.
# Sin embargo, la función se puede utilizar para añadir ruido a cualquier tipo de imagen. Considera una imagen en color,
# por ejemplo, ojo_azul.png. Utiliza la función random_noise para añadirle varias cantidades de ruido sal y pimienta
# (1%, 5% y 25%) y de ruido gaussiano (varianzas 0.001, 0.005 y 0.010). Analiza los resultados obtenidos para entender
# cómo afecta el ruido en este caso.

import skimage as ski
import matplotlib.pyplot as plt
import math

imagen = ski.io.imread("../images/ojo_azul.png")
print(imagen.shape)
#imagen = ski.transform.rescale(imagen, 0.5, order=5, channel_axis=2)
#print(imagen.shape)

# Añdir ruido sal y pimiemta
sp_values = (0.01,  # 1%
             0.05,  # 5%
             0.25)  # 10%
sp_noise = []
for i in range(len(sp_values)):
    img_noise = ski.util.random_noise(imagen, mode="s&p", amount=sp_values[i])
    sp_noise.append(img_noise)

# Añadir ruido Gaussiano
gaussian_values = (0.001,  # sigma = 0.032
                   0.005,  # sigma = 0.071
                   0.010)  # sigma = 0.1
gaussian_noise = []
for i in range(len(gaussian_values)):
    img_noise = ski.util.random_noise(imagen, mode="gaussian", var=gaussian_values[i])
    gaussian_noise.append(img_noise)
"""
# Filtro Media
mean_filter_sp_noise = []
for i in range(len(sp_values)):
    filtered_image = ski.filters.rank.mean(ski.util.img_as_ubyte(sp_noise[i]), footprint=ski.morphology.footprint_rectangle((3,3)))
    mean_filter_sp_noise.append(filtered_image)

mean_filter_gaussian_noise = []
for i in range(len(gaussian_values)):
    filtered_image = ski.filters.rank.mean(ski.util.img_as_ubyte(gaussian_noise[i]), footprint=ski.morphology.footprint_rectangle((3,3)))
    mean_filter_gaussian_noise.append(filtered_image)

# Filtro Gaussiano
gaussian_filter_sp_noise = []
for i in range(len(sp_values)):
    filtered_image = ski.filters.gaussian(sp_noise[i])
    gaussian_filter_sp_noise.append(filtered_image)

gaussian_filter_gaussian_noise = []
for i in range(len(gaussian_values)):
    filtered_image = ski.filters.gaussian(gaussian_noise[i])
    gaussian_filter_gaussian_noise.append(filtered_image)

# Filtro mediana
median_filter_sp_noise = []
for i in range(len(sp_values)):
    filtered_image = ski.filters.median(sp_noise[i])
    median_filter_sp_noise.append(filtered_image)

median_filter_gaussian_noise = []
for i in range(len(gaussian_values)):
    filtered_image = ski.filters.median(gaussian_noise[i])  # footprint=ski.morphology.square(7)
    median_filter_gaussian_noise.append(filtered_image)
"""

# Mostrar Resultados
def mostar_por_imagen(titulo, f, imagen, values, noise, mean_filter, gaussian_filter, median_filter):
    for i in range(len(values)):
        fig, axs = plt.subplots(2, len(sp_values), layout="constrained")
        fig.suptitle("Ruido " + titulo.format(f(values[i])), size=24)
        axs[0, 0].imshow(imagen, cmap='gray')
        axs[0, 0].set_title("Original")

        axs[0, 1].imshow(noise[i], cmap='gray')
        axs[0, 1].set_title("Con ruido ")

        axs[1, 0].imshow(mean_filter[i], cmap='gray')
        axs[1, 0].set_title("Filtro media 3x3")

        axs[1, 1].imshow(gaussian_filter[i], cmap='gray')
        axs[1, 1].set_title("Filtro Gaussiano $\\sigma = 1$")

        axs[1, 2].imshow(median_filter[i], cmap='gray')
        axs[1, 2].set_title("Filtro mediana 3x3")

        for a in axs.ravel():
            a.set_axis_off()
        plt.show()


def mostrar_por_filtro(titulo, imagen, sp_values, gaussian_values, sp_images, gaussian_images):
    print(imagen.shape)
    fig, axs = plt.subplots(2, len(sp_values) + 1, layout="constrained")
    fig.suptitle(titulo, size=24)
    axs[0, 0].imshow(imagen)
    axs[0, 0].set_title("Original")

    for i in range(len(sp_values)):
        axs[0, i + 1].imshow(sp_images[i])
        axs[0, i + 1].set_title(f"Ruido S&P {sp_values[i] * 100:0.0f}%")

    for i in range(len(gaussian_values)):
        axs[1, i + 1].imshow(gaussian_images[i])
        axs[1, i + 1].set_title(f"Ruido Gaussiano $\\sigma$ = {math.sqrt(gaussian_values[i]):0.2f}")

    ax = axs.ravel()
    for a in ax:
        a.set_axis_off()
    plt.show()


mostrar_por_filtro("Imágenes con ruido", imagen, sp_values, gaussian_values, sp_noise, gaussian_noise)

#mostar_por_imagen("S&P {0:0.0f}%", lambda x: 100 * x, imagen, sp_values, sp_noise, mean_filter_sp_noise,
#                  gaussian_filter_sp_noise, median_filter_sp_noise)
#mostar_por_imagen("Gaussiano $\\sigma = {0:0.2f}$", lambda x: math.sqrt(x), imagen, gaussian_values, gaussian_noise,
#                  mean_filter_gaussian_noise, gaussian_filter_gaussian_noise, median_filter_gaussian_noise)

# mostrar_por_filtro("Resultados del filtro media (3x3)", imagen, sp_values, gaussian_values, mean_filter_sp_noise, mean_filter_gaussian_noise)
# mostrar_por_filtro("Resultados del filtro Gaussiano ($\sigma = 1$)", imagen, sp_values, gaussian_values, gaussian_filter_sp_noise, gaussian_filter_gaussian_noise)
# mostrar_por_filtro("Resultados del filtro mediana (3x3)", imagen, sp_values, gaussian_values, median_filter_sp_noise, median_filter_gaussian_noise)


