import tensorflow as tf

from models import StyleContentModel
from neural_network import TrainModel 
from utils import load_img, tensor_to_image


# Define image locations and load the images
content_path = "../../assets/dog.jpg"
style_path = "../../assets/kandinsky.jpg"

content_image = load_img(content_path)
style_image = load_img(style_path)

print("Images loaded")


# Set layer parameters (Die sind jetzt aus dem Notebook kopiert)
content_layers = ['block5_conv2'] 

# Style layer we are interested in
style_layers = ['block1_conv1',
                'block2_conv1',
                'block3_conv1', 
                'block4_conv1', 
                'block5_conv1',
               ]

num_content_layers = len(content_layers)
num_style_layers = len(style_layers)

print("Layer parameters set")

# Load the model
model = StyleContentModel(style_layers, content_layers)

style_targets = model(style_image)['style']
content_targets = model(content_image)['content']

print("Model loaded")

# --- Training ---

image = tf.Variable(content_image)

trainer = TrainModel(model, image, (style_targets, content_targets), (num_style_layers, num_content_layers))
result = trainer.train()

# Save the result
file_name = 'stylized-image.png'
tensor_to_image(result).save(file_name)