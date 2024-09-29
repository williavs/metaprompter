import streamlit as st
st.set_page_config(layout="wide")
import hmac
from main import generate_prompt_page

def check_password() -> bool:
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials", clear_on_submit=True):
            st.markdown('<div class="login-form">', unsafe_allow_html=True)
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            submit_button = st.form_submit_button("Log in", on_click=password_entered)
            st.markdown('</div>', unsafe_allow_html=True)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and hmac.compare_digest(
                st.session_state["password"],
                st.secrets["passwords"][st.session_state["username"]],
            )
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False

def home_page():
    st.title("Welcome to CodePromptPro")

    st.markdown("""**Build a prompt for your AI-Powered IDE, even if you don't know where to start.**""")

    with st.expander("How It Works", expanded=True):
        st.markdown("""
        1. **Provide Initial Parameters:** Describe your project, its key features, and technical requirements
        2. **Answer Clarifying Questions:** Our AI will ask for additional details to refine the prompt
        3. **Receive Your Comprehensive Prompt:** Get a detailed, AI-generated prompt tailored to your project needs
        """)

    with st.expander("Current Framework Support", expanded=True):
        st.markdown("""
        CodePromptPro is optimized to generate prompts for full-stack web applications with the following technology stack (Framework Agnosticism in Development):
        """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ### Frontend
            - **Framework:** React
            - **Language:** TypeScript
            - **Routing:** React Router
            - **State Management:** Context API or Redux
            - **Styling:** CSS Modules or Styled Components
            - **Testing:** Jest and React Testing Library
            """)

            st.markdown("""
            ### Backend
            - **Language:** Python 3.x
            - **Framework:** Flask
            - **ORM:** SQLAlchemy
            - **Serialization:** Marshmallow
            - **Testing:** Pytest
            """)

        with col2:
            st.markdown("""
            ### Database
            - **PostgreSQL** (with SQLAlchemy ORM integration)
            """)

            st.markdown("""
            ### DevOps
            - **Containerization:** Docker and Docker Compose
            - **Infrastructure as Code:** Terraform (for Linode deployment)
            - **CI/CD:** GitHub Actions or Jenkins
            - **Local Development:** LocalStack for cloud service simulation
            """)

            st.markdown("""
            ### Additional Tools
            - **Environment Management:** dotenv
            - **Secrets Management:** git-crypt
            - **Code Quality:** ESLint, Prettier (Frontend), Flake8, Black (Backend)
            - **API Documentation:** Swagger/OpenAPI
            """)

    st.markdown("""
    This stack provides a robust foundation for building modern, scalable web applications. Our AI-generated prompts will guide you through setting up this entire ecosystem, from project structure to deployment configurations.
    """)

    st.success("Ready to create your first prompt? Click on 'Generate Prompt' in the sidebar to get started!")

def main():
    def load_css():
        with open("styles.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Call this function at the start of your app
    load_css()

    # Initialize session state for logout
    if 'logout' not in st.session_state:
        st.session_state.logout = False

    if st.session_state.logout:
        st.session_state.clear()
        st.rerun()

    if not check_password():
        st.stop()

    # Set default page to Home if not set
    if 'page' not in st.session_state:
        st.session_state.page = "Home"

    # Sidebar navigation
    st.sidebar.title("Navigation")
    if st.sidebar.button("Home", key="home", help="Go to Home Page"):
        st.session_state.page = "Home"
    if st.sidebar.button("Generate Prompt", key="generate_prompt", help="Generate a new prompt"):
        st.session_state.page = "Generate Prompt"
    
    # Add a logout button
    if st.sidebar.button("Logout", key="logout"):
        st.session_state.logout = True
        st.rerun()

    # Main content
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Generate Prompt":
        generate_prompt_page()

if __name__ == "__main__":
    main()