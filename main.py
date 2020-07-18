
import tkinter as tk
from PIL import ImageTk
from PIL import Image
from tkinter import filedialog as fd 
import pyautogui
import cv2
import clipboard


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
    




def main():
    
    
    show_camera()


    load_btn = tk.Button(window, text="Show Icon", width=25, activebackground="grey", activeforeground="blue",bg="purple", command=lambda:Upload())
    load_btn.grid(row=0,column=1,columnspan=2, padx=10, pady=50)
    window.mainloop()



if __name__ == "__main__":
    main()    
