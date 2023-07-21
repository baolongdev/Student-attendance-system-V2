import cv2
import cvzone
import numpy as np
from modules import *
import mediapipe as mp
from PIL import Image, ImageDraw, ImageFont

mp_draw = mp.solutions.drawing_utils


class TextRenderer:
    def __init__(self, font_path, colorMain = (255, 255, 255), colorText=(0,0,0)):
        self.font_path = font_path
        self.colorMain = colorMain
        self.colorText = colorText

    def render_text(self, img, text, position, textSize=24):
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        draw = ImageDraw.Draw(img)
        fontStyle = ImageFont.truetype(str(self.font_path), textSize, encoding="utf-8")
        
        text_width, text_height = draw.textsize(text, font=fontStyle)
        padding = 10
        left, top = position
        right = left + text_width + padding * 2
        bottom = top + text_height
        draw.rectangle([(left, bottom - 35), (right, bottom)], fill=self.colorMain)
        
        draw.text((left+padding, top - padding / 2), text, self.colorText, font=fontStyle)
        
        
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

class FaceDrawer:
    def __init__(self, frame):
        self.font_path = get_from_control_reference("current_dir") / "assets" / "fonts" / "fontBe.ttf"
        self.frame = frame

    def check_face_out_frame(self, detection):
        bbox = detection.location_data.relative_bounding_box
        xmin, ymin, width, height = bbox.xmin, bbox.ymin, bbox.width, bbox.height
        if xmin < 0 or \
                ymin < 0 or \
                xmin + width > 1 or \
                ymin + height > 1:
            return False
        return True

    def draw(self, detection, dataList = None):
        if detection is None:
            return
        if dataList is None:
            # undifine
            colorMain = (255, 0, 0)
            colorText = (255, 255, 255)
            ID = Name = "Loading..."
            confidence_percent = ""
        else:
            colorMain = (255,255,255)
            colorText = (0,0,0)
            ID, Name, confidence_percent = dataList
            confidence_percent =f'{confidence_percent}%'
             
            
        mode = get_from_control_reference("Face_detection")
        image = self.frame.copy()
        bbox = detection["bbox"]
        posX = bbox[0]
        posY = bbox[1]
        if self.check_face_out_frame(detection["detection"]):
            if mode == "face_detection":
                mp_draw.draw_detection(image, detection["detection"])
            elif mode == "default":
                image = cvzone.cornerRect(image, bbox, rt=0, colorC=(255,255,255),l=20,t=2)
                text_position = (bbox[0], bbox[1] - 40)
                text_renderer = TextRenderer(self.font_path, colorMain, colorText)
                image = text_renderer.render_text(image, f'{Name} {confidence_percent}', text_position)
            self.frame[:] = image