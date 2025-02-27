import skimage as ski
import matplotlib.pyplot as plt

# Reescribir el codigo para que sea una funcion que cumpla con las siguientes especificaciones:
# - La funcion ejecutara las transformaciones afines que ya se han descrito.
# - Debe tener un argumento que por default sea False, que si esta True, mostrara las imagenes intermedias.
# - La funcion debe devolver la imagen final.

def rotar_imagen(img, n_grados, mostrar_intermedias=False):
    if mostrar_intermedias:
        fig, axs = plt.subplots(1, 5, layout="constrained")
    else:
        fig, axs = plt.subplots(1, 1, layout="constrained")
    # Trasladar el centro de la imagen hasta la posición (0, 0).
    transf_despl_1 = ski.transform.AffineTransform(translation=(-img.shape[0] // 2, -img.shape[1] // 2))
    matriz_rotacion = ski.transform.AffineTransform(rotation=-n_grados)
    transf_despl_2 = ski.transform.AffineTransform(translation=(img.shape[0] // 2, img.shape[1] // 2))
    transf_final = ski.transform.AffineTransform(
        (transf_despl_2.params @ matriz_rotacion.params @ transf_despl_1.params))
    imagen_final = ski.transform.warp(img, transf_final.inverse)

    if mostrar_intermedias:
        transf_despl_1_img = ski.transform.warp(img, transf_despl_1.inverse)
        img_girada = ski.transform.warp(img, matriz_rotacion.inverse)
        transf_despl_2_img = ski.transform.warp(img_girada, transf_despl_2.inverse)

        axs[0].imshow(img, cmap=plt.cm.gray)
        axs[0].set_title("Original")
        axs[1].imshow(transf_despl_1_img, cmap=plt.cm.gray)
        axs[1].set_title("Traslación")
        axs[2].imshow(img_girada, cmap=plt.cm.gray)
        axs[2].set_title("Rotada")
        axs[3].imshow(transf_despl_2_img, cmap=plt.cm.gray)
        axs[3].set_title("Traslación 2")
        axs[4].imshow(imagen_final, cmap=plt.cm.gray)
        axs[4].set_title("Funcion afin")
    else:
        axs.imshow(imagen_final, cmap=plt.cm.gray)
        axs.set_title("Funcion afin")

    plt.show()
    return imagen_final

if __name__ == "__main__":
    img_original = ski.io.imread("images/lena256.pgm")
    n_grados = 0.7853981633974483  # 45 grados en radianes
    img_final = rotar_imagen(img_original, n_grados, mostrar_intermedias=True)

    # Comparar resultado con el de la funcion de skimage
    img_girada = ski.transform.rotate(img_original, 45, center=(img_original.shape[0] // 2, img_original.shape[1] // 2), resize=False, order=3)

    fig, axs = plt.subplots(1, 2, layout="constrained")
    axs[0].imshow(img_final, cmap=plt.cm.gray)
    axs[0].set_title("Funcion propia")
    axs[1].imshow(img_girada,cmap=plt.cm.gray)
    axs[1].set_title("Funcion rotate")
    plt.show()
