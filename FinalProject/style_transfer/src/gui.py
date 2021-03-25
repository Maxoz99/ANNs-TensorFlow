import tkinter as tk
from tkinter import ttk

from tkinter import filedialog as fd
from PIL import ImageTk, Image
from shutil import copyfile
from sys import exc_info

from utils import img_prop_resize


class ImageWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.text = tk.StringVar()
        self.label = ttk.Label(parent, text="Image Window")
        self.label.pack(side="left", expand=True)

    def set_text(self, text):
        self.label.config(text=text)

    def set_image(self, path):
        """Displays an image in the frame"""
        raw_img = Image.open(path)
        resized_img = img_prop_resize(raw_img, int(self.winfo_screenheight() / 2))
        img = ImageTk.PhotoImage(resized_img)
        self.label.configure(image=img)
        self.label.image = img


class Footer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Image selection

        btn_select_style_img = ttk.Button(
            parent,
            text="Select a style image",
            command=self.select_style_img)

        btn_select_content_img = ttk.Button(
            parent,
            text="Select a content image",
            command=self.select_content_img)

        # Button to start the transfer

        btn_apply_style = ttk.Button(
            parent,
            text="Transfer Style",
            command=self.parent.apply_style)

        # Options for the content style weight

        style_content_frame = ttk.Labelframe(parent, text="Content vs. Style")

        slider_ratio = ttk.Scale(
            style_content_frame,
            from_=5,
            to=-5,
            command=self.parent.update_style_ratio,
            length = 300,
            orient="horizontal",
        )

        content_label = ttk.Label(style_content_frame, text="Content")
        style_label = ttk.Label(style_content_frame, text="Style")

        content_label.grid(column=0, row=0, padx=5, ipady=5)
        slider_ratio.grid(column=1, row=0, padx=10, ipady=5)
        style_label.grid(column=2, row=0, ipady=5)

        # Options for quality parameters
        self.epochs = tk.IntVar(value=10)
        self.steps = tk.IntVar(value=100)
        self.total_variation = tk.IntVar(value=30)

        quality_frame = ttk.Labelframe(parent, text="Quality")

        epoch_label = ttk.Label(quality_frame, text="Epochs:")
        epoch_entry = ttk.Entry(quality_frame, textvariable=self.epochs, width=10)
        steps_label = ttk.Label(quality_frame, text="Steps per epoch:")
        steps_entry = ttk.Entry(quality_frame, textvariable=self.steps, width=10)
        variation_label = ttk.Label(quality_frame, text="Total Variation:")
        variation_entry = ttk.Entry(quality_frame, textvariable=self.total_variation, width=10)

        epoch_label.grid(column=0, row=0, ipadx=10, ipady=5)
        epoch_entry.grid(column=0, row=1, ipadx=10, ipady=5)
        steps_label.grid(column=1, row=0, ipadx=10, ipady=5)
        steps_entry.grid(column=1, row=1, ipadx=10, ipady=5)
        variation_label.grid(column=2, row=0, ipadx=10, ipady=5)
        variation_entry.grid(column=2, row=1, ipadx=10, ipady=5)

        # Packing the footer

        btn_select_content_img.pack(side="left", ipadx=15, padx=10)
        btn_select_style_img.pack(side="left", ipadx=15, padx=20)
        style_content_frame.pack(side="left", padx=20, ipadx=10, ipady=5)
        quality_frame.pack(side="left", padx=20, ipadx=10)
        btn_apply_style.pack(side="right", ipadx=15, padx=20)

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


class PopoutImage(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.image_frame = ImageWindow(self)
        self.geometry("600x600+100+100")
        # The text does not show at the moment because the gui is not threaded
        self.image_frame.set_text("Applying style...please wait")
        self.image_frame.pack()
        btn_save = ttk.Button(self, text="Save Image", command=select_save_loc)
        btn_save.pack()


def select_image():
    """Open a file dialog to pick an image and use this path to access the image for training and display"""
    img_path = fd.askopenfilename(
        title="Select an Image",
        filetypes=(("image files","*.jpg"),("All files","*.*")),
        initialdir="../assets"
    )
    if img_path:
        return img_path


def select_save_loc():
    """Select a filename and location and copy the generated image to this location"""
    savepath = fd.asksaveasfilename(
        title="Select save location",
        filetypes=(("image files","*.png"),("All files","*.*")),
    )
    
    if savepath:
        try:
            copyfile(src="tmp/styled_image.png", dst=savepath)
        except :
            print(f"Error {exc_info()[0]}")