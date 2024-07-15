
import cv2
import tkinter as tk
from tkinter import Button, Label
from PIL import Image, ImageTk
import os

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

        self.btn_record = Button(window, text="Record", width=50, command=self.start_recording)
        self.btn_record.pack(anchor=tk.CENTER, expand=True)

        self.btn_stop = Button(window, text="Stop", width=50, command=self.stop_recording)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)

        self.recording = False
        self.out = None
        self.file_index = 0

        self.delay = 10
        self.update()

        self.window.mainloop()

    def start_recording(self):
        if not os.path.exists('videos'):
            os.makedirs('videos')
        while os.path.exists(f'videos/video{self.file_index}.avi'):
            self.file_index += 1
        self.recording = True
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        frame_size = (int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        self.out = cv2.VideoWriter(f'videos/video{self.file_index}.avi', fourcc, fps, frame_size)
        print(f'Recording started: videos/video{self.file_index}.avi')

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.out.release()
            self.out = None
            print(f'Recording stopped: videos/video{self.file_index}.avi')

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.flip(frame, 1)
            if self.recording:
                self.out.write(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(self.delay, self.update)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        if self.recording and self.out:
            self.out.release()

def main():
    root = tk.Tk()
    app = CameraApp(root, "Camera App")
    root.mainloop()

if __name__ == "__main__":
    main()
