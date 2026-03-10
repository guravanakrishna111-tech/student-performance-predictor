# 🎓 Student Performance Predictor

A Machine Learning web application that predicts a student's exam score based on study habits such as study hours, sleep hours, previous scores, and number of practice tests.
The project uses a **Linear Regression model** and provides an **interactive dashboard built with Streamlit** to visualize data and generate predictions.

---
## ☯️ Live Demo
 https://student-performance-predictor-wy8lzjce8uk7xdwaemgb7d.streamlit.app/
## 🚀 Features

* Interactive **web UI built with Streamlit**
* Predict exam scores using machine learning
* Dynamic **data visualization with Matplotlib**
* Synthetic dataset generation for students
* Real-time prediction based on user input
* Model performance evaluation using:

  * Mean Absolute Error (MAE)
  * R² Score
* Clean and modular project structure

---

## 🧠 Machine Learning Model

The application uses **Linear Regression** to predict exam scores.

### Input Features

* Study Hours
* Sleep Hours
* Previous Score
* Practice Tests

### Output

* Predicted Exam Score (0–100)

---

## 📊 Visualizations

The dashboard includes:

1. **Study Hours vs Exam Score**
2. **Actual vs Predicted Exam Scores**

These graphs help understand the relationship between study habits and exam performance.

---

## 🛠️ Tech Stack

* **Python**
* **Streamlit**
* **Scikit-learn**
* **Pandas**
* **Matplotlib**
* **NumPy**

---

## 📁 Project Structure

```
student-performance-predictor
│
├── app.py
│
├── dataset
│   ├── data_generator.py
│   └── student_data.csv
│
├── model
│   └── student_predictor.py
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the Repository

```
git clone https://github.com/yourusername/student-performance-predictor.git
```

```
cd student-performance-predictor
```

### 2. Install Dependencies

```
pip install streamlit pandas scikit-learn matplotlib numpy
```

---

## ▶️ Running the Application

Start the Streamlit app:

```
streamlit run app.py
```

The application will open in your browser:

```
http://localhost:8501
```

---

## 📈 Model Evaluation

The model performance is evaluated using:

* **Mean Absolute Error (MAE)**
* **R² Score**

These metrics help determine the accuracy of predictions.

---

## 🎯 Example Prediction

User Inputs:

```
Study Hours: 6
Sleep Hours: 7
Previous Score: 75
Practice Tests: 3
```

Output:

```
Predicted Exam Score: ~82
```

---

## 💡 Future Improvements

* Add **feature importance visualization**
* Use **advanced ML models (Random Forest / XGBoost)**
* Deploy the app using **Streamlit Cloud**
* Add **authentication system**
* Store real student datasets
* Improve UI with interactive charts (Plotly)

---

## 🌐 Deployment

You can deploy this project using:

* **Streamlit Cloud**
* **Docker**
* **AWS / GCP**
* **Render**

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Submit a Pull Request

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Developed by **Guravana Krishna**

If you like this project, consider giving it a ⭐ on GitHub.
