import streamlit as st

st.set_page_config(page_title="My Amazing Streamlit App", page_icon="🚀", layout="wide")

# st.image("logo.png", width=100)
st.title("Welcome to My Amazing Streamlit App")

st.write("## Solve [Problem] with ease!")

col1, col2 = st.columns(2)

with col1:
    st.write("### Key Features:")
    st.write("- Feature 1")
    st.write("- Feature 2")
    st.write("- Feature 3")

with col2:
    st.image("app_screenshot.png", caption="App in action")

st.write("### What users are saying:")
st.write("> This app changed my life! - Happy User")

if st.button("Try the App Now", key="cta"):
    st.write("Redirecting to app...")

st.write("---")
st.write("Made with ❤️ using Streamlit")