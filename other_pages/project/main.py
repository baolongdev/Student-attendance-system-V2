from pathlib import Path
import streamlit as st
from st_pages import show_pages, Page
from other_pages.project import *


def main():
    current_dir = return_control_reference()["current_dir"]
    InitPageSetting(st, current_dir,
                    "Student attendance system", "📹", "project.css")
    Custom_Code(st, """ 
        <h2 class="project__title"> Student attendance system </h2>
    """)
    Camera, ManageStudent, Training = st.tabs(["Camera", "Quản lý", "Training"])
    with Camera:
        st.markdown("#")
        CameraDisplay()
    with ManageStudent:
        st.markdown("#")
        ManageStudentDisplay()
    with Training:
        st.markdown("#")
        ManageTraining()
        


if __name__ == '__main__':
    main()
