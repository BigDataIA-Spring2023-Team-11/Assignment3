import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie
# import components.authenticate as authenticate

logout_btn = False
valid_user_flag = 0
placeholder = st.empty()
placeholder_logout = st.empty()


st.markdown(
        "<h3 style='text-align: center'><span style='color: #2A76BE;'>Welcome to Data Exploration Application</span></h3>",
        unsafe_allow_html=True)
st.markdown(
        "<h5 style='text-align: center'>One stop to leverage data from NOAA Satellite and radars for analysis and extract insights.</h5>",
        unsafe_allow_html=True)

# from pages.Nexrad import nexrad_home
# from streamlit_extras.switch_page_button import switch_page


if 'login_status' not in st.session_state:
    st.session_state.login_status = False

if 'login_submit' not in st.session_state:
    st.session_state.login_submit = False

if 'logout_submit' not in st.session_state:
    st.session_state.logout_submit = True

if 'username' not in st.session_state:
    st.session_state.username = False

if 'password' not in st.session_state:
    st.session_state.password = False

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'valid_user_flag' not in st.session_state:
    st.session_state.valid_user_flag = False

if 'logout_btn' not in st.session_state:
    st.session_state.logout_btn = False


valid_user_flag = False

def validate_user_credentials(username, password):

    url = 'http://api:8000/autheticate_user'
    data = {
        "un": username,
        "pwd": password
    }
    response = requests.post(url=url, json=data)
    valid_user_flag = response.json().get('matched')
    return valid_user_flag

###################################################################################
# Login Form



def home_introduction():
    def load_lottiefile(filepath:str):
        with open(filepath,"r") as f:
            return json.load(f)
    def load_lottieurl(url:str):
        r = requests.get(url)
        if r.status_code !=200:
            return None
        return r.json()
    lottie_satellite = "https://assets3.lottiefiles.com/private_files/lf30_cmdcmgh0.json"
    # with st.sidebar:
    #     lottie_pro = load_lottieurl(f"{lottie_satellite}")
    #     st_lottie(
    #         lottie_pro,
    #         speed=1,
    #         reverse=False,
    #         loop=True,
    #         height="450px",
    #         width=None,
    #         key=None,
    #     )
    # st.markdown("<h3 style='text-align: center'><span style='color: #2A76BE;'>Welcome to Data Exploration Application</span></h3>",unsafe_allow_html=True)
    # st.markdown("<h5 style='text-align: center'>One stop to leverage data from NOAA Satellite and radars for analysis and extract insights.</h5>",unsafe_allow_html=True)
    st.markdown("")
    st.markdown("The 2 datasets available are: <span style='color: #2A76BE;'>[GOES](https://noaa-goes18.s3.amazonaws.com/index.html#ABI-L1b-RadC/)</span> and <span style='color: #2A76BE;'>[NEXRAD](https://noaa-nexrad-level2.s3.amazonaws.com/index.html)</span> ",unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown("GOES (Geostationary Operational Environmental Satellite)These satellites assist meteorologists in observing and forecasting local weather phenomena such as thunderstorms, tornadoes, fog, hurricanes, flash floods, and other severe weather. GOES observations have also been useful in monitoring dust storms, volcanic eruptions, and forest fires.")
    st.markdown("")
    st.markdown("")
    st.markdown("NEXRAD (Next Generation Radar)NEXRAD detects precipitation and atmospheric movement or wind. It returns data which when processed can be displayed in a mosaic map which shows patterns of precipitation and its movement. The radar system operates in two basic modes, selectable by the operator – a slow-scanning clear-air mode for analyzing air movements when there is little or no activity in the area, and a precipitation mode, with a faster scan for tracking active weather.")


# Function for home page layout
def home_page_layout(auth_session_state_flag):
    # st.markdown(session_state_flag)

    # Checking any user is authorized / current active user Logged-In, if not it will show logout button
    if not auth_session_state_flag:
        with st.form(key="Login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            # Executes FastAPI to check Login
            # c1, c2,c3 = st.columns(3)
            # with c1:
            login_status = st.form_submit_button("Login")
            # if username == "" or password == "": st.info("Please provide credentials")
            if login_status and username != "" and password != "":
                # Validate user credentials by calling the api function passing username and password
                valid_user_flag = validate_user_credentials(username, password)

        # st.session_state["authenticated"] = False

        if username == "" or password == "":
            st.info("Please provide credentials")
        elif valid_user_flag:
            st.session_state["authenticated"] = True
            st.success("Logged In - Active User")
            # placeholder.empty()
            # logout_btn_actions()
            # st.session_state.login_status = False
            # st.session_state.logout_submit = True
            # login_status.disabled = False
        else:
            st.session_state["authenticated"] = False
            st.error("Username or password is invalid")

    else:
        st.success("Logged In - Active User")
        c1, c2, c3, c4, c5 = st.columns(5)

        with c3:
            logout_btn = st.button("Logout!")

        if logout_btn:
            st.session_state.authenticated = False
            # placeholder_logout.empty()
            # st.success("User Logged-OUT")
            home_page_layout(st.session_state.authenticated)

def logout_btn_actions():
    st.success("Found Active USER, Please logout!")
    c1, c2, c3, c4, c5 = st.columns(5)

    with c5:
        logout_btn1 = st.button("Logout")

    if logout_btn1:
        st.session_state.authenticated = False
        placeholder_logout.empty()
        # st.success("User Logged-OUT")
        home_page_layout(st.session_state.authenticated)

        # home_introduction()

#########################################################################################

# st.markdown(f"{st.session_state.login_status} - login status flag")
# st.markdown(f"{st.session_state.authenticated} - login status flag")

# st.markdown("HOME PAGE")
# with placeholder.container():
home_page_layout(st.session_state.authenticated)



