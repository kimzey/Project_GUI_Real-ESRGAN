import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import subprocess
import os
import cv2
cropping = False

def upload_files():
    global img,folder_path,crop_img
    files_path = filedialog.askopenfilename()

    l3 = tk.Label(canvas,text='INPUT ',width=30,font=my_font1)
    l3.grid(row=1,column=2)

    crop_img = cv2.resize(cv2.imread(files_path),(900,900))
    img = Image.open(files_path)
    img = img.resize((300,300))
    img = ImageTk.PhotoImage(img)
    show_img = tk.Label(canvas,image=img)
    show_img.grid(row=2,column=2)

    cv2.imshow("image", crop_img)
    cv2.setMouseCallback("image", mouse_crop,crop_img)

def mouse_crop(event, x, y, flags, img):
    global x_start, y_start, x_end, y_end, cropping,img_crop
    # print("x",x)
    # print("y",y)
    img_copy = img.copy()
    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        save_img_crop = img[y_start:y_end, x_start:x_end]
        save_path = "./crop/crop.png"
        cv2.imwrite(save_path, save_img_crop)
        showimg_crop(save_path)
    if cropping  :
        cv2.rectangle(img_copy, (x_start, y_start), (x_end, y_end), (255, 0, 0), 1)
        cv2.imshow("image", img_copy)
        # cv2.imshow("img1", roi)

def showimg_crop(path):
    global img_crop
    text_img2 = tk.Label(canvas,text='showimg_crop ',width=30,font=my_font1)
    text_img2.grid(row=3,column=2)

    img_crop = Image.open(path)
    # print(img)
    img_crop = img_crop.resize((300,300))
    img_crop = ImageTk.PhotoImage(img_crop)
    show_img2 = tk.Label(canvas,image=img_crop)
    show_img2.grid(row=4,column=2)

    b2 = tk.Button(canvas, text='Process',
    width=20,command = lambda:process_img(path))
    b2.grid(row=2,column=3)

def process_img(path):

    reslut = subprocess.run(["python", "inference_realesrgan.py", "-n" ,"RealESRGAN_x4plus", "-i",path, "--face_enhance" ,"--fp32"],
                    capture_output=True,text=True)
    print(path)
    path_output = "./results"
    files = os.listdir(path_output)

    global output_img
    text_img2 = tk.Label(canvas,text='output_img ',width=30,font=my_font1)
    text_img2.grid(row=3,column=3)

    print(path_output+"/"+files[0])
    output_img = Image.open(path_output+"/"+files[0])
    # print(img)
    output_img = output_img.resize((300,300))
    output_img = ImageTk.PhotoImage(output_img)
    show_img2 = tk.Label(canvas,image=output_img)
    show_img2.grid(row=4,column=3)

canvas = tk.Tk()
canvas.geometry('1600x800')

canvas.title('DMT330')
my_font1=('times', 18, 'bold')

l2 = tk.Label(canvas,text='IMG PROCESS ',width=30,font=my_font1)
l2.grid(row=1,column=1)

b1 = tk.Button(canvas, text='Upload_file',
   width=20,command = lambda:upload_files())
b1.grid(row=2,column=1)

canvas.mainloop()