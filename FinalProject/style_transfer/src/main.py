import tensorflow as tf
import tkinter as tk
import time

from models import StyleContentModel
from neural_network import TrainModel 
from gui import ImageWindow, Footer, PopoutImage
from utils import load_img, save_img, calculate_content_style_weights, create_dir

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Style Transfer Application")
        self.geometry("%dx%d+0+0" % self.maxsize())
        self.minsize(700,400)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.content_path = ""
        self.style_path = ""
        self.content_style_ratio = 0

        self.content_frame = ImageWindow(container)
        self.content_frame.set_text("Select a content image!")
        self.content_frame.pack()

        self.style_frame = ImageWindow(container)
        self.style_frame.set_text("Select a style image!")
        self.style_frame.pack()

        self.footer = Footer(self)

        self.footer.pack(side="bottom", fill="x", pady=75, padx=50)

    def update_image(self, type):
        if type == "content":
            self.content_frame.set_image(self.content_path)
        elif type == "style":
            self.style_frame.set_image(self.style_path)

    def update_style_ratio(self, value):
        self.content_style_ratio = float(value)

    def apply_style(self):

        self.popout_window = PopoutImage()

        start_time = time.time()

        print("Preparing images")
        content_image = load_img(self.content_path)
        style_image = load_img(self.style_path)

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

        create_dir("tmp")

        image = tf.Variable(content_image)

        trainer = TrainModel(model, image, (style_targets, content_targets), (num_style_layers, num_content_layers))

        content_weight, style_weight = calculate_content_style_weights(self.content_style_ratio)
        trainer.set_content_style_ratio(content_weight, style_weight)

        print(f"Content weight: {content_weight}")

        result = trainer.train()
        save_img(result, "tmp/styled_image.png")
        end_time = time.time()
        print(f"Application finished in: {end_time-start_time:.1f}")

        self.popout_window.image_frame.set_image("tmp/styled_image.png")

if __name__ == "__main__":
    app = Application()
    app.mainloop()