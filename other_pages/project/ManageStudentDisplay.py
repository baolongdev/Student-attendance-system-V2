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
        class_size = len(data) - 1
        present_count = sum(int(row['status']) for row in data if row['status'] == '1')
        absent_count = class_size - present_count
        with col1:
            st.text(f"Lớp: {st.session_state.SelectClass}")
            st.text(f"Sĩ số: {class_size}")
            st.text(f"Hiện diện: {present_count}")
            st.text(f"Vắng: {absent_count}")
        with col2:
            now = dt.now()
            day_of_week_preloader = st.empty()
            selected_date = st.date_input("Ngày", value=pd.to_datetime(now, format='%d/%m/%Y'))
            day_of_week = get_vi_day_of_week(selected_date.strftime('%A'))
            with day_of_week_preloader:
                st.text(f"{day_of_week}")
            
        st.markdown("#")
        with st.container():
            # Create lists to store id, name, and timeIn data
            id_list = []
            name_list = []
            time_in_list = []

            # Process data to populate lists
            for row in data:
                print(row)
                id_value = row['id']
                name_value = row['name']
                status_value = row['status']
                time_value = row['time']
                date_value = row['date']
                
                if id_value is not None:
                    id_list.append(id_value)
                    name_list.append(name_value)
                    if status_value == '1':
                        time_in_list.append(time_value)
                    else:
                        time_in_list.append("Vắng")

            # Create DataFrame from lists
            df = pd.DataFrame({
                "Id": id_list,
                "Họ và tên": name_list,
                "Thời gian đến lớp": time_in_list
            })

            # Display the DataFrame in Streamlit
            st.dataframe(df, use_container_width=True, hide_index=True)

def rows_to_dict_list(rows, column_names):
    dict_list = []
    for row in rows:
        data_dict = dict(zip(column_names, row))
        dict_list.append(data_dict)
    return dict_list

def getData():
    pathDatabase = get_from_control_reference("pathDatabase")
    db = DatabaseHandler(pathDatabase)
    data = db.select_data("students")
    # Tên cột trong bảng students (id, class, name, status, time, date)
    column_names = ["id", "class", "name", "status", "time", "date"]
    # Chuyển đổi dữ liệu từ danh sách các tuple thành danh sách các dict
    data_dict_list = rows_to_dict_list(data, column_names)
    return data_dict_list

def ManageStudentDisplay():
    element1 = st.empty()
    st.markdown("#")
    data = getData()
    Student(element1, "Thông tin lớp", data)
