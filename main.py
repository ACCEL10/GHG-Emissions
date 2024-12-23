import streamlit as st
from streamlit_option_menu import option_menu

# Ensure these files have the app() function defined
import login
import register_user

st.set_page_config(page_title="GHG Emission", layout="wide")

class MultiApp:
    def __init__(self):
        self.apps = []  

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function,
        })

    def run(self):
        # Sidebar navigation
        with st.sidebar:
            app_names = [app["title"] for app in self.apps]
            selected_app = option_menu(
                menu_title='Navigation',
                options=app_names,
                icons=['house', 'person'],
                menu_icon="cast",
                default_index=0
            )

        # Load the selected app
        for app in self.apps:
            if app["title"] == selected_app:
                app["function"]()

# Multi-page app setup
app = MultiApp()
app.add_app("Login", login.app)  # Ensure 'app()' exists in login.py
app.add_app("Register", register_user.app)  # Ensure 'app()' exists in register_user.py

if __name__ == "__main__":
    app.run()
