import tkinter as tk
from tkinter import ttk

from tkinter import filedialog as fd
from PIL import ImageTk, Image

class ImageWindow(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        
        self.text = tk.StringVar()
        self.label = ttk.Label(parent, text="Image Window")
        self.label.pack(side="left", expand=True)

    def set_text(self, text):
        self.label.config(text=text)

    def set_image(self, path):
        """Displays an image in the frame"""
        img = ImageTk.PhotoImage(image=Image.open(path))
        self.label.configure(image=img)
        self.label.image = img


class Footer(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.parent = parent
        self.btn_select_style_img = ttk.Button(
            parent,
            text="Select a style image",
            command=self.select_style_img)

        self.btn_select_content_img = ttk.Button(
            parent,
            text="Select a content image",
            command=self.select_content_img)

        self.btn_apply_style = ttk.Button(
            parent,
            text="Transfer Style",
            command=self.parent.apply_style)

        self.slider_ratio = ttk.Scale(
            parent,
            from_=0,
            to=1,
            command=self.parent.update_style_ratio,
            length = 300,
            orient="horizontal",
        )

        content_label = ttk.Label(parent, text="Content")
        style_label = ttk.Label(parent, text="Style")

        self.btn_select_content_img.pack(side="left", ipadx=15, padx=10)
        self.btn_select_style_img.pack(side="left", ipadx=15, padx=20)
        content_label.pack(side="left")
        self.slider_ratio.pack(side="left", padx=20)
        style_label.pack(side="left")
        self.btn_apply_style.pack(side="right", ipadx=15, padx=20)

    def select_content_img(self):
        img = select_image()
        if img:
            self.parent.content_path = img
            self.parent.update_image("content")

    def select_style_img(self):
        img = select_image()
        if img:
            self.parent.style_path = img
            self.parent.update_image("style")


def select_image():
    """Opens a file dialog to pick an image and uses this path to access the image for training and display"""
    img_path = fd.askopenfilename(
        title="Select an Image",
        filetypes=(("image files","*.jpg"),("All files","*.*")),
        initialdir="../../assets"
    )
    if img_path:
        return img_path