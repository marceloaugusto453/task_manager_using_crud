import streamlit as st
import requests
from user_page import user_management_section
from project_page import project_management_section
from task_page import task_management_section
from dashboard_page import dashboard_management_section

API_URL = "http://backend:8000/" 

st.set_page_config(
    page_title="Task Manager",
    layout="wide",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded"
)


st.title("Task Manager with CRUD")

menu = [
    "User tab", 
    "Project tab", 
    "Task tab", 
    "Dashboard"
]
choice = st.sidebar.selectbox("Navigation", menu)

st.session_state.current_page = choice

if 'users' not in st.session_state:
    st.session_state.users = []

if st.session_state.current_page == "User tab":
   user_management_section()

if st.session_state.current_page == "Project tab":
   project_management_section()

if st.session_state.current_page == "Task tab":
   task_management_section()

if st.session_state.current_page == "Dashboard":
   dashboard_management_section()