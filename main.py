from threading import Thread
import tkinter as tk
from PIL import ImageTk
from PIL import Image
from tkinter import filedialog as fd 
import pyautogui
import cv2
import clipboard
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import imutils


window = tk.Tk()
window.config(bg="black")
window.title("Color_Detection")
window.geometry("900x500")
width=900
height=500
window_list = []
window.bind('<Escape>', lambda e: window.quit())

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
model = load_model("Output2.hdf5")


def show_camera():
    _,frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    image_copy = img.copy()
    image = image_copy.resize((width-200, height))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(image=photo)
    label.image=photo
    label.grid(row=0,column=3,rowspan = 8, columnspan = 9)
    label.after(5,show_camera)
    

def Capture(image):
    cv2.imsave(str(image), image)


def predict_smile():
    _,frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameClone = frame.copy()

    rects = detector.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5,
        minSize = (30, 30), flags = cv2.CASCADE_SCALE_IMAGE)

    #for (x, y, w, h) in rects:
    if(len(rects)!=0):
        x,y,w,h = rects[0]
        face = gray[y: y + h, x: x + w]
        face = cv2.resize(face, (64, 64))
        face = face.astype("float") / 255.0
        face = img_to_array(face)
        face = np.expand_dims(face, axis = 0)
        (notSmiling, smiling) = model.predict(face)[0]
        if smiling > notSmiling:
            label = "Smiling"
            side_image = Image.open("smile.jpg")
        else :
            label = "Not Smiling"
            side_image = Image.open("not_smile.jpeg")
        #Thread(target=show_result(label)).start()
        #show_result(label)
        #image_copy = side_image.copy()
        side_image = side_image.resize((100, 100))
        photo = ImageTk.PhotoImage(side_image)
        side_label = tk.Label(image=photo)
        side_label.image=photo
        side_label.grid(row=0, column=1, columnspan = 2, padx=50, pady=50)
        cv2.putText(frameClone, label, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.rectangle(frameClone, (x, y), (x + w, y + h),
            (0, 0, 255), 2)

    
        
    

    cv2image = cv2.cvtColor(frameClone, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    image_copy = img.copy()
    image = image_copy.resize((width-200, height))
    photo = ImageTk.PhotoImage(image)
    label = tk.Label(image=photo)
    label.image=photo
    label.grid(row=0,column=3,rowspan = 8, columnspan = 9)
    
    label.after(30,predict_smile)
    #capture_btn = tk.Button(window, text="Capture Button", width=25, activebackground="grey", activeforeground="blue",bg="purple", command=lambda:Capture(frameClone))
    #capture_btn.grid(row=3,column=1,columnspan=2, padx=10, pady=50)
    





def main():

    predict_smile()
    
    window.mainloop()



if __name__ == "__main__":
    main()    
