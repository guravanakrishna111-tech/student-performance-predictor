import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from dataset.data_generator import generate_student_data
from auth import login, sign_up
import os

st.set_page_config(page_title="Student Performance Predictor", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.main-title{
font-size:40px;
font-weight:700;
text-align:center;
color:#4CAF50;
animation: fadeIn 1s ease-in;
}
.subtitle{
text-align:center;
font-size:18px;
margin-bottom:30px;
animation: slideIn 1s ease-in;
}
.prediction{
font-size:28px;
font-weight:bold;
color:#FF4B4B;
text-align:center;
animation: bounce 0.6s ease-in-out;
padding: 20px;
border-radius: 10px;
background-color: #f0f0f0;
box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.auth-container{
max-width: 400px;
margin: auto;
padding: 20px;
border-radius: 10px;
background-color: #f9f9f9;
box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}
@keyframes slideIn {
  from {transform: translateX(-100%); opacity: 0;}
  to {transform: translateX(0); opacity: 1;}
}
@keyframes bounce {
  0%, 100% {transform: translateY(0);}
  50% {transform: translateY(-10px);}
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "login" not in st.session_state:
    st.session_state.login = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "id_token" not in st.session_state:
    st.session_state.id_token = None

@st.cache_data
def load_data():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(BASE_DIR, "dataset", "student_data.csv")

    if not os.path.exists(data_path):
        generate_student_data(200)

    data = pd.read_csv(data_path)
    return data
@st.cache_resource
def train_model():
    data = load_data()
    X = data[["studyHours","sleepHours","previousScore","practiceTests"]]
    y = data["examScore"]
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)
    model = LinearRegression()
    model.fit(X_train,y_train)
    predictions = model.predict(X_test)
    return model,X_test,y_test,predictions

# Show login/signup page if not logged in
if not st.session_state.login:
    st.markdown('<div class="main-title">🎓 Student Performance Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Login to predict your exam score</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        menu = st.radio("Select Option", ["🔐 Login", "📝 Sign Up"], horizontal=True)
        
        email = st.text_input("📧 Email Address")
        password = st.text_input("🔑 Password", type="password")
        
        if menu == "🔐 Login":
            if st.button("Login", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("❌ Please enter email and password")
                else:
                    with st.spinner("🔄 Logging in..."):
                        response = login(email, password)
                        
                        if "idToken" in response:
                            st.session_state.login = True
                            st.session_state.user_email = email
                            st.session_state.id_token = response.get("idToken")
                            st.success("✅ Login Successful!")
                            st.rerun()
                        elif "error" in response:
                            error_msg = response.get("error", {}).get("message", "Login failed")
                            st.error(f"❌ {error_msg}")
                        else:
                            st.error("❌ Invalid credentials. Please try again.")
        
        else:  # Sign Up
            if st.button("Create Account", use_container_width=True, type="primary"):
                if not email or not password:
                    st.error("❌ Please enter email and password")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                else:
                    with st.spinner("🔄 Creating account..."):
                        response = sign_up(email, password)
                        
                        if "idToken" in response:
                            st.session_state.login = True
                            st.session_state.user_email = email
                            st.session_state.id_token = response.get("idToken")
                            st.success("✅ Account created successfully!")
                            st.rerun()
                        elif "error" in response:
                            error_msg = response.get("error", {}).get("message", "Sign up failed")
                            st.error(f"❌ {error_msg}")
                        else:
                            st.error("❌ Failed to create account. Try a different email.")
        st.markdown('</div>', unsafe_allow_html=True)

# Show main app if logged in
else:
    # Sidebar logout button
    with st.sidebar:
        st.write(f"👤 Welcome, {st.session_state.user_email}!")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.login = False
            st.session_state.user_email = None
            st.session_state.id_token = None
            st.success("✅ Logged out successfully!")
            st.rerun()

    data = load_data()
    model,X_test,y_test,predictions = train_model()

    st.markdown('<div class="main-title">🎓 Student Performance Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Predict exam score based on study habits</div>', unsafe_allow_html=True)

    st.sidebar.header("📊 Student Inputs")

    study_hours = st.sidebar.slider("Study Hours",0,15,5)
    sleep_hours = st.sidebar.slider("Sleep Hours",0,12,6)
    previous_score = st.sidebar.slider("Previous Score",0,100,60)
    practice_tests = st.sidebar.slider("Practice Tests",0,10,3)

    predict = st.sidebar.button("🔮 Predict Score", use_container_width=True, type="primary")

    if predict:
        new_student = pd.DataFrame(
            [[study_hours,sleep_hours,previous_score,practice_tests]],
            columns=["studyHours","sleepHours","previousScore","practiceTests"]
        )
        predicted_score = model.predict(new_student)
        predicted_score = np.clip(predicted_score, 0, 100)
        st.markdown(f'<div class="prediction">🎯 Predicted Exam Score: {predicted_score[0]:.2f}/100</div>', unsafe_allow_html=True)
        
        # Show motivational message
        score = predicted_score[0]
        if score >= 80:
            st.balloons()
            st.success("🌟 Excellent performance! Keep up the great work!")
        elif score >= 60:
            st.info("📈 Good progress! Focus on your weak areas.")
        else:
            st.warning("⚠️ Need improvement. Increase study hours and practice more!")

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("📚 Study Hours vs Exam Score")
        fig1 = plt.figure()
        plt.scatter(data["studyHours"],data["examScore"],alpha=0.7, color="#4CAF50")
        plt.xlabel("Study Hours")
        plt.ylabel("Exam Score")
        plt.title("Study Hours vs Exam Score")
        plt.grid(True, alpha=0.3)
        st.pyplot(fig1)

    with col2:
        st.subheader("📊 Actual vs Predicted")
        fig2 = plt.figure()
        plt.scatter(y_test,predictions,alpha=0.7, color="#FF4B4B")
        plt.xlabel("Actual Scores")
        plt.ylabel("Predicted Scores")
        plt.title("Actual vs Predicted")
        plt.grid(True, alpha=0.3)
        st.pyplot(fig2)


    mae = mean_absolute_error(y_test,predictions)
    r2 = r2_score(y_test,predictions)

    m1,m2 = st.columns(2)
    m1.metric("📉 Mean Absolute Error",round(mae,2))
    m2.metric("📊 R2 Score",round(r2,2))

    st.subheader("📋 Dataset Preview")
    st.dataframe(data.head(20))
