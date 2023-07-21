import cv2
import streamlit as st
from av import VideoFrame
from other_pages.project.lib.Draw import *
from other_pages.project.lib.FaceDetection import *
from other_pages.project.lib.FaceRecognition import *

class VideoReader(FaceDetection, FaceRecognition):
    def __init__(self) -> None:
        self.fps = 0.0
        self.prevTime = cv2.getTickCount()
        self.frame = None        
        FaceDetection.__init__(self, self.frame)
        FaceRecognition.__init__(self)

    def calculate_frame_rate(self):
        currTime = cv2.getTickCount()
        time_diff = (currTime - self.prevTime) / cv2.getTickFrequency()
        self.fps = 1.0 / time_diff
        self.prevTime = currTime

    
    def Drawface(self):
        detections = self.detections
        for detection in detections:
            if self.check_face_out_frame(detection["detection"]):
                data = self.FaceRecognition_Processing(crop_face(self.frame, detection["bbox"]))
                self.draw(detection, data)
            
    
    
    def recv(self, frame: VideoFrame) -> VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.mainframe = img
        self.frame = img
        self.calculate_frame_rate()            
        self.detectFace()
        self.Drawface()
                
        return VideoFrame.from_ndarray(img, format="bgr24")

    def get_frame(self):
        return VideoFrame.from_ndarray(self.frame, format="bgr24")
    def get_frame_rate(self, element):
        fps = self.fps
        with element:
            st.text("FPS: {:.2f}".format(fps))

    def get_TimeNow(self, element):
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%H:%M - %d/%m/%Y")
        with element:
            st.text(f"Thời gian: \n{dt_string}")
