import streamlit as st


def require_login():

    if not st.session_state.get("logged_in", False):

        st.warning("🔐 Please login first.")
        st.info("Go to the Login page from the sidebar.")

        st.stop()


def logout():

    st.session_state.logged_in = False
    st.session_state.pop("username", None)

    st.success("👋 Logged out successfully!")

    st.rerun()


def show_logout():

    if st.session_state.get("logged_in", False):

        st.sidebar.success(
            f"👤 Logged in as: {st.session_state.get('username', 'User')}"
        )

        if st.sidebar.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout()