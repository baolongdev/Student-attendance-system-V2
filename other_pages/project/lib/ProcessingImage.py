import cv2

def crop_face(frame, face_location):
    x1, y1, x2, y2 = face_location
    return frame[y1:y1+y2, x1:x1+x2]

def ConvertBGR2RGB(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

def ConvertRGB2BGR(frame):
    frame[:] = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return frame