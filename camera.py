import cv2
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import os
#pip install opencv-python-headless opencv-python Pillow
class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.video_source = 0
        
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)
        
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tk.CENTER, expand=True)

        self.delay = 10
        self.update()

        self.window.mainloop()

    def snapshot(self):
        if not os.path.exists('photos'):
            os.makedirs('photos')
        i = 0
        while os.path.exists(f'photos/{i}.jpg'):
            i += 1
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            cv2.imwrite(f'photos/{i}.jpg', frame)
            print(f'Photo saved as photos/{i}.jpg')

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def main():
    root = tk.Tk()
    app = CameraApp(root, "Camera App")
    root.mainloop()

if __name__ == "__main__":
    main()

