import streamlit as st

class JobSearchApp:
    def __init__(self):
        if "page" not in st.session_state:
            st.session_state.page = "home"

    def change_page(self, page_name: str) -> None:
        st.session_state.page = page_name

    def render_home_page(self):
        st.title("Hello!")
        st.subheader("This app will help you search and find your suit job.")
        st.header("")
        if st.button("ENTER"):
            self.change_page("app_page")

    def render_app_page(self):
        st.subheader("JOBS")
        num_results = st.number_input("How many results: ", value=5, min_value=1)
        job_query = st.text_input("Enter the job", "")
        st.button("SEARCH")

        if st.checkbox("FILTER"):
            if st.checkbox("LOCATION"):
                location = st.text_input("City", "")
            if st.checkbox("EXPERIENCE"):
                experience_level = st.selectbox(
                    "EXPERIENCE LEVEL",
                    ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
                )

        st.write("")
        st.write("")
        if st.button("RETURN HOME"):
            self.change_page("home")

    def run(self):
        if st.session_state.page == "home":
            self.render_home_page()
        elif st.session_state.page == "app_page":
            self.render_app_page()

if __name__ == "__main__":
    app = JobSearchApp()
    app.run()