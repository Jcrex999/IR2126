"""
Como ya hemos visto, el ejemplo 3 de teoría permite comprobar el teorema de la convolución, es decir,
que la convolución en el espacio es equivalente a un producto punto a punto en las frecuencias.

En la práctica anterior habíamos visto que, cuando una máscara de convolución 2D es separable, realizar
dos convoluciones con los vectores unidimensionales correspondientes es mucho más eficiente que
realizar la convolución con la máscara 2D. En este ejercicio, vamos a comparar los tiempos de
realizar una convolución utilizando dos máscaras unidimensionales frente a realizarla en la frecuencia.

Para ello, vamos a aplicar el filtro media con tamaños de máscara impares desde 3x3 hasta 103x103 con
paso 10, sobre una imagen cualquiera, por ejemplo, boat.511.tiff. Cuando realicemos la convolución en el
espacio lo haremos aprovechando que la máscara es separable.

Como resultado del ejercicio, debes mostrar un resultado similar al siguiente:

(imagen de ejemplo)

Como puedes ver, aparece la imagen utilizada en la prueba y dos gráficas: la línea roja muestra el tiempo
empleado por las convoluciones 1D en el espacio para cada tamaño de máscara, mientras que la línea azul
muestra el tiempo empleado cuando trabajamos en las frecuencias.

Para evitar fluctuaciones extrañas en las gráficas, debes repetir cada convolución un cierto número de veces y
considerar su tiempo de ejecución como el promedio de todas las repeticiones. En la gráfica anterior,
cada convolución se repitió 20 veces.

Comenta las gráficas obtenidas. Céntrate en la diferencia de tiempos de ejecución cuando trabajamos en el
espacio con máscaras 1D o en las frecuencias y las similitudes y diferencias con la gráfica similar que
obtuviste en la práctica anterior.

Explicacion del profesor:
En la practica 4, se compara la mascara media bidimensional contra una mascara unidimensional en
vertical y horizontal.
"""

from ejercicio3 import ComparacionTTFConvolucion
import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.fft as fft
import time


def main():
    imagen = ski.io.imread("images/boat.511.tiff")
    imagen = ski.util.img_as_float(imagen)

    tamaños = np.arange(3, 104, 10)
    tiempos_1D = []
    tiempos_FT = []

    tiempos_1D_promedio = []
    tiempos_FT_promedio = []

    for tam in tamaños:
        for i in range(20):
            print(f"Calculando para tamaño de máscara {tam}")
            comparacion = ComparacionTTFConvolucion(tam, imagen)
            mascara = comparacion.mascara_media_unidimencional()
            vectorH = mascara.reshape(1, tam)
            vectorV = mascara.reshape(tam, 1)
            mascara /= np.sum(mascara)

            mascara_centrada = comparacion.centralizar_mascara(mascara)

            # 1D
            inicio1D = time.time()
            resH = scipy.ndimage.convolve(imagen, vectorH)
            res1D = scipy.ndimage.convolve(resH, vectorV)
            fin1D = time.time()
            tiempo1D = fin1D - inicio1D
            tiempos_1D.append(tiempo1D)

            # FT
            inicioFT = time.time()
            FTimagen_filtrada = comparacion.convolucion_frecuencia(mascara_centrada)
            res_filtro_FT = comparacion.recuperar_resultado(FTimagen_filtrada)
            finFT = time.time()
            tiempoFT = finFT - inicioFT
            tiempos_FT.append(tiempoFT)

        tiempos_1D_promedio.append(np.mean(tiempos_1D))
        tiempos_FT_promedio.append(np.mean(tiempos_FT))

    fig, ax = plt.subplots()
    print(tiempos_1D_promedio)
    print(tiempos_FT_promedio)
    ax.plot(tamaños, tiempos_1D_promedio, 'r', label="1D")
    ax.plot(tamaños, tiempos_FT_promedio, 'b', label="FT")
    ax.set_xlabel("Tamaño de la máscara")
    ax.set_ylabel("Tiempo (s)")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    main()