# import streamlit as st
#
# pages = {
#     "Your account": [
#         st.Page("create_account.py", title="Create your account"),
#         st.Page("manage_account.py", title="Manage your account"),
#     ],
#     "Games": [
#         st.Page("create_game.py", title="Create Game"),
#         st.Page("my_games.py", title="My Games"),
#     ],
# }
#
# pg = st.navigation(pages)
# pg.run()


import streamlit as st

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.session_state.logged_in = True

def logout():
    st.session_state.logged_in = False

def home():
    st.title("Welcome to Game Creator")
    st.write("This is the home page of our awesome game creation app!")

def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Here you would normally check the credentials
        # For this example, we'll just log in if both fields are filled
        if username and password:
            login()
            st.success("Logged in successfully!")
            st.experimental_rerun()
        else:
            st.error("Please enter both username and password.")

def create_game():
    st.title("Create a New Game")
    st.write("Here you can create your new game!")
    # Add your game creation form or logic here

# Sidebar navigation
def sidebar_nav():
    with st.sidebar:
        st.title("Navigation")
        if st.session_state.logged_in:
            if st.button("Home"):
                st.session_state.page = "home"
            if st.button("Create Game"):
                st.session_state.page = "create_game"
            if st.button("Logout"):
                logout()
                st.session_state.page = "home"
                st.experimental_rerun()
        else:
            if st.button("Home"):
                st.session_state.page = "home"
            if st.button("Login"):
                st.session_state.page = "login"

# Main app logic
def main():
    sidebar_nav()

    if not st.session_state.logged_in:
        if st.session_state.get('page') == "login":
            login_page()
        else:
            home()
    else:
        if st.session_state.get('page') == "create_game":
            create_game()
        else:
            home()

if __name__ == "__main__":
    main()