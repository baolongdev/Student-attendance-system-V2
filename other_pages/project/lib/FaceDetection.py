import cv2
import streamlit as st
import mediapipe as mp
from other_pages.project.lib.Draw import *
from other_pages.project.lib.ProcessingImage import *

class FaceDetection(FaceDrawer):
    def __init__(self, frame = None):
        self.frame = frame
        self.face_count = 0
        self.check_anway= None
        
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection()
        
        self.detections = []
        self.check_anway = None
        self.prev_face_count = get_from_control_reference("prev_face_count")
        FaceDrawer.__init__(self, self.frame)
        
    def detectFace(self):
        if self.frame is None:
            return
        
        frame_rgb = ConvertBGR2RGB(self.frame)
        results = self.face_detection.process(frame_rgb)
        self.face_count = 0
        self.detections = []
        if results.detections:
            ih, iw, _ = self.frame.shape
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                xmin, ymin, width, height = bboxC.xmin, bboxC.ymin, bboxC.width, bboxC.height
                bbox = int(xmin * iw), int(ymin * ih),\
                    int(width * iw), int(height * ih)
                self.face_count += 1
                self.detections.append({
                    "detection": detection,
                    "bbox": bbox,
                })
        return self.detections
        
    def check_new_face_appeared(self):
        # Check if a new face has appeared in the current frame
        new_faces = self.face_count - self.prev_face_count
        if new_faces != 0:
            self.prev_face_count = self.face_count
            add_to_control_reference("prev_face_count", self.prev_face_count)
            return new_faces
        return 0
    
    def check_and_print_new_faces(self):
        delay = get_from_control_reference("time_checkFaceDetect")
        if delay > get_from_control_reference("time_delay_check_faces"):
            add_to_control_reference("time_delay_check_faces",  get_from_control_reference("time_delay_check_faces")+1)
            data = self.check_new_face_appeared()
            if data:
                self.check_anway = data
                return self.check_anway
            else:
                self.check_anway = None
                return self.check_anway
        
        
    def get_faces(self, element):
        faces = self.face_count
        with element:
            st.text(f"Faces: {faces}")
        pass
    
    def get_image_face_detect(self, mainframe):
        detections = self.detections
        if detections:
            return crop_face(mainframe, detections[0]["bbox"])
        else:
            return None