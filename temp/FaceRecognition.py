import cv2
import math
import pickle
import streamlit as st
import face_recognition
from other_pages.project.lib.FaceDetection import *
import time
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

def face_confidence(face_distance, face_match_threshold=0.6):
    range_val = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range_val * 2.0)
    
    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + "%"
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + "%"


class FaceRecognition(FaceDetection):
    def __init__(self, frame, face_match_threshold=0.6):
        FaceDetection.__init__(self, frame)
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
    
    def check_face(self):
        dataRequest = None
        face_locations = self.detections
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_face, face_loc) for face_loc in face_locations]
            results = [future.result() for future in futures if future.result() is not None]

        if results:
            dataRequest = max(results, key=lambda x: x[1])
        
        return dataRequest

    def process_face(self, face_location):
        faceLoc = face_location["face_location"]
        try:
            face_encoding = self.encode_faces(self.crop_face(self.frame, face_location["bbox"]), faceLoc)
            face_encoding = np.array(face_encoding)
            name = "Unknown"
            confidence = "Unknown"
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            # print("face_encoding: ", self.known_face_names)
            # print("matches: ", len(matches))
            # print("face_distances: ", len(face_distances))
            # print("best_match_index: ", best_match_index)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                confidence = face_confidence(face_distances[best_match_index])
            return name, confidence
        except Exception as e:
            # Handle any exceptions that may occur during face encoding
            print(f"Error during face encoding: {e}")
            return None

    
