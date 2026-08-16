import streamlit as st

st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)

st.title("🔐 User Login")
st.markdown("### Welcome to AI Career Guidance & Interview Assistant")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login", use_container_width=True):

    if username == "admin" and password == "admin123":

        st.session_state["logged_in"] = True
        st.session_state["username"] = username

        st.success("✅ Login Successful")
        st.balloons()

        st.info("You can now access the protected pages.")

    else:
        st.session_state["logged_in"] = False
        st.error("❌ Invalid Username or Password")