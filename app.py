import os
os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
os.environ["STREAMLIT_SERVER_ENABLECORS"] = "false"

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import hashlib
import random
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Black Friday Sales Prediction",
    page_icon="🛒",
    layout="centered"
)

# Enhanced glassy UI with more translucent effects
st.markdown("""
    <style>
        /* Base Background */
        .stApp {
            background: linear-gradient(to bottom right, rgba(0, 0, 0, 0.92), rgba(20, 20, 40, 0.88)) !important;
            backdrop-filter: blur(20px) !important;
        }
        
        /* Main container */
        .main .block-container {
            padding: 1rem 2rem !important;
            max-width: 850px !important;
        }
        
        /* Make all text white instead of gray */
        .stMarkdown, .stText, p, div, span, label, .stSelectbox, .stMultiselect, .stSlider, .stExpander, .stRadio, .stCheckbox, .stDeckGlChart, .stDataFrame {
            color: white !important;
        }
        
        /* Make input fields and placeholders have black text for better visibility */
        input, select, textarea, .stTextInput input, .stNumberInput input, .stDateInput input, .stTimeInput input, [role="combobox"] input {
            color: black !important;
        }
        
        /* Make text inside select boxes black */
        .css-81oif8, .css-16huue1, .css-162k6ax, [data-baseweb="select"] span, 
        [data-testid="stWidgetLabel"], .stSelectbox span, div[data-baseweb="select"] div,
        .stSelectbox div[data-baseweb="select"] span {
            color: black !important;
        }
        
        /* Make selectbox selected value black */
        .stSelectbox [data-baseweb="select"] [role="button"] div,
        div[data-baseweb="select"] div span,
        div[data-baseweb="select"] [role="combobox"] span,
        [data-baseweb="popover"] span {
            color: black !important;
        }
        
        /* Make dropdown options black text on white background */
        div[data-baseweb="select"] div[role="option"],
        div[data-baseweb="select"] ul li,
        div[data-baseweb="popover"] ul li,
        div[data-baseweb="menu"] li,
        div[data-baseweb="select"] div[data-testid="stMarkdown"] p {
            color: black !important;
            background-color: rgba(255, 255, 255, 0.95) !important;
        }
        
        /* Fix the dropdown options with the highlighted one */
        div[data-baseweb="select"] div[role="option"][aria-selected="true"] {
            color: black !important;
            background-color: rgba(230, 57, 70, 0.2) !important;
        }
        
        /* Make sure option list items and menu items are black text */
        .stSelectbox div[role="listbox"] span,
        div[data-baseweb="select"] ul span,
        div[data-baseweb="menu"] span {
            color: black !important;
        }
        
        /* Make sure placeholders are also visible */
        ::placeholder {
            color: rgba(0, 0, 0, 0.6) !important;
        }
        
        /* Enhance sidebar */
        .css-1d391kg, .css-163ttbj, section[data-testid="stSidebar"] {
            background-color: rgba(20, 20, 40, 0.7) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
            backdrop-filter: blur(15px) !important;
        }
        
        /* Sidebar links and text */
        .css-1d391kg p, .css-163ttbj p, section[data-testid="stSidebar"] p,
        .css-1d391kg span, .css-163ttbj span, section[data-testid="stSidebar"] span,
        .css-1d391kg a, .css-163ttbj a, section[data-testid="stSidebar"] a,
        .css-1d391kg div, .css-163ttbj div, section[data-testid="stSidebar"] div {
            color: white !important;
        }
        
        /* Active sidebar item */
        .css-1aehpvj, .css-8ojfln, [data-testid="stSidebar"] [aria-selected="true"] {
            background-color: rgba(80, 80, 200, 0.5) !important;
            border-left: 3px solid rgba(255, 255, 255, 0.7) !important;
        }
        
        /* Sidebar hover effects */
        section[data-testid="stSidebar"] [role="button"]:hover {
            background-color: rgba(100, 100, 200, 0.3) !important;
            transition: all 0.3s ease !important;
        }
        
        /* App title */
        h1 {
            color: white !important;
            font-weight: 700 !important;
            text-align: center !important;
            margin-bottom: 1rem !important;
            font-size: 2.5rem !important;
            text-shadow: 0 0 10px rgba(255, 255, 255, 0.3) !important;
        }
        
        /* Description box - enhanced glass morphism */
        .description-box {
            background: linear-gradient(135deg, rgba(30, 30, 50, 0.5), rgba(40, 40, 60, 0.5)) !important;
            border-radius: 16px !important;
            padding: 1.5rem !important;
            margin: 1.8rem 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
            color: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(5px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Section headers with icons - enhanced design */
        .section-header {
            background: linear-gradient(135deg, rgba(40, 40, 60, 0.7), rgba(30, 30, 50, 0.7)) !important;
            border-radius: 15px !important;
            padding: 1rem 1.5rem !important;
            margin: 1.2rem 0 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            font-weight: 600 !important;
            font-size: 1.2rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            backdrop-filter: blur(10px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15) !important;
        }
        
        /* Form inputs - enhanced glassy effect */
        div[data-testid="stSelectbox"], div[data-testid="stNumberInput"], div[data-testid="stTextInput"] {
            background: linear-gradient(135deg, rgba(30, 30, 50, 0.4), rgba(40, 40, 60, 0.4)) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
            padding: 4px 8px !important;
            margin-bottom: 1.2rem !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.2), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
            transition: all 0.3s ease !important;
        }
        
        /* Input hover effect */
        div[data-testid="stSelectbox"]:hover, div[data-testid="stNumberInput"]:hover {
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
        }
        
        /* Input labels */
        .stSelectbox label, .stNumberInput label {
            color: rgba(255, 255, 255, 0.85) !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.3rem !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0px !important;
            background-color: rgba(30, 30, 50, 0.3) !important;
            border-radius: 8px !important;
            padding: 0px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            border-radius: 7px !important;
            color: white !important;
            padding: 10px 20px !important;
            font-weight: 500 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(230, 57, 70, 0.15) !important;
            border-bottom: 2px solid #e63946 !important;
            box-shadow: 0 4px 12px rgba(230, 57, 70, 0.1) !important;
        }
        
        /* Prediction button */
        div.stButton > button {
            background: linear-gradient(to right, #e63946, #d62828) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-size: 16px !important;
            font-weight: bold !important;
            padding: 12px 24px !important;
            width: 100% !important;
            box-shadow: 0 4px 15px rgba(230, 57, 70, 0.4) !important;
            transition: all 0.3s ease !important;
            margin-top: 1rem !important;
        }
        
        div.stButton > button:hover {
            background: linear-gradient(to right, #d62828, #c21f1f) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(230, 57, 70, 0.5) !important;
        }
        
        /* Success/Info/Error Messages */
        .stAlert {
            background: rgba(30, 30, 50, 0.7) !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px) !important;
            border-left: 4px solid !important;
            padding: 1rem !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            margin-top: 1rem !important;
        }
        
        /* Make scrollbar stylish */
        ::-webkit-scrollbar {
            width: 8px;
            background: transparent;
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(100, 100, 120, 0.5);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(140, 140, 160, 0.6);
        }
        
        /* Dropdown options */
        div[data-baseweb="select"] ul {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid rgba(0, 0, 0, 0.1) !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
        }
        
        div[data-baseweb="select"] li {
            color: black !important;
        }
        
        /* Make dropdowns show white text for selected item on dark background */
        [data-baseweb="select"] > div > div {
            color: black !important;
            background-color: rgba(255, 255, 255, 0.9) !important;
        }
        
        div[data-baseweb="select"] li:hover {
            background-color: rgba(230, 57, 70, 0.2) !important;
        }
        
        /* Data tables */
        .stDataFrame {
            background: rgba(25, 25, 35, 0.4) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            overflow: hidden !important;
        }
        
        .stDataFrame [data-testid="stDataFrameResizable"] {
            color: white !important;
        }
        
        /* Tab content container */
        .stTabs [data-baseweb="tab-panel"] {
            padding: 1rem 0 !important;
        }
        
        /* Help tooltip icons - force them to be black */
        button[data-baseweb="tooltip"] svg,
        button[data-baseweb="tooltip"] path,
        button[data-baseweb="tooltip"] circle,
        button[data-baseweb="tooltip"] span[aria-hidden="true"] {
            color: #000000 !important;
            fill: #000000 !important;
            stroke: #000000 !important;
        }
        
        /* Help tooltip text - force black text */
        div[data-baseweb="tooltip"],
        div[data-baseweb="tooltip"] *,
        div[role="tooltip"],
        div[role="tooltip"] *,
        [data-baseweb="popover"] div,
        [data-baseweb="popover"] div * {
            color: #000000 !important;
            background-color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# Error handling for model loading
@st.cache_resource
def load_model():
    try:
        with open("model.pkl", "rb") as f:
            data = pickle.load(f)
            return data["model"], data["features"]
    except FileNotFoundError:
        st.error("❌ Model file not found. Please ensure 'model.pkl' exists in the current directory.")
        return None, None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None, None

# Function to load the dataset
@st.cache_data
def load_dataset():
    try:
        file_path = "Data/BlackFridaySales.csv"
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("❌ Dataset file not found. Please ensure 'Data/BlackFridaySales.csv' exists.")
        return None
    except Exception as e:
        st.error(f"❌ Error loading dataset: {str(e)}")
        return None

# Load the model
model, feature_names = load_model()

# Load the dataset
df = load_dataset()

if model is None or df is None:
    st.stop()

# User authentication functions
def make_hashed_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_password(password, hashed_password):
    return make_hashed_password(password) == hashed_password

# Initialize session state for user management
if 'user_db' not in st.session_state:
    st.session_state.user_db = {}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Login/Signup logic
def login_signup_ui():
    st.markdown('<h1>🛒 Black Friday Sales Prediction</h1>', unsafe_allow_html=True)
    
    auth_tab1, auth_tab2 = st.tabs(["Login", "Sign Up"])
    
    with auth_tab1:
        st.markdown('<div class="section-header">🔑 Login to Your Account</div>', unsafe_allow_html=True)
        login_email = st.text_input("Email", key="login_email")
        login_password = st.text_input("Password", type="password", key="login_password")
        
        login_button = st.button("Login", key="login_btn", use_container_width=True)
        
        if login_button:
            if login_email in st.session_state.user_db:
                if check_password(login_password, st.session_state.user_db[login_email]['password']):
                    st.session_state.logged_in = True
                    st.session_state.current_user = login_email
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Incorrect password")
            else:
                st.error("Email not found. Please sign up first.")
    
    with auth_tab2:
        st.markdown('<div class="section-header">📝 Create a New Account</div>', unsafe_allow_html=True)
        signup_name = st.text_input("Full Name", key="signup_name")
        signup_email = st.text_input("Email", key="signup_email")
        signup_password = st.text_input("Password", type="password", key="signup_password")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        signup_button = st.button("Create Account", key="signup_btn")
        
        if signup_button:
            if not signup_name or not signup_email or not signup_password:
                st.error("Please fill all fields")
            elif signup_password != signup_confirm:
                st.error("Passwords do not match")
            elif signup_email in st.session_state.user_db:
                st.error("Email already registered")
            else:
                # Create new user
                st.session_state.user_db[signup_email] = {
                    'password': make_hashed_password(signup_password),
                    'name': signup_name,
                    'joined_date': datetime.now().strftime("%Y-%m-%d")
                }
                st.success("Account created successfully! You can now login.")

# User profile and logout
def show_user_menu():
    user_info = st.session_state.user_db[st.session_state.current_user]
    
    with st.sidebar:
        st.markdown(f"### Welcome, {user_info['name']}")
        st.markdown(f"**Email:** {st.session_state.current_user}")
        st.markdown(f"**Joined:** {user_info['joined_date']}")
        
        st.markdown("---")
        
        # Help Toolbox
        st.markdown("""
        <div style='background: rgba(30, 30, 50, 0.4); 
                    padding: 15px; 
                    border-radius: 10px; 
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    margin: 10px 0;'>
            <h4 style='color: white; margin-top: 0;'>📚 Help & Tips</h4>
            <ul style='color: white; margin: 0; padding-left: 20px;'>
                <li>Use Individual Prediction for single customer estimates</li>
                <li>Try Sales Prediction for event-wide forecasts</li>
                <li>Check the Dashboard for historical data</li>
                <li>All predictions are saved in your history</li>
            </ul>
            <div style='margin-top: 10px; font-size: 0.9em; color: rgba(255, 255, 255, 0.7);'>
                Need more help? Click below:
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📖 View User Guide"):
            st.markdown("""
            <div style='background: rgba(30, 30, 50, 0.4); 
                        padding: 15px; 
                        border-radius: 10px; 
                        border: 1px solid rgba(255, 255, 255, 0.1);
                        margin: 10px 0;'>
                <h5 style='color: white; margin-top: 0;'>Quick Start Guide</h5>
                <p style='color: white; font-size: 0.9em;'>
                1. Choose prediction type from navigation<br>
                2. Enter required parameters<br>
                3. Click predict to get results<br>
                4. View history in the Dashboard
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.success("Logged out successfully!")
            time.sleep(1)
            st.rerun()

# Individual Prediction Page Function
def show_individual_prediction_page():
    # Create tabs for prediction and history
    pred_tab, history_tab = st.tabs(["Make Prediction", "Prediction History"])
    
    # Prediction Tab
    with pred_tab:
        # Customer Demographics Section
        st.markdown('<div class="section-header">👤 Customer Demographics</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox(
                "Select Gender",
                ["Male", "Female"],
                help="Select customer's gender",
                key="ind_gender"
            )
            
            age = st.selectbox(
                "Select Age Group",
                ["0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+"],
                help="Select customer's age group",
                key="ind_age"
            )
            
            occupation = st.number_input(
                "Enter Occupation (0-20)",
                min_value=0,
                max_value=20,
                step=1,
                help="Enter occupation code (0-20)",
                key="ind_occupation"
            )

        with col2:
            city_category = st.selectbox(
                "Select City Category",
                ["A", "B", "C"],
                help="A: Metro cities, B: Small cities, C: Villages",
                key="ind_city"
            )
            
            stay_years = st.selectbox(
                "Years Stayed in Current City",
                ["0", "1", "2", "3", "4+"],
                help="How long has the customer stayed in the current city",
                key="ind_stay"
            )
            
            marital_status = st.selectbox(
                "Marital Status",
                ["Single", "Married"],
                help="Select customer's marital status",
                key="ind_marital"
            )

        # Product Information Section
        st.markdown('<div class="section-header">🛍️ Product Information</div>', unsafe_allow_html=True)
        
        col3, col4 = st.columns(2)
        
        with col3:
            product_category_1 = st.number_input(
                "Product Category 1",
                min_value=1,
                max_value=20,
                value=1,
                help="Primary product category (1-20)",
                key="ind_cat1"
            )
        
        with col4:
            product_category_2 = st.number_input(
                "Product Category 2 (Optional)",
                min_value=0,
                max_value=20,
                value=0,
                help="Secondary product category (0 for none)",
                key="ind_cat2"
            )
            
            product_category_3 = st.number_input(
                "Product Category 3 (Optional)",
                min_value=0,
                max_value=20,
                value=0,
                help="Tertiary product category (0 for none)",
                key="ind_cat3"
            )
        
        # Add prediction button
        predict_btn = st.button("🔮 Predict Purchase Amount", key="ind_predict_btn")
        
        if predict_btn:
            try:
                # Show a spinner while processing
                with st.spinner("Analyzing data and making prediction..."):
                    # Convert gender to model format (M/F)
                    gender_code = 'M' if gender == 'Male' else 'F'
                    
                    # Convert marital status to binary (0/1)
                    marital_code = 1 if marital_status == 'Married' else 0
                    
                    # Initialize input dictionary with all features from the model
                    input_dict = {feature: 0 for feature in feature_names}
                    
                    # Set the base features
                    input_dict['Gender'] = 1 if gender_code == 'M' else 0
                    input_dict['Occupation'] = occupation
                    input_dict['Marital_Status'] = marital_code
                    input_dict['Product_Category_1'] = product_category_1
                    input_dict['Product_Category_2'] = product_category_2 if product_category_2 > 0 else 0
                    input_dict['Product_Category_3'] = product_category_3 if product_category_3 > 0 else 0
                    
                    # One-hot encode the categorical features
                    # Age
                    age_feature = f'Age_{age}'
                    if age_feature in feature_names:
                        input_dict[age_feature] = 1
                    
                    # City Category
                    city_feature = f'City_Category_{city_category}'
                    if city_feature in feature_names:
                        input_dict[city_feature] = 1
                    
                    # Stay Years
                    stay_feature = f'Stay_In_Current_City_Years_{stay_years}'
                    if stay_feature in feature_names:
                        input_dict[stay_feature] = 1
                    
                    # Create a DataFrame with exactly the features the model expects
                    input_df = pd.DataFrame([input_dict])[feature_names]
                    
                    # Make prediction
                    predicted_amount = model.predict(input_df)
                    predicted_amount = float(predicted_amount[0])
                
                # Display the prediction with a nice animation
                st.balloons()
                
                st.success(f"### Predicted Purchase Amount: ₹{predicted_amount:,.2f}")
                
                # Add to prediction history
                if "prediction_history" not in st.session_state:
                    st.session_state.prediction_history = []
                
                # Add timestamp
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Create history item
                history_item = {
                    "Timestamp": timestamp,
                    "Gender": gender,
                    "Age": age,
                    "City": city_category,
                    "Product Category": product_category_1,
                    "Predicted Amount": f"₹{predicted_amount:,.2f}"
                }
                
                # Add to history
                st.session_state.prediction_history.append(history_item)
                
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")
                import traceback
                st.error(traceback.format_exc())
    
    # History Tab
    with history_tab:
        st.markdown('<div class="section-header">📜 Prediction History</div>', unsafe_allow_html=True)
        
        if "prediction_history" in st.session_state and len(st.session_state.prediction_history) > 0:
            history_df = pd.DataFrame(st.session_state.prediction_history)
            st.dataframe(history_df, use_container_width=True)
            
            if st.button("Clear History", key="clear_hist_btn"):
                st.session_state.prediction_history = []
                st.success("History cleared!")
                st.rerun()
        else:
            st.info("No prediction history available. Make some predictions to see them here!")

# Sales Prediction Page Function
def show_sales_prediction_page():
    st.markdown('<div class="section-header">📈 Sales Prediction</div>', unsafe_allow_html=True)
    
    st.write("""
    Predict total sales based on key parameters. This tool helps in forecasting 
    sales for upcoming sales events or specific time periods.
    """)
    
    # Create a form for batch prediction
    with st.form("sales_prediction_form"):
        st.markdown("### Event Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            event_duration = st.number_input(
                "Event Duration (Days)",
                min_value=1,
                max_value=30,
                value=5,
                help="Duration of the sales event in days"
            )
            
            discount_percentage = st.slider(
                "Average Discount (%)",
                min_value=0,
                max_value=80,
                value=30,
                help="Average discount percentage across products"
            )
        
        with col2:
            marketing_spend = st.number_input(
                "Marketing Budget (₹)",
                min_value=1000,
                max_value=1000000,
                value=50000,
                step=1000,
                help="Total marketing budget for the event"
            )
            
            previous_event_success = st.slider(
                "Previous Event Performance",
                min_value=1,
                max_value=10,
                value=7,
                help="Rate how successful your previous event was (1-10)"
            )
        
        st.markdown("### Target Demographics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            target_age_groups = st.multiselect(
                "Target Age Groups",
                ["0-17", "18-25", "26-35", "36-45", "46-50", "51-55", "55+"],
                default=["18-25", "26-35"]
            )
        
        with col2:
            target_city_categories = st.multiselect(
                "Target City Categories",
                ["A", "B", "C"],
                default=["A", "B"]
            )
        
        with col3:
            gender_focus = st.selectbox(
                "Gender Focus",
                ["Balanced", "Male-focused", "Female-focused"]
            )
        
        st.markdown("### Product Categories")
        selected_categories = st.multiselect(
            "Select Product Categories to Focus On",
            [f"Category {i}" for i in range(1, 21)],
            default=[f"Category {i}" for i in range(1, 5)]
        )
        
        # Submit button with custom styling to ensure it appears properly
        submit_button = st.form_submit_button(
            "Predict Total Sales",
            type="primary",
            use_container_width=True
        )
    
    # Only execute after form submission
    if submit_button:
        # Calculate a sales prediction based on the inputs
        try:
            # Get our model
            model = load_model()
            
            # Create a DataFrame with the input features
            # This is just an example - you would adapt this based on your model
            
            # Create a baseline prediction (could be from your model)
            base_prediction = 50000  # Starting point
            
            # Adjust based on inputs (simplified example)
            duration_factor = event_duration / 5  # Normalized by 5 days
            discount_factor = (100 - discount_percentage) / 100  # Higher discount means higher sales
            marketing_factor = marketing_spend / 50000  # Normalized by 50k budget
            previous_success_factor = previous_event_success / 7  # Normalized by 7 (average performance)
            
            # Demographics factors
            age_factor = len(target_age_groups) / 7  # Normalized by total possible age groups
            city_factor = len(target_city_categories) / 3  # Normalized by total possible city categories
            
            # Gender factor
            if gender_focus == "Balanced":
                gender_factor = 1.0
            else:
                gender_factor = 0.9  # Slight penalty for focusing on one gender
            
            # Product category factor
            category_factor = len(selected_categories) / 20  # Normalized by total possible categories
            
            # Combine all factors
            total_factor = (
                duration_factor * 1.5 +  # Duration is important
                (2 - discount_factor) * 2.0 +  # Higher discount means higher sales (inverted factor)
                marketing_factor * 1.2 +
                previous_success_factor * 0.8 +
                age_factor * 0.7 +
                city_factor * 0.9 +
                gender_factor * 0.6 +
                category_factor * 1.1
            ) / 8  # Average of all factors
            
            # Apply the total factor to the base prediction
            predicted_sales = base_prediction * total_factor
            
            # For demonstration, add some randomness
            import random
            predicted_sales = predicted_sales * random.uniform(0.9, 1.1)
            
            # Display the prediction
            st.success(f"### 📊 Predicted Total Sales: ₹{predicted_sales:,.2f}")
            
            # Display some insights
            st.markdown("### 📈 Key Insights")
            
            # Create three columns for metrics
            col1, col2, col3 = st.columns(3)
            
            # Calculate some example metrics
            avg_order_value = predicted_sales / (event_duration * 100)  # Simplified
            estimated_transactions = predicted_sales / avg_order_value
            conversion_rate = random.uniform(2.0, 5.0)  # Example
            
            # Display metrics
            col1.metric("Estimated Total Orders", f"{int(estimated_transactions):,}")
            col2.metric("Avg. Order Value", f"₹{avg_order_value:,.2f}")
            col3.metric("Est. Conversion Rate", f"{conversion_rate:.2f}%")
            
            # Display a breakdown of sales by product category
            st.markdown("#### Sales Breakdown by Category")
            
            # Create example data for a chart
            category_data = {}
            remaining_percentage = 100
            
            for i, category in enumerate(selected_categories):
                if i == len(selected_categories) - 1:
                    # Last category gets the remaining percentage
                    category_data[category] = remaining_percentage
                else:
                    # Random percentage for each category
                    percentage = random.randint(5, min(30, remaining_percentage - 5))
                    category_data[category] = percentage
                    remaining_percentage -= percentage
            
            # Create a DataFrame for the chart
            import pandas as pd
            category_df = pd.DataFrame({
                'Category': list(category_data.keys()),
                'Percentage': list(category_data.values())
            })
            
            # Create a bar chart
            import plotly.express as px
            fig = px.bar(
                category_df, 
                x='Category', 
                y='Percentage',
                title='Sales Distribution by Product Category (%)',
                color='Percentage',
                color_continuous_scale=px.colors.sequential.Plasma
            )
            
            fig.update_layout(
                xaxis_title="Product Category",
                yaxis_title="Sales Percentage (%)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white")
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Save to history
            if "sales_prediction_history" not in st.session_state:
                st.session_state.sales_prediction_history = []
            
            # Create timestamp for history
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create a history entry
            history_entry = {
                "Timestamp": timestamp,
                "Duration (Days)": event_duration,
                "Discount (%)": discount_percentage,
                "Marketing Budget": f"₹{marketing_spend:,}",
                "Predicted Sales": f"₹{predicted_sales:,.2f}"
            }
            
            # Add to history
            st.session_state.sales_prediction_history.append(history_entry)
            
        except Exception as e:
            st.error(f"❌ Error predicting sales: {str(e)}")
            import traceback
            st.error(traceback.format_exc())

# Sales Dashboard Page Function
def show_sales_dashboard_page():
    st.markdown('<div class="section-header">📊 Sales Dashboard & Analytics</div>', unsafe_allow_html=True)
    
    # Create tabs for dashboard sections
    insights_tab1, insights_tab2 = st.tabs(["Prediction History", "Dataset Overview"])
    
    with insights_tab1:
        st.markdown('<div class="section-header">📜 Prediction History</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Individual Predictions")
            
            if "prediction_history" in st.session_state and st.session_state.prediction_history:
                history_df = pd.DataFrame(st.session_state.prediction_history)
                st.dataframe(history_df, use_container_width=True)
            else:
                st.info("No individual predictions made yet.")
        
        with col2:
            st.markdown("#### Sales Predictions")
            
            if "sales_prediction_history" in st.session_state and st.session_state.sales_prediction_history:
                sales_history_df = pd.DataFrame(st.session_state.sales_prediction_history)
                st.dataframe(sales_history_df, use_container_width=True)
            else:
                st.info("No sales predictions made yet.")
        
        # Clear history button
        if ("prediction_history" in st.session_state and st.session_state.prediction_history) or \
           ("sales_prediction_history" in st.session_state and st.session_state.sales_prediction_history):
            if st.button("🗑️ Clear History"):
                st.session_state.prediction_history = []
                st.session_state.sales_prediction_history = []
                st.success("History cleared successfully!")
                st.rerun()
    
    with insights_tab2:
        st.markdown('<div class="section-header">📊 Dataset Overview</div>', unsafe_allow_html=True)
        
        # Calculate and display some dataset statistics
        if df is not None:
            total_records = len(df)
            unique_users = df['User_ID'].nunique()
            unique_products = df['Product_ID'].nunique()
            avg_purchase = df['Purchase'].mean()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Records", f"{total_records:,}")
            
            with col2:
                st.metric("Unique Customers", f"{unique_users:,}")
            
            with col3:
                st.metric("Unique Products", f"{unique_products:,}")
            
            with col4:
                st.metric("Avg. Purchase", f"₹{avg_purchase:,.2f}")
            
            # Dataset previews
            st.markdown("### Dataset Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Distribution charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Gender distribution
                gender_counts = df['Gender'].value_counts().reset_index()
                gender_counts.columns = ['Gender', 'Count']
                gender_counts['Gender'] = gender_counts['Gender'].map({'M': 'Male', 'F': 'Female'})
                
                gender_fig = px.pie(
                    gender_counts, 
                    values='Count', 
                    names='Gender', 
                    title='Gender Distribution',
                    color_discrete_sequence=px.colors.sequential.Plasma
                )
                gender_fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white")
                )
                st.plotly_chart(gender_fig, use_container_width=True)
            
            with col2:
                # Age distribution
                age_counts = df['Age'].value_counts().reset_index()
                age_counts.columns = ['Age', 'Count']
                
                age_fig = px.bar(
                    age_counts,
                    x='Age',
                    y='Count',
                    title='Age Distribution',
                    color='Count',
                    color_continuous_scale=px.colors.sequential.Plasma
                )
                age_fig.update_layout(
                    xaxis_title="Age Group",
                    yaxis_title="Count",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color="white")
                )
                st.plotly_chart(age_fig, use_container_width=True)
            
            # Purchase distribution
            purchase_fig = px.histogram(
                df,
                x='Purchase',
                nbins=50,
                title='Purchase Amount Distribution',
                color_discrete_sequence=['rgba(230, 57, 70, 0.7)']
            )
            purchase_fig.update_layout(
                xaxis_title="Purchase Amount (₹)",
                yaxis_title="Frequency",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white")
            )
            st.plotly_chart(purchase_fig, use_container_width=True)
            
        else:
            st.error("Dataset not available for overview.")

# Add the footer to the main app
def show_footer():
    st.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: rgba(30, 30, 50, 0.4); 
                border-radius: 10px; backdrop-filter: blur(5px); border: 1px solid rgba(255, 255, 255, 0.1);">
        <p style="color: rgba(255, 255, 255, 0.7); margin: 0;">
            Black Friday Sales Prediction | Data Analysis and Prediction Tool
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main app UI if logged in
def show_main_app():
    # Application title with shopping cart icon
    st.markdown('<h1>🛒 Black Friday Sales Prediction</h1>', unsafe_allow_html=True)
    
    # Description box with glassy effect
    st.markdown("""
    <div class="description-box">
        This application predicts purchase amounts for Black Friday sales based on customer demographics 
        and product categories. You can predict individual purchase amounts or estimate total sales 
        for specific demographic segments.
    </div>
    """, unsafe_allow_html=True)
    
    # Side navigation
    with st.sidebar:
        st.markdown('<div class="section-header">📊 Navigation</div>', unsafe_allow_html=True)
        selected_page = st.radio(
            "Go to",
            ["Individual Prediction", "Sales Prediction", "Sales Dashboard"],
            key="navigation"
        )
    
    # Show the selected page
    if selected_page == "Individual Prediction":
        show_individual_prediction_page()
    elif selected_page == "Sales Prediction":
        show_sales_prediction_page()
    elif selected_page == "Sales Dashboard":
        show_sales_dashboard_page()
    
    # Show footer
    show_footer()

# App entry point - check if user is logged in
if st.session_state.logged_in:
    show_user_menu()
    show_main_app()
else:
    login_signup_ui()