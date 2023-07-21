import random
import pandas as pd
from modules import *
import streamlit as st
from datetime import datetime as dt
from streamlit_webrtc import webrtc_streamer
from other_pages.project.lib import *
import time
import os

def get_vi_day_of_week(day):
    vi_day_of_week = {
        "Monday": "Thứ Hai",
        "Tuesday": "Thứ Ba",
        "Wednesday": "Thứ Tư",
        "Thursday": "Thứ Năm",
        "Friday": "Thứ Sáu",
        "Saturday": "Thứ Bảy",
        "Sunday": "Chủ Nhật"
    }
    return vi_day_of_week.get(day, "")

def Student(element, title, data):
    with element.expander(f'{title}: {st.session_state.SelectClass}'):
        col1, col2 = st.columns(2)
        class_size = len(data)
        with col1:
            st.text(f"Lớp: {st.session_state.SelectClass}")
            st.text(f"Sĩ số: {class_size}")
            st.text("Hiện diện: ")
            st.text("Vắng: ")
        with col2:
            now = dt.now()
            day_of_week = get_vi_day_of_week(now.strftime('%A'))
            date = now.strftime('%d/%m/%Y')
            time = now.strftime('%H:%M:%S')
            st.text(f"{day_of_week}")
            st.text(f"Ngày: {date}")

        st.markdown("#")
        with st.container():
            # Replace the existing DataFrame with the data from the 'data' dictionary
            df = pd.DataFrame()
            df["id"] = list(data.keys())
            df["name"] = list(data.values())
            df["timeIn"] = [None for _ in range(len(data))]

            # Display the DataFrame in Streamlit
            st.dataframe(
                df,
                column_config={
                    "id": "Id",
                    "name": "Họ và tên",
                    "timeIn": "Thời gian đến lớp",
                },
                use_container_width=True,
                hide_index=True
            )



def ManageStudentDisplay():
    element1 = st.empty()
    st.markdown("#")
    data = read_labels_from_file()
    data.pop("null")
    Student(element1, "Thông tin lớp", data)
    
    
    pass