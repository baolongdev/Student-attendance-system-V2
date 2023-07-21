import cv2
import av
import streamlit as st
from av import VideoFrame
from streamlit_webrtc import webrtc_streamer
from modules import *
import pandas as pd
import mediapipe as mp
import numpy as np
import cvzone
from PIL import Image, ImageDraw, ImageFont


class VideoProcessor:
    def __init__(self):
        self.fps = 0.0
        self.face_count = 0
        self.prevTime = cv2.getTickCount()
        self.fps_dataFrame = pd.DataFrame({'Time': [], 'FPS': []})
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection()
        self.font_path = get_from_control_reference("current_dir") / "assets" / "fonts" / "fontBe.ttf"
        self.detections = []
        
        
    def putText(self, img, text, position, textColor=(255, 255, 255), textSize=18):
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
       
        draw = ImageDraw.Draw(img)
        fontStyle = ImageFont.truetype(str(self.font_path), textSize, encoding="utf-8")
        
        draw.text(position, text, textColor, font=fontStyle)
        
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    
    
    def DrawFrame(self, frame, detection):
        if detection is None:
            return
        mode = get_from_control_reference("Face_detection")
        image = frame.copy()  # Make a copy of the frame to avoid modifying the original
        bbox = detection["bbox"]
        posX = bbox[0]
        posY = bbox[1]
        if self.checkFaceOutFrame(detection["detection"]):
            if mode == "face_detection":
                self.mp_draw.draw_detection(image, detection["detection"])
            elif mode == "default":
                image = cvzone.cornerRect(image, bbox, rt=0)
                text_position = (bbox[0], bbox[1] - 40)
                image = self.putText(image, "Lê Bảo Long", text_position)
        frame[:] = image

    def checkFaceOutFrame(self, detection):
        # khuôn mặt nằm ngoài khung hình:
        # False ngược lại True
        bbox = detection.location_data.relative_bounding_box
        xmin, ymin, width, height = bbox.xmin, bbox.ymin, bbox.width, bbox.height

        if xmin < 0 or \
            ymin < 0 or \
            xmin + width > 1 or \
            ymin + height > 1:
                return False
        
        return True
    
    def checkFace(self, frame, faceCurFrames):
        for faceCurFrame in faceCurFrames:
            self.DrawFrame(frame, faceCurFrame)
            # print(faceCurFrame)
        
        pass
    def detectFace(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(frame_rgb)
        self.face_count = 0
        self.detections = []
        if results.detections:
            ih, iw, _ = frame.shape
            for detection in results.detections:
                # Kiểm tra tọa độ khuôn mặt
                bboxC = detection.location_data.relative_bounding_box
                xmin, ymin, width, height = bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height
                left, top, right, bottom = int(xmin * iw), int(ymin * ih), \
                    int((xmin + width) * iw), int((ymin + height) * ih)
                bbox = int(xmin * iw), int(ymin * ih),\
                    int(width * iw), int(height * ih)
                self.detections.append({
                    "detection": detection,
                    "bbox": bbox,
                    "face_location": (top, right, bottom, left)
                })
                self.face_count += 1

        return self.detections
    
    def process_video(self, frame):
        faceCurFrame = self.detectFace(frame)    
        self.checkFace(frame, faceCurFrame)
        pass
        
    def process_frame(self, frame):
        currTime = cv2.getTickCount()
        time_diff = (currTime - self.prevTime) / cv2.getTickFrequency()
        self.fps = 1.0 / time_diff
        self.prevTime = currTime
        self.process_video(frame)


    def recv(self, frame: VideoFrame) -> VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        self.process_frame(img)
        return VideoFrame.from_ndarray(img, format="bgr24")

    def getFPS(self):
        return self.fps

    def getNewFPS_DataFrame(self):
        return pd.DataFrame({'Time': [pd.Timestamp.now().strftime('%H:%M:%S')],
                             'FPS': self.fps})

    def WidgetFPS(self, element):
        fps = self.getFPS()
        with element:
            st.text("FPS: {:.2f}".format(fps))
        pass

    def WidgetFaces(self, element):
        faces = self.face_count
        with element:
            st.text(f"Faces: {faces}")
        pass

    def WidgetTimeNow(self, element):
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%H:%M - %d/%m/%Y")
        with element:
            st.text(f"Thời gian: \n{dt_string}")
        pass
