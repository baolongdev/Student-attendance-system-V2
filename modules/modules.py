import os
import json
import datetime
import numpy as np
from PIL import Image
import streamlit as st
from tensorflow import keras
from modules.controls import *

def InitPageSetting(st, path, PAGE_NAME, PAGE_ICON, name_file_css="", name_file_js=""):
    current_dir = path
    CSS_MAIN = current_dir / "assets" / "styles" / "main.css"
    js_MAIN = current_dir / "assets" / "js" / "main.js"
    st.set_page_config(PAGE_NAME, PAGE_ICON)
    Custom_Code(st, """
        <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap"/>            
    """)
    if name_file_css:
        css_file = current_dir/"assets" / "styles" / name_file_css
        Custom_CSS(st, CSS_MAIN)
        Custom_CSS(st, css_file)
    else:
        Custom_CSS(st, CSS_MAIN)

    if name_file_js:
        js_file = current_dir/"assets" / "js" / name_file_js
        Custom_JS(st, js_MAIN)
        Custom_JS(st, js_file)
    else:
        Custom_JS(st, js_MAIN)


def Custom_CSS(st, css_file):
    with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()),
                    unsafe_allow_html=True)


def Custom_Code(st, data):
    st.markdown(data, unsafe_allow_html=True)


def Custom_JS(st, js_file):
    with open(js_file) as f:
        st.markdown("<script>{}</script>".format(f.read()),
                    unsafe_allow_html=True)


def Custom_Title(st, title):
    st.subheader(title)
    st.markdown("#")

# đếm số lượng image trong thu mục
def get_image_count(folder_path):
    return str(sum(1 for item in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, item))))

# Cung cấp id mới
def get_id(root):
    try:
        directories = os.listdir(root)
        count = sum(1 for directory in directories if os.path.isdir(os.path.join(root, directory)))
        return count + 1
    except:
        return 1

# Đém tất cả ảnh 
def get_count_images_in_directory(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']  # Các phần mở rộng của ảnh
    total_images = 0

    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                total_images += 1

    return total_images

# Lưu ảnh vào thư mục
def save_image(datasets, img_array, getid, imgCount):
    if st.session_state.optionSave == "dataVisual":
        path = str(datasets).replace("datasets", "dataVisual")
        id = int(get_count_images_in_directory(path) + 1)
        file_name = f'{id}.jpg'
    else:
        path = datasets /f'{getid}_{st.session_state.name}'
        file_name = f'{imgCount}.jpg'
        
    img = Image.fromarray(np.uint8(img_array))
    os.makedirs(path, exist_ok=True)
    try:
        img.save(f'{path}/{file_name}')
        print("Image saved successfully.")
    except Exception as e:
        print("Error saving the image:", e)
    pass

    
def load_model():
    modelpath = get_from_control_reference("current_dir") / "assets" / "models"
    model = keras.models.load_model(modelpath)
    return model

def read_labels_from_file():
    path = get_from_control_reference("current_dir") / "assets"
    with open(path / "label.txt", "r") as label_file:
        label_dict = json.load(label_file)
    print("Labels loaded successfully.")
    return label_dict

def ImagePath2Array(image_path):
    img = Image.open(image_path)
    img = img.resize((50, 50))  # Resize the image
    img_grayscale = img.convert('L')  # Convert to grayscale
    image_array = np.array(img_grayscale)
    return image_array

def get_time():
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    data = f"{hour}:{minute}:{second}"
    return data

def get_date():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    data = f'{year}:{month}:{day}'
    return data
