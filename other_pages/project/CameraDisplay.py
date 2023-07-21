import streamlit as st
from streamlit_webrtc import webrtc_streamer
from other_pages.project.lib import *
from modules import *
import time


def ColOption():
    def ModeCheck(mode):
        if "rtsp://..." in mode:
            st.text_input("rtsp://...", key="linkCamera")
            st.markdown("#")
        if "https://..." in mode:
            st.text_input("https://...", key="linkCamera")
            st.markdown("#")
    Custom_Title(st, "Bảng điều kiển")
    ClassInput = st.selectbox(
        "Chọn lớp:",
        ["11CTin"],
        key="SelectClass"
    )
    st.markdown("#")
    st.radio(
        "Face detection:",
        ["default","face_detection"],
        key="Face_detection"
    )
    st.markdown("#")
    st.slider('Thời gian phát hiện khuôn mặt', 1.0, 10.0, 2.1, key="time_delay_check_faces")
    add_to_control_reference("Face_detection", st.session_state.Face_detection)
    add_to_control_reference("time_delay_check_faces", st.session_state.time_delay_check_faces)
    add_to_control_reference("listfacerecog", [])
    # ModeCheck(ModeInput)


def ColCamera():
    # Custom_Title(st, "camera")
    col1, col2 = st.columns([3, 1])
    with col1:
        ctx = webrtc_streamer(
            key="MainCamera",
            video_processor_factory=VideoReader,
        )
    with col2:
        parameterContainer = st.empty()
        pass

    with parameterContainer.container():
        with st.expander("Thông số kỹ thuật"):
            date_placeholder = st.empty()
            st.markdown("#")
            fps_placeholder = st.empty()
            st.markdown("#")
            faces_placeholder = st.empty()                        

    if ctx.video_processor:
        prev_fps_time = time.time()
        prev_checkFaceDetect_time = time.time()
        while ctx.state.playing:
            if not ctx.state.playing:
                print("hello")
                break
            else:
                print(ctx.state.playing, ctx.state)
            time_diff = time.time() - prev_fps_time
            time_checkFaceDetect = time.time() - prev_checkFaceDetect_time
            add_to_control_reference("time_checkFaceDetect", time_checkFaceDetect)
            if time_diff >= 0.5:  # Update FPS every 0.5 seconds
                ctx.video_processor.get_frame_rate(fps_placeholder)
                ctx.video_processor.get_TimeNow(date_placeholder)
                ctx.video_processor.get_faces(faces_placeholder)
                prev_fps_time = time.time()
                
            if time_checkFaceDetect >= get_from_control_reference("time_delay_check_faces"):
                prev_checkFaceDetect_time = time.time()
            time.sleep(0.1)
            


def CameraDisplay():
    option, camera = st.columns([1, 4], gap="medium")
    add_to_control_reference("prev_face_count", 0)
    with option:
        ColOption()
        pass
    with camera:
        ColCamera()
