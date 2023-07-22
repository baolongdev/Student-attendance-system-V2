from streamlit_webrtc import webrtc_streamer
from other_pages.project.lib import *
import matplotlib.pyplot as plt
from random import shuffle
from scipy import ndimage
import streamlit as st
from modules import *
import json
import time
import cv2
import os

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tqdm import tqdm




def save_label_dict_to_file(label_dict):
    # Access the global label_dict
    path = get_from_control_reference("current_dir") / "assets"
    with open(f"{path}/label.txt", "w", encoding="utf8") as label_file:
        json.dump(label_dict, label_file)
    print("Label dictionary saved to 'label.txt' file.")

def ProcessingDatabase(id, class_name, name):
    db = DatabaseHandler(get_from_control_reference("pathDatabase"))
    db.connect()
    data = (id, class_name, name, None, None, None)
    db.insert_data("students", data)
    db.disconnect()


def Evaluation(model, history):
    fig1, ax = plt.subplots()
    ax.plot(history.history['accuracy'])
    ax.plot(history.history['val_accuracy'])
    ax.axhline(y=0.4, color='r', linestyle='--')
    ax.grid()
    ax.set_title("Model Accuracy")
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Epochs")
    ax.legend(['train', 'validation'])
    st.pyplot(fig1)


# Train model
def CreateModel(X_train, y_train, X_test, y_test, num_classes, info):
    modelpath = get_from_control_reference("current_dir") / "assets" / "models"
    
    # Data Augmentation (you may need to implement this separately depending on the size of your dataset)
    # augmenter = ImageDataGenerator(rotation_range=10, zoom_range=0.1, horizontal_flip=True)
    # augmenter.fit(X_train)
    
    with info:
        st.spinner("Running")
        st.warning("Đang trong quá trình train model \nvui lòng không refresh lại trang")
    
    model = Sequential()
    model.add(Conv2D(32, (5, 5), activation='relu', padding='same', input_shape=(50, 50, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (5, 5), activation='relu', padding='same'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (5, 5), activation='relu', padding='same'))

    model.add(Flatten())

    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_classes, activation='softmax'))

    # Optimizer with Learning Rate Scheduling
    optimizer = Adam(learning_rate=0.001)
    
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    # Early stopping to prevent overfitting
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Model checkpoint to save the best model during training
    checkpoint_path = str(f'{modelpath}/best_model.h5')
    model_checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_accuracy', save_best_only=True, mode='max')

    # Data Augmentation
    augmenter = ImageDataGenerator(
        rotation_range=10,   # Random rotation in the range [-10, 10] degrees
        zoom_range=0.1,       # Random zoom in/out by 10%
        horizontal_flip=True, # Random horizontal flips
        width_shift_range=0.1, # Random horizontal shifts by 10% of the image width
        height_shift_range=0.1 # Random vertical shifts by 10% of the image height
    )
    augmenter.fit(X_train)
    with st.spinner("Training..."):
    # Train the model with data augmentation and callbacks
        history = model.fit(augmenter.flow(X_train, y_train, batch_size=32),
                epochs=12,
                validation_data=(X_test, y_test),
                callbacks=[early_stopping, model_checkpoint],
                verbose=1)

    model.save(f"{modelpath}/model.h5")
    
    with info:
        st.success("Hoàn tất")
        
    Evaluation(model, history)

# Xử lý dữ liệu trước khi Train
def Processing(data, info):
    train = data[:st.session_state.TrainCount]
    test = data[st.session_state.TestCount:]
    num_classes = len(np.unique([i[1] for i in train])) + 1
    X_train = np.array([i[0] for i in train]).reshape(-1, 50, 50, 1)
    y_train = np.array([i[1] for i in train])

    X_test = np.array([i[0] for i in test]).reshape(-1, 50, 50, 1)
    y_test = np.array([i[1] for i in test])

    # One-hot encode the labels
    y_train = to_categorical(y_train, num_classes)
    y_test = to_categorical(y_test, num_classes)
    
    
    
    CreateModel(X_train, y_train, X_test, y_test, num_classes, info)


# lấy ảnh từ folder
def GetImageonFolder(datasets):   
    data = []
    for dirpath, _, filenames in os.walk(datasets):
        for filename in filenames:
            image_path = os.path.join(dirpath, filename)
            img = Image.open(image_path)
            img = img.resize((50, 50))  # Resize the image
            img_grayscale = img.convert('L')  # Convert to grayscale
            image_array = np.array(img_grayscale)
            data.append([image_array])
    shuffle(data)  # Shuffle the data in-place
    return data
    
def TrainModel(datasets, progressbar, info, label, image):
    data = []
    label_dict = {}
    for dirpath, _, filenames in os.walk(datasets):
        id, name = os.path.basename(dirpath).split("_") if "_" in os.path.basename(dirpath) else (None, None)
        label_dict[id] = name
        ProcessingDatabase(id, get_from_control_reference("ClassInput"), name)
        for filename in filenames:
            image_path = os.path.join(dirpath, filename)
            
            img = Image.open(image_path)
            img = Image.open(image_path)
            img = img.resize((50, 50))  # Resize the image
            img_grayscale = img.convert('L')  # Convert to grayscale
            image_array = np.array(img_grayscale)
            data.append([image_array, id])
            with image:
                st.image(img)
            with label:
                st.text(f'{id}_{name}/{filename}')
           
    save_label_dict_to_file(label_dict)
    shuffle(data)  # Shuffle the data in-place
    Processing(data, info)
    

# Đọc ảnh từ camera -> lưu trữ
def DataColection(element, title, datasets):
    
    with element.expander(f'{title}'):
        col1, col2 = st.columns([2, 4])
        with col1:
            ctx = webrtc_streamer(
                key="RegisterCamera",
                video_processor_factory=VideoReader,
            )
            st.markdown("#")
            StartRegister = st.button("Bắt đầu", key="StartRecord", use_container_width=True)
            st.markdown("#")
            warning = st.empty()
            
        with col2:
            col21, col22 = st.columns([2, 3])
            with col21:
                id = st.empty()                    
                st.markdown("#")
                option = st.selectbox(
                    'nơi lưu trữ',
                    ('default', 'dataVisual'),
                    key="optionSave"
                )
                st.markdown("#")
                nameInput = st.text_input("Họ và tên", key="name")                    
                st.markdown("#")
                imgCount = 0
                displayCountImage = st.empty()
                st.slider('Số lượng ảnh Train:', 100, 2000, 250, key="limitImage")
                st.markdown("#")
                st.slider('Thời gian chờ:', 0.01, 1.00, 0.02, key="delay")
            with col22:
                imgList = st.empty()
                progressbar = st.empty()            

            if StartRegister:
                imgCount = 0
                # if 
                if st.session_state.name =="":
                    print("None")
                    with warning:
                        st.warning("Nhập Họ và tên")
                elif ctx.video_processor:
                    prev_fps_time = time.time()
                    with id:
                        getid = get_id(datasets)
                        st.text(f"Id: {getid}")
                        
                        
                    while ctx.state.playing:
                        time_diff = time.time() - prev_fps_time
                        if time_diff >= st.session_state.delay:  # Update FPS every 0.5 seconds
                            img = ctx.video_processor.get_image_face_detect(ctx.video_processor.mainframe)
                            if img is None:
                                continue
                            else: 
                                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                            with imgList:
                                st.image(img)
                            save_image(datasets, img, getid, imgCount)
                            with displayCountImage:
                                st.text(f"Số lượng ảnh: {imgCount}")
                            progress_value = min(imgCount/(st.session_state.limitImage + 1), 1.0)
                            with progressbar:
                                st.progress(progress_value, "loading...")
                            imgCount += 1
                            prev_fps_time = time.time()
                        if imgCount == st.session_state.limitImage + 1:
                            with warning:
                                st.success("Đã hoàn tất việc lấy dữ liệu")
                            break
                        time.sleep(st.session_state.delay / 5)
                else:
                    with warning:
                        st.warning("Chưa khởi động Camera")
                pass

def Training(element, title, datasets):
    with element.container():
        st.subheader(f'{title}')
        st.markdown("#")
        col1, col2 = st.columns([1, 4])
    with col1:
        try:
            folder_names = os.listdir(datasets)
            image_counts = [get_image_count(datasets / folder) for folder in folder_names]
            folder_data = {"Dữ liệu": folder_names, "Số lượng ảnh": image_counts}
            ListFolder = st.dataframe(data=folder_data, height=400, use_container_width=True)
        except:
            pass
    with col2:
        TotalImage = get_count_images_in_directory(datasets) 
        if TotalImage == 0:
            TotalImage = 1
        col21, col22 = st.columns([2, 5])
        with col21:
            st.text(f"Tổng {TotalImage} bức ảnh")
            st.markdown("#")
            st.slider('Train:', 0, TotalImage, int(TotalImage/2), key="TrainCount")
            st.markdown("#")
            st.slider('Test:', 0, TotalImage, int(TotalImage/2), key="TestCount")
            st.markdown("#")
            btn_start = st.button("Run", "btn_start", use_container_width=True)
            st.markdown("#")
            progressbar = st.empty()
            st.markdown("#")
            info = st.empty()
        with col22:
            lable = st.empty()
            image = st.empty()
    
    if btn_start:
        TrainModel(datasets,progressbar, info, lable, image)
         
def VisualizeData(element, title, dataVisual, datasets) -> None:
    with element.container():
        st.subheader(f'{title}')
        st.markdown("#")
        btn = st.button("startView")
        st.markdown("#")
        
        e = st.empty()
    if btn:
        label = read_labels_from_file()
        Vdata = GetImageonFolder(dataVisual)
        model = load_model()

        # Create a grid layout for displaying images and predictions
        cols = 5
        rows = len(Vdata) // cols + (1 if len(Vdata) % cols != 0 else 0)

        # Loop through the data and display the images with predictions
        for index, data in enumerate(Vdata[:20]):
            img_data = data[0]
            data = img_data.reshape(1, 50, 50, 1)
            model_out = model.predict(data)[0]

            # Get the predicted class index
            predicted_class_index = np.argmax(model_out)
            confidence_percent = round(model_out[predicted_class_index] * 100, 2)
            
            # Plot the image and show the predicted class
            with st.expander(f"Test {index}"):
                st.image(img_data, width=300)
                # st.text(f"Predicted Class: {predicted_class_index}")
                st.text(f"True Label: {label.get(str(predicted_class_index))}")
                for i in range(len(label)):
                    class_label = label.get(str(i))
                    confidence = round(model_out[i] * 100, 2)
                    st.write(f"{class_label}: {confidence}%")
                st.text(f"Predicted Class: {predicted_class_index} (Confidence: {confidence_percent}%)")


def ManageTraining():
    datasets = get_from_control_reference("current_dir") / "assets" / "datasets"
    dataVisual = get_from_control_reference("current_dir") / "assets" / "dataVisual"
    element1 = st.empty()
    st.markdown("#")
    element2 = st.empty()
    st.markdown("#")
    element3 = st.empty()
    DataColection(element1, "Thu thập dữ liệu khuôn mặt", datasets)
    Training(element2, "Training Model", datasets)
    VisualizeData(element3, "Visualization", dataVisual, datasets)
    
    
    pass



