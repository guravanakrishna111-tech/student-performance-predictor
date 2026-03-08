import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from dataset.data_generator import generate_student_data

st.set_page_config(page_title="Student Performance Predictor", page_icon="🎓", layout="wide")

st.markdown("""
<style>
.main-title{
font-size:40px;
font-weight:700;
text-align:center;
color:#4CAF50;
}
.subtitle{
text-align:center;
font-size:18px;
margin-bottom:30px;
}
.prediction{
font-size:28px;
font-weight:bold;
color:#FF4B4B;
text-align:center;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    generate_student_data(200)
    data = pd.read_csv("dataset/student_data.csv")
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

data = load_data()
model,X_test,y_test,predictions = train_model()

st.markdown('<div class="main-title">🎓 Student Performance Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict exam score based on study habits</div>', unsafe_allow_html=True)

st.sidebar.header("Student Inputs")

study_hours = st.sidebar.slider("Study Hours",0,15,5)
sleep_hours = st.sidebar.slider("Sleep Hours",0,12,6)
previous_score = st.sidebar.slider("Previous Score",0,100,60)
practice_tests = st.sidebar.slider("Practice Tests",0,10,3)

predict = st.sidebar.button("Predict Score")

if predict:
    new_student = pd.DataFrame(
        [[study_hours,sleep_hours,previous_score,practice_tests]],
        columns=["studyHours","sleepHours","previousScore","practiceTests"]
    )
    predicted_score = model.predict(new_student)
    st.markdown(f'<div class="prediction">Predicted Exam Score: {predicted_score[0]:.2f}</div>', unsafe_allow_html=True)

col1,col2 = st.columns(2)

with col1:
    fig1 = plt.figure()
    plt.scatter(data["studyHours"],data["examScore"],alpha=0.7)
    plt.xlabel("Study Hours")
    plt.ylabel("Exam Score")
    plt.title("Study Hours vs Exam Score")
    st.pyplot(fig1)

with col2:
    fig2 = plt.figure()
    plt.scatter(y_test,predictions,alpha=0.7)
    plt.xlabel("Actual Scores")
    plt.ylabel("Predicted Scores")
    plt.title("Actual vs Predicted")
    st.pyplot(fig2)

mae = mean_absolute_error(y_test,predictions)
r2 = r2_score(y_test,predictions)

m1,m2 = st.columns(2)
m1.metric("Mean Absolute Error",round(mae,2))
m2.metric("R2 Score",round(r2,2))

st.subheader("Dataset Preview")
st.dataframe(data.head(20))