"""
A partir de las máscaras gaussianas centradas que has generado en los ejercicios 1 y 2, muestra en una misma
gráfica el perfil de la línea central de cada máscara, es decir, la fila 255 de la misma (la imagen es de 511x511).
Muestra en rojo la línea del ejercicio 1 y en azul la del ejercicio 2. Para apreciar mejor las diferencias,
puedes mostrar solo la parte central de cada fila, por ejemplo, la parte comprendida entre los índices 240 y 270
(ambos incluidos).

Comenta las gráficas obtenidas. ¿Puedes explicar ahora por qué la transformada de Fourier de la segunda gaussiana
se parece más a la transformada de un filtro media que a la transformada de un filtro gaussiano? ¿Puedes dar alguna
recomendación a la hora de diseñar un filtro gaussiano?
"""

import skimage as ski
import matplotlib.pyplot as plt
import numpy as np
import scipy
import scipy.fft as fft

class ComparacionTTFConvolucion():
    def __init__(self, tam, sigma, imagen):
        self.tam = tam
        self.sigma = sigma
        self.imagen = imagen

    def mascara_gaussiana_unidimencional(self):
        vector = scipy.signal.windows.gaussian(self.tam, self.sigma)
        vector /= np.sum(vector)
        return vector

    def mascara_gaussiana_bidimencional(self):
        vector = self.mascara_gaussiana_unidimencional()
        vectorH = vector.reshape(1, self.tam)
        vectorV = vector.reshape(self.tam, 1)
        return vectorV @ vectorH

    def centralizar_mascara(self, mascara, imagen):
        mascara_centrada = np.zeros(imagen.shape)
        fila_i = imagen.shape[0] // 2 - self.tam // 2
        col_i = imagen.shape[1] // 2 - self.tam // 2
        mascara_centrada[fila_i:fila_i + self.tam, col_i:col_i + self.tam] = mascara
        return mascara_centrada

    def convolucion_espacio(self, imagen, mascara):
        return scipy.ndimage.convolve(imagen, mascara, mode="wrap")

    def convolucion_frecuencia(self, imagen, mascara):
        FTimagen = fft.fft2(imagen)
        mascara_en_origen = fft.ifftshift(mascara)
        FTmascara = fft.fft2(mascara_en_origen)
        return FTimagen * FTmascara

    


    def run(self):
        self.graficar_perfil()
        #self.graficar_perfiles()

if __name__ == "__main__":
    ejercicio = ComparacionTTFConvolucion(31, 5)
    ejercicio.run()