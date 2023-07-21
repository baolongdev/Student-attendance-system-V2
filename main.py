from pathlib import Path
import streamlit as st
from st_pages import show_pages, Page
from PIL import Image
from modules import *
from data import *


def Social(SOCIAL_MEDIA):
    st.write("#")
    cols = st.columns(len(SOCIAL_MEDIA))
    for index, (platform, link) in enumerate(SOCIAL_MEDIA.items()):
        cols[index].write(f"[{platform}]({link})")


def ExpQua():
    st.write("#")
    st.subheader("Experience & Qualifications")
    st.write(
        """
        - ✨ abc xyz         
        - ✨ abc xyz         
        - ✨ abc xyz         
    """
    )


def Skills():
    st.write("#")
    st.subheader("Hard Skills")
    st.write(
        """
        - 👨‍💻 Programming: Python, HTML, CSS, JavaScript, C++, ...  
        - 📊 Data Visulization: MS Excel
        - 📚 Modeling: Logistic regression, linear regression, decition trees
        - 🗒️ Databases: Postgres, MongoDB, MySQL       
    """
    )


def Proj(PROJECTS):
    st.write("#")
    st.subheader("Projects & Accomplishments")
    st.write("---")
    for project, link in PROJECTS.items():
        st.write(f"[{project}]({link})")


def SetPage() -> None:
    show_pages(
        [
            Page("main.py", "Home", "⭐"),
            Page("other_pages/project/main.py",
                 "Student-attendance-system", "📹"),
        ]
    )


def App():
    current_dir = Path(
        __file__).parent if "__file__" in locals() else Path.cwd()
    add_to_control_reference("current_dir", current_dir)
    InitPageSetting(st, current_dir, "Home", "⭐")

    resume_file = current_dir / "assets" / "CV.pdf"
    profile_pic = current_dir / "assets" / "profile-pic.jpg"
    with open(resume_file, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    profile_pic = Image.open(profile_pic)

    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.image(profile_pic, width=230)
    with col2:
        st.title(NAME)
        st.write(DESCRIPTION)
        st.download_button(
            label="📃 Download Resume",
            data=PDFbyte,
            file_name=resume_file.name,
            mime="application/octet-stream",
        )
        st.write("📫", EMAIL)
    # --- SOCIAL LINKS ---
    Social(SOCIAL_MEDIA)
    # --- EXPERIENCE & QUALIFICATIONS ---
    # ExpQua()
    # --- SKILLS ---
    Skills()
    # --- Projects & Accomplishments ---
    Proj(PROJECTS)


if __name__ == '__main__':
    SetPage()
    App()
