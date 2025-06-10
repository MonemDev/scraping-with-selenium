import streamlit as st


class JobSearchApp:
    def __init__(self):
        if "page" not in st.session_state:
            st.session_state.page = "home"

    def change_page(self, page_name):
        st.session_state.page = page_name

    def render_home_page(self):
        st.title("LINKEDIN")
        st.subheader("This app will help you search and find your suit job.")
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
        
        st.subheader("JOBS")
        job = st.text_input("Enter the job", "")

        location = st.text_input("LOCATION", value="Remote")

        experience_level = st.selectbox(
            "EXPERIENCE LEVEL",
            ["Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"]
        )

        num_results = st.number_input("How many results: ", value=5, min_value=1, max_value=10)

        with open("user_input.txt", 'w') as f:
            f.write(f"{job}"+ '\n')
            f.write(f"{location}"+ '\n')
            f.write(f"{experience_level}"+ '\n')
            f.write(f"{num_results}"+ '\n')
        st.button("SEARCH", key="search2")

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