
import skimage as ski
import numpy as np
import matplotlib.pyplot as plt

class ImageProcessor:
    def __init__(self, image, color=False, hsv=False):
        self.img_original = ski.io.imread(image)
        if hsv:
            self.hsv = hsv
            self.img_original = ski.color.rgb2hsv(self.img_original)
        self.h_orig, self.c_orig = ski.exposure.histogram(self.img_original)
        self.img_real = ski.util.img_as_float(self.img_original) * 255
        self.color = color

    def aclarado(self, n=1.0):
        if self.color:
            # Código existente para RGB
            centros_color, plano_rojo, histo_rojo, plano_verde, histo_verde, plano_azul, histo_azul = self.histograma_color()
            img_clara = np.zeros_like(self.img_original)

            # Procesar cada plano individualmente
            plano_claro_r = np.power(plano_rojo / 255, 1 / n) * 255
            plano_claro_g = np.power(plano_verde / 255, 1 / n) * 255
            plano_claro_b = np.power(plano_azul / 255, 1 / n) * 255

            img_clara[:, :, 0] = plano_claro_r
            img_clara[:, :, 1] = plano_claro_g
            img_clara[:, :, 2] = plano_claro_b

            img_clara = ski.util.img_as_ubyte(img_clara / 255)

            h_clara = []
            c_clara = []
            for i in range(3):
                h, c = ski.exposure.histogram(img_clara[:, :, i])
                h_clara.append(h)
                c_clara.append(c)

            return img_clara, h_clara, c_clara
        elif hasattr(self, 'hsv') and self.hsv:
            # Procesamiento para HSV (aplicar solo al canal V)
            v_canal = self.img_original
            img_clara = np.power(v_canal, 1.0 / n)
            img_clara = ski.util.img_as_ubyte(img_clara)
            h_clara, c_clara = ski.exposure.histogram(img_clara)
            return img_clara, h_clara, c_clara
        else:
            # Código existente para escala de grises
            img_clara = np.power(self.img_original / 255, 1 / n) * 255
            img_clara = ski.util.img_as_ubyte(img_clara / 255)
            h_clara, c_clara = ski.exposure.histogram(img_clara)
            return img_clara, h_clara, c_clara

    def oscurecer(self, n=2.0):
        if self.color:
            # Código existente para RGB
            centros_color, plano_rojo, histo_rojo, plano_verde, histo_verde, plano_azul, histo_azul = self.histograma_color()
            img_oscura = np.zeros_like(self.img_original)

            # Procesar cada plano individualmente
            plano_oscuro_r = np.power(plano_rojo / 255, n) * 255
            plano_oscuro_g = np.power(plano_verde / 255, n) * 255
            plano_oscuro_b = np.power(plano_azul / 255, n) * 255

            img_oscura[:, :, 0] = plano_oscuro_r
            img_oscura[:, :, 1] = plano_oscuro_g
            img_oscura[:, :, 2] = plano_oscuro_b

            img_oscura = ski.util.img_as_ubyte(img_oscura / 255)

            h_oscura = []
            c_oscura = []
            for i in range(3):
                h, c = ski.exposure.histogram(img_oscura[:, :, i])
                h_oscura.append(h)
                c_oscura.append(c)

            return img_oscura, h_oscura, c_oscura
        elif hasattr(self, 'hsv') and self.hsv:
            # Procesamiento para HSV (aplicar solo al canal V)
            v_canal = self.img_original
            img_oscura = np.power(v_canal, n)
            img_oscura = ski.util.img_as_ubyte(img_oscura)
            h_oscura, c_oscura = ski.exposure.histogram(img_oscura)
            return img_oscura, h_oscura, c_oscura
        else:
            # Código existente para escala de grises
            img_oscura = np.power(self.img_original / 255, n) * 255
            img_oscura = ski.util.img_as_ubyte(img_oscura / 255)
            h_oscura, c_oscura = ski.exposure.histogram(img_oscura)
            return img_oscura, h_oscura, c_oscura

    def invertida(self):
        if self.color:
            # Código existente para RGB
            centros_color, plano_rojo, histo_rojo, plano_verde, histo_verde, plano_azul, histo_azul = self.histograma_color()
            img_inv = np.zeros_like(self.img_original)

            # Invertir cada plano individualmente
            img_inv[:, :, 0] = 255 - plano_rojo
            img_inv[:, :, 1] = 255 - plano_verde
            img_inv[:, :, 2] = 255 - plano_azul

            h_inv = []
            c_inv = []
            for i in range(3):
                h, c = ski.exposure.histogram(img_inv[:, :, i])
                h_inv.append(h)
                c_inv.append(c)

            return img_inv, h_inv, c_inv
        elif hasattr(self, 'hsv') and self.hsv:
            # Procesamiento para HSV (aplicar solo al canal V)
            v_canal = self.img_original
            img_inv = 1 - v_canal
            img_inv = ski.util.img_as_ubyte(img_inv)
            h_inv, c_inv = ski.exposure.histogram(img_inv)
            return img_inv, h_inv, c_inv
        else:
            # Código existente para escala de grises
            img_inv = 255 - self.img_original
            h_inv, c_inv = ski.exposure.histogram(img_inv)
            return img_inv, h_inv, c_inv

    def ecualizada(self):
        if self.color:
            # Código existente para RGB
            centros_color, plano_rojo, histo_rojo, plano_verde, histo_verde, plano_azul, histo_azul = self.histograma_color()
            img_eq = []
            h_eq, c_eq = [], []

            # Ecualizar cada plano
            for i, plano in enumerate([plano_rojo, plano_verde, plano_azul]):
                img_eq.append(ski.util.img_as_ubyte(ski.exposure.equalize_hist(plano)))
                h, c = ski.exposure.histogram(img_eq[i])
                h_eq.append(h)
                c_eq.append(c)

            # Combinar los tres canales en una imagen a color
            img_combinada = np.zeros_like(self.img_original)
            img_combinada[:, :, 0] = img_eq[0]
            img_combinada[:, :, 1] = img_eq[1]
            img_combinada[:, :, 2] = img_eq[2]

            return img_combinada, h_eq, c_eq
        elif hasattr(self, 'hsv') and self.hsv:
            # Procesamiento para HSV (aplicar solo al canal V)
            v_canal = self.img_original
            v_eq = ski.util.img_as_ubyte(ski.exposure.equalize_hist(v_canal))
            h_eq, c_eq = ski.exposure.histogram(v_eq)
            return v_eq, h_eq, c_eq
        else:
            # Código existente para escala de grises
            img_eq = ski.exposure.equalize_hist(self.img_original)
            img_eq = ski.util.img_as_ubyte(img_eq)
            h_eq, c_eq = ski.exposure.histogram(img_eq)
            return img_eq, h_eq, c_eq

    def ecualizada_adaptativa(self, kernel_size=None, clip_limit=1.0, nbins=256):
        if self.color:
            # Código existente para RGB
            centros_color, plano_rojo, histo_rojo, plano_verde, histo_verde, plano_azul, histo_azul = self.histograma_color()
            img_eq_adapt = []
            h_eq_adapt, c_eq_adapt = [], []

            for i, plano in enumerate([plano_rojo, plano_verde, plano_azul]):
                img_eq_adapt.append(ski.util.img_as_ubyte(ski.exposure.equalize_adapthist(plano,
                                                                                          kernel_size=kernel_size,
                                                                                          clip_limit=clip_limit,
                                                                                          nbins=nbins)))
                h, c = ski.exposure.histogram(img_eq_adapt[i])
                h_eq_adapt.append(h)
                c_eq_adapt.append(c)

            img_combinada = np.zeros_like(self.img_original)
            img_combinada[:, :, 0] = img_eq_adapt[0]
            img_combinada[:, :, 1] = img_eq_adapt[1]
            img_combinada[:, :, 2] = img_eq_adapt[2]

            return img_combinada, h_eq_adapt, c_eq_adapt
        elif hasattr(self, 'hsv') and self.hsv:
            # Procesamiento para HSV (aplicar solo al canal V)
            v_canal = self.img_original
            v_eq = ski.util.img_as_ubyte(ski.exposure.equalize_adapthist(v_canal,
                                                                         kernel_size=kernel_size, clip_limit=clip_limit,
                                                                         nbins=nbins))
            h_eq, c_eq = ski.exposure.histogram(v_eq)
            return v_eq, h_eq, c_eq
        else:
            # Código existente para escala de grises
            img_eq_adapt = ski.exposure.equalize_adapthist(self.img_original, kernel_size=kernel_size,
                                                           clip_limit=clip_limit, nbins=nbins)
            img_eq_adapt = ski.util.img_as_ubyte(img_eq_adapt)
            h_eq_adapt, c_eq_adapt = ski.exposure.histogram(img_eq_adapt)
            return img_eq_adapt, h_eq_adapt, c_eq_adapt

    def clahe(self, kernel_size=None, clip_limit=0.01, nbins=256):
        if self.color:
            # Código existente para RGB
            centros_color, plano_rojo, histo_rojo, plano_verde, histo_verde, plano_azul, histo_azul = self.histograma_color()
            img_eq_CLAHE = []
            h_eq_CLAHE, c_eq_CLAHE = [], []

            for i, plano in enumerate([plano_rojo, plano_verde, plano_azul]):
                img_eq_CLAHE.append(ski.util.img_as_ubyte(ski.exposure.equalize_adapthist(plano,
                                                                                          kernel_size=kernel_size,
                                                                                          clip_limit=clip_limit,
                                                                                          nbins=nbins)))
                h, c = ski.exposure.histogram(img_eq_CLAHE[i])
                h_eq_CLAHE.append(h)
                c_eq_CLAHE.append(c)

            img_combinada = np.zeros_like(self.img_original)
            img_combinada[:, :, 0] = img_eq_CLAHE[0]
            img_combinada[:, :, 1] = img_eq_CLAHE[1]
            img_combinada[:, :, 2] = img_eq_CLAHE[2]

            return img_combinada, h_eq_CLAHE, c_eq_CLAHE
        elif hasattr(self, 'hsv') and self.hsv:
            # Procesamiento para HSV (aplicar solo al canal V)
            v_canal = self.img_original
            v_eq = ski.util.img_as_ubyte(ski.exposure.equalize_adapthist(v_canal,
                                                                         kernel_size=kernel_size, clip_limit=clip_limit,
                                                                         nbins=nbins))
            h_eq, c_eq = ski.exposure.histogram(v_eq)
            return v_eq, h_eq, c_eq
        else:
            # Código existente para escala de grises
            img_eq_CLAHE = ski.exposure.equalize_adapthist(self.img_original, kernel_size=kernel_size,
                                                           clip_limit=clip_limit, nbins=nbins)
            img_eq_CLAHE = ski.util.img_as_ubyte(img_eq_CLAHE)
            h_eq_CLAHE, c_eq_CLAHE = ski.exposure.histogram(img_eq_CLAHE)
            return img_eq_CLAHE, h_eq_CLAHE, c_eq_CLAHE

    def histograma_color(self):
        if self.hsv:
            self.img_original = ski.color.hsv2rgb(self.img_original)
        h_color, centros_color = ski.exposure.histogram(self.img_original, channel_axis=-1)
        plano_rojo = self.img_original[:, :, 0]
        histo_rojo = h_color[0, :]

        plano_verde = self.img_original[:, :, 1]
        histo_verde = h_color[1, :]

        plano_azul = self.img_original[:, :, 2]
        histo_azul = h_color[2, :]

        return [centros_color, plano_rojo, histo_rojo, plano_verde, histo_verde, plano_azul, histo_azul]

    def plano_pca(self):
        img = ski.util.img_as_float(self.img_original)
        forma_inicial = img.shape
        imagen_por_pixeles = np.reshape(self.img_original, (forma_inicial[0] * forma_inicial[1], forma_inicial[2])).transpose()
        cov_matrix = np.cov(imagen_por_pixeles)
        U, S, V = np.linalg.svd(cov_matrix)
        y = U.transpose() @ imagen_por_pixeles
        y = y.transpose().reshape(forma_inicial)
        pca = (y - y.min()) / (y.max() - y.min())
        print("Valores propios:", S)
        return pca
