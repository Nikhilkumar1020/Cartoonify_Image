import cv2  # for image processing
import easygui  # to open the filebox
import numpy as np  # to store image
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import Button, Label

# Create the main window
top = tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image!')
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))
label.pack(pady=20)

def upload():
    ImagePath = easygui.fileopenbox()
    if ImagePath:  # Check if a file was selected
        cartoonify(ImagePath)

def cartoonify(ImagePath):
    # Read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    # Confirm that image is chosen
    if originalmage is None:
        print("Cannot find any image. Choose an appropriate file.")
        return

    # Resize the image for consistent processing
    ReSized1 = cv2.resize(originalmage, (960, 540))

    # Converting an image to grayscale
    grayScaleImage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    ReSized2 = cv2.resize(grayScaleImage, (960, 540))

    # Applying median blur to smoothen the grayscale image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 7)  # Increased kernel size for more smoothing
    ReSized3 = cv2.resize(smoothGrayScale, (960, 540))

    # Retrieving the edges for cartoon effect
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255,
                                     cv2.ADAPTIVE_THRESH_MEAN_C,
                                     cv2.THRESH_BINARY, 11, 11)  # Adjusted parameters for better edge detection
    ReSized4 = cv2.resize(getEdge, (960, 540))

    # Applying bilateral filter to remove noise and keep edge sharp
    colorImage = cv2.bilateralFilter(originalmage, 15, 300, 300)  # Increased parameters for more smoothing
    ReSized5 = cv2.resize(colorImage, (960, 540))

    # Masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)
    ReSized6 = cv2.resize(cartoonImage, (960, 540))

    # Enhance colors (optional)
    cartoonImage = cv2.cvtColor(cartoonImage, cv2.COLOR_RGB2HSV)  # Convert to HSV
    cartoonImage[..., 1] = np.clip(cartoonImage[..., 1] * 1.5, 0, 255)  # Increase saturation
    cartoonImage = cv2.cvtColor(cartoonImage, cv2.COLOR_HSV2RGB)  # Convert back to RGB

    # Plotting the whole transition
    images = [ReSized1, ReSized2, ReSized3, ReSized4, ReSized5, ReSized6]

    fig, axes = plt.subplots(3, 2, figsize=(8, 8), subplot_kw={'xticks': [], 'yticks': []}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i])
        ax.set_title(['Original', 'Grayscale', 'Smooth', 'Edges', 'Color', 'Cartoon'][i])
        ax.axis('off')

    save1 = Button(top, text="Save cartoon image", command=lambda: save(cartoonImage, ImagePath), padx=30, pady=5)
    save1.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
    save1.pack(side=tk.TOP, pady=50)

    plt.show()

def save(cartoonImage, ImagePath):
    # Saving an image using imwrite()
    newName = "cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension = os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName + extension)
    cv2.imwrite(path, cv2.cvtColor(cartoonImage, cv2.COLOR_RGB2BGR))
    I = "Image saved by name " + newName + " at " + path
    messagebox.showinfo(title=None, message=I)

upload_button = Button(top, text="Cartoonify an Image", command=upload, padx=10, pady=5)
upload_button.configure(background='#364156', foreground='white', font=('calibri', 10, 'bold'))
upload_button.pack(side=tk.TOP, pady=50)

top.mainloop()