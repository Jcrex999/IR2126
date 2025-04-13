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
    def __init__(self, tam, imagen, sigma=None):
        self.tam = tam
        self.sigma = sigma
        self.imagen = imagen

    def mascara_gaussiana_unidimencional(self):
        if self.sigma is None:
            print("No se ha especificado sigma.")
            return None
        else:
            vector = scipy.signal.windows.gaussian(self.tam, self.sigma)
            vector /= np.sum(vector)
            return vector

    def mascara_gaussiana_bidimencional(self):
        vector = self.mascara_gaussiana_unidimencional()
        vectorH = vector.reshape(1, self.tam)
        vectorV = vector.reshape(self.tam, 1)
        return vectorV @ vectorH

    def mascara_media_unidimencional(self):
        vector = np.ones(self.tam) / self.tam
        return vector

    def mascara_media_bidimencional(self):
        vector = self.mascara_media_unidimencional()
        vectorH = vector.reshape(1, self.tam)
        vectorV = vector.reshape(self.tam, 1)
        return vectorV @ vectorH

    def centralizar_mascara(self, mascara):
        mascara_centrada = np.zeros(self.imagen.shape)
        fila_i = self.imagen.shape[0] // 2 - self.tam // 2
        col_i = self.imagen.shape[1] // 2 - self.tam // 2
        mascara_centrada[fila_i:fila_i + self.tam, col_i:col_i + self.tam] = mascara
        return mascara_centrada

    def convolucion_espacio(self, mascara):
        return scipy.ndimage.convolve(self.imagen, mascara, mode="wrap")

    def convolucion_frecuencia(self, mascara):
        FTimagen = fft.fft2(self.imagen)
        mascara_en_origen = fft.ifftshift(mascara)
        FTmascara = fft.fft2(mascara_en_origen)
        return FTimagen * FTmascara

    def recuperar_resultado(self, FTimagen_filtrada):
        res_filtro_FT = fft.ifft2(FTimagen_filtrada)
        res_filtro_real = np.real(res_filtro_FT)
        res_filtro_imag = np.imag(res_filtro_FT)
        if not np.allclose(res_filtro_imag, np.zeros(self.imagen.shape)):
            print("Warning. Algo no está yendo bien!!!")
        return res_filtro_real

    def graficar_perfil(self):
        mascara1 = self.mascara_gaussiana_unidimencional()
        mascara2 = self.mascara_gaussiana_bidimencional()
        mascara1 /= np.sum(mascara1)
        mascara2 /= np.sum(mascara2)
        mascara1_centrada = self.centralizar_mascara(mascara1)
        mascara2_centrada = self.centralizar_mascara(mascara2)
        perfil1 = mascara1_centrada[255, 240:271]
        perfil2 = mascara2_centrada[255, 240:271]
        plt.plot(perfil1, color="red")
        plt.plot(perfil2, color="blue")
        plt.show()

    def run(self):
        self.graficar_perfil()
        #self.graficar_perfiles()

if __name__ == "__main__":
    ejercicio1 = ComparacionTTFConvolucion(31, ski.io.imread("images/boat.511.tiff"),5)
    ejercicio2 = ComparacionTTFConvolucion(5, ski.io.imread("images/boat.511.tiff"), 5)

    mascara1 = ejercicio1.mascara_gaussiana_unidimencional()
    mascara2 = ejercicio2.mascara_gaussiana_bidimencional()
    mascara1 /= np.sum(mascara1)
    mascara2 /= np.sum(mascara2)
    mascara1_centrada = ejercicio1.centralizar_mascara(mascara1)
    mascara2_centrada = ejercicio2.centralizar_mascara(mascara2)
    perfil1 = mascara1_centrada[255, 240:271]
    perfil2 = mascara2_centrada[255, 240:271]
    plt.plot(perfil1, color="red")
    plt.plot(perfil2, color="blue")
    plt.show()