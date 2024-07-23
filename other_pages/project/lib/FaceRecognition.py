import cv2
import streamlit as st
from PIL import Image
from modules import *


class FaceRecognition():
    def __init__(self):
        try:
            self.model = load_model() 
        except:
            self.model = None
        self.label = read_labels_from_file()

    def FaceRecognition_Processing(self, face_cut):
        if not self.model:
            print()
            return None

        img_data = face_cut
        img = Image.fromarray(np.uint8(img_data))  # Convert image data to an Image object
        img = img.resize((50, 50))  # Resize the image
        img_grayscale = img.convert('L')  # Convert to grayscale
        image_array = np.array(img_grayscale)
        data = image_array.reshape(1, 50, 50, 1)
        
        model_out = self.model.predict(data)[0]

        # Get the predicted class index
        predicted_class_index = np.argmax(model_out)
        # print("predicted_class_index: ",predicted_class_index)
        confidence_percent = round(model_out[predicted_class_index] * 100, 2)
        id = predicted_class_index
        name = self.label[str(predicted_class_index)]
        return (id, name, confidence_percent)
        
        

    
