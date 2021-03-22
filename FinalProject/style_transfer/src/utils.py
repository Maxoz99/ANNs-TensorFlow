import PIL.Image
import numpy as np
import tensorflow as tf
import os


def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def img_prop_resize(image, height):
    """Resize a PIL image to height while preserving the aspect ratio"""
    height_percent = height / image.size[1]
    width_size = int(image.size[0] * height_percent)
    image = image.resize((width_size, height), PIL.Image.NEAREST)
    return image


def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


def gram_matrix(input_tensor):
    channels = int(input_tensor.shape[-1])
    a = tf.reshape(input_tensor, [-1, channels])
    n = tf.shape(a)[0]
    gram = tf.matmul(a, a, transpose_a=True)
    return gram / tf.cast(n, tf.float32)


def calculate_content_style_weights(factor):
    """Adjust the weight according to the presented ratio"""
    content_weight = 1 - factor
    style_weight = factor
    return content_weight, style_weight


def save_img(img, filename):
    tensor_to_image(img).save(filename)


def create_dir(path):
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
    else:
        print("Path already exists.")