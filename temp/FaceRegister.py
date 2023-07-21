import cv2
import math
import pickle
import streamlit as st
import face_recognition
from concurrent.futures import ThreadPoolExecutor
from other_pages.project.lib.FaceDetection import *
import time

class FaceRegister(FaceDetection):
    def __init__(self):
        FaceDetection.__init__(self)
        self.modelFile = get_from_control_reference("current_dir") / "assets" / "models" / "models.p"
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_file()
    def load_file(self):
        print("Loading file")
        try:
            with open(self.modelFile, 'rb') as file:
                encode_list_known_with_ids = pickle.load(file)
                if encode_list_known_with_ids:
                    self.known_face_encodings, self.known_face_names = map(list, zip(*encode_list_known_with_ids))
                    # print(self.known_face_encodings, self.known_face_names)
                else:
                    self.known_face_encodings = []
                    self.known_face_names = []
            print("Encode File Loaded")
        except FileNotFoundError:
            print("No pre-existing Encode File found. Creating an empty one.")
            self.known_face_encodings = []
            self.known_face_names = []
            self.save_file()  # Create an empty file
    
    def save_file(self):
        print("Saving file")
        encode_list_known_with_ids = list(zip(self.known_face_encodings, self.known_face_names))
        with open(self.modelFile, 'wb') as file:
            pickle.dump(encode_list_known_with_ids, file)
        print("Encode File Saved")
        
    def add_face(self, face_encoding, face_name):
        face_encoding = np.array(face_encoding)
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(face_name)
        self.save_file()
        
    def encode_single_face(self, faceLoc, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img_rgb, [faceLoc])
        if not face_encodings:  # Check if the list is empty
            return None  # Return None to indicate no face was encoded
        face_encoding = face_encodings[0]
        return face_encoding
    def encode_faces(self, img, faceLoc):
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.encode_single_face, faceLoc, img)]
            results = [future.result() for future in futures]
        return results
        
    def register_faces(self, element, e1):
        data = get_from_control_reference("register_faces")

        if data["check"]:
            name = data["name"]
            img = data["img"]
            if img is not None and name != "":
                image = np.array(Image.open(img))
                detections = self.detectFace_frame(image)
                for detection in detections:
                    faceLoc = detection["face_location"]
                    bbox = detection["bbox"]
                    img = self.crop_face(image, bbox)
                    face_encoding = self.encode_faces(img, faceLoc)
                    self.add_face(face_encoding, name)
                    with element:
                        with st.spinner():
                            time.sleep(5)
                        st.success("Thêm thành công", icon="✅")
                    with e1:
                        st.image(img)
            else:
                with element:
                    with st.spinner():
                        time.sleep(5)
                    st.error("Thêm không thành công")
                print("error")
            add_to_control_reference("register_faces", {"check":False})