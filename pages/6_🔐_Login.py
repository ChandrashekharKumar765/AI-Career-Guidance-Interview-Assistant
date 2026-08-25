import streamlit as st

from database_manager import (
    create_database,
    register_user,
    verify_user
)


# =========================
# Database
# =========================

create_database()


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)


st.title("🔐 AI Career Guidance & Interview Assistant")

st.markdown(
    "### Login or create a new account"
)


# =========================
# Login / Register Tabs
# =========================

login_tab, register_tab = st.tabs(
    ["🔑 Login", "🆕 Register"]
)


# =========================
# Login
# =========================

with login_tab:

    st.subheader("🔑 User Login")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login",
        use_container_width=True
    ):

        if not username or not password:

            st.warning(
                "⚠️ Please enter username and password."
            )

        elif verify_user(username, password):

            st.session_state["logged_in"] = True
            st.session_state["username"] = username

            st.success(
                "✅ Login Successful"
            )

            st.balloons()

            st.info(
                "You can now access the protected pages."
            )

        else:

            st.session_state["logged_in"] = False

            st.error(
                "❌ Invalid Username or Password"
            )


# =========================
# Register
# =========================

with register_tab:

    st.subheader("🆕 Create New Account")

    new_username = st.text_input(
        "Choose Username",
        key="register_username"
    )

    new_password = st.text_input(
        "Choose Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    if st.button(
        "Create Account",
        use_container_width=True
    ):

        if not new_username or not new_password:

            st.warning(
                "⚠️ Please fill all required fields."
            )

        elif len(new_username) < 3:

            st.warning(
                "⚠️ Username must contain at least 3 characters."
            )

        elif len(new_password) < 6:

            st.warning(
                "⚠️ Password must contain at least 6 characters."
            )

        elif new_password != confirm_password:

            st.error(
                "❌ Passwords do not match."
            )

        else:

            success, message = register_user(
                new_username.strip(),
                new_password
            )

            if success:

                st.success(
                    "✅ Account created successfully! "
                    "Please go to Login and sign in."
                )

            else:

                st.error(
                    f"❌ {message}"
                )