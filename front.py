import streamlit as st
import pandas as pd
from back import *

class JobSearchApp:
    def __init__(self):
        if "page" not in st.session_state:
            st.session_state.page = "home"

    def change_page(self, page_name):
        st.session_state.page = page_name

    def render_home_page(self):
        st.title("LINKEDIN")
        st.subheader("This app will help you search and find suit job for you.")
        st.header("")
        st.header("Sign in")
        email = st.text_input("Email", "")
        password = st.text_input("Password", "")
        with open("user_email.txt", 'w') as f:
            f.write(f"{email}"+ '\n')
            f.write(f"{password}"+ '\n')
        if st.button("ENTER"):
            self.change_page("app_page")    

    def render_app_page(self):
        job = st.text_input("JOBS", "Data Science")
        location = st.text_input("LOCATION", value="United State")
        experience_level = st.selectbox(
            "EXPERIENCE LEVEL",
            ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
        )
        num_results = st.number_input("How many results: ", value=10, min_value=1, max_value=20)

        with open("user_input.txt", 'w') as f:
            f.write(f"{job}"+ '\n')
            f.write(f"{location}"+ '\n')
            f.write(f"{experience_level}"+ '\n')
            f.write(f"{num_results}"+ '\n')
            
        if st.button("SEARCH"):
            self.change_page("waiting_page")

    def render_waiting_page(self):
        st.subheader("Result")
        Data = Linkedin()
        Data.run()
        df = pd.read_csv("result.csv")
        st.dataframe(df)    

    def run(self):
        if st.session_state.page == "home":
            self.render_home_page()
        elif st.session_state.page == "app_page":
            self.render_app_page()
        elif st.session_state.page == "waiting_page":
            self.render_waiting_page()


if __name__ == "__main__":
    app = JobSearchApp()
    app.run()