import tkinter as tk
from tkinter import Label, filedialog
from PIL import ImageTk, Image

content_style_ratio = 0.5

def open_image():
    img_path = filedialog.askopenfilename(filetypes=(("image files","*.jpg"),("All files","*.*")))
    if len(img_path) < 1:
        return

    img = Image.open(img_path)
    img = img.resize((200,200), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(img)
    return render

def get_content_image():
    content_image = open_image()
    display_image = Label(frame_content, image=content_image)
    display_image.pack(fill=tk.BOTH)

def get_style_image():
    style_image = open_image()
    display_image = Label(frame_style, image=style_image)
    display_image.pack(fill=tk.BOTH)

def set_content_style_ratio(v):
    content_style_ratio = v


window = tk.Tk()
window.title("Artistic Style Transfer")

frame_main = tk.Frame(master=window)
frame_main.pack(fill=tk.BOTH)

frame_content = tk.Frame(master=frame_main, bg="yellow", width=200, height=200)
frame_content.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame_style = tk.Frame(master=frame_main, bg="red", width=200, height=200)
frame_style.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame_setup = tk.Frame(master=window, bg="blue", height=50)
frame_setup.pack(fill=tk.BOTH, side=tk.BOTTOM)

slider_content_style = tk.Scale(frame_setup, from_=0, to=100, label="Content-Scale-Ratio", orient=tk.HORIZONTAL, command=content_style_ratio)
slider_content_style.set(content_style_ratio)
slider_content_style.pack()

btn_convert = tk.Button(
    master=frame_setup,
    text="Transfer Styles",
    width=25,
    height=5,
    bg="gray",
    fg="white",
)
btn_convert.pack(side=tk.RIGHT)

btn_open_content = tk.Button(
    master=frame_setup,
    text="Select Content Image",
    command=get_content_image,
    width=25,
    height=4,
    bg="gray",
    fg="white",
)
btn_open_content.pack(side=tk.LEFT)

btn_open_style = tk.Button(
    master=frame_setup,
    text="Select Style Image",
    command=get_style_image,
    width=25,   
    height=4,
    bg="gray",
    fg="white",
)
btn_open_style.pack(side=tk.LEFT)


window.mainloop()

