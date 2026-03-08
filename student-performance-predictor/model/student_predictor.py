import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.abspath("../dataset"))
from dataset.data_generator import generate_student_data

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

if not os.path.exists("../dataset/student_data.csv"):
    generate_student_data(200)

data = pd.read_csv("../dataset/student_data.csv")

data = data.dropna()

plt.scatter(data["studyHours"],data["examScore"],alpha=0.7)
plt.xlabel("Study Hours")
plt.ylabel("Exam Score")
plt.title("Study Hours vs Exam Score")
plt.show()

X = data[["studyHours","sleepHours","previousScore","practiceTests"]]
y = data["examScore"]

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=42)

model = LinearRegression()
model.fit(X_train,y_train)

predictions = model.predict(X_test)

print("Predictions")
print(predictions)

mae = mean_absolute_error(y_test,predictions)
print("Mean Absolute Error:",mae)

r2 = r2_score(y_test,predictions)
print("R2 Score:",r2)

plt.scatter(y_test,predictions,alpha=0.7)
plt.xlabel("Actual Scores")
plt.ylabel("Predicted Scores")
plt.title("Actual vs Predicted")
plt.show()

study_hours = float(input("Enter Study Hours: "))
sleep_hours = float(input("Enter Sleep Hours: "))
previous_score = float(input("Enter Previous Score: "))
practice_tests = float(input("Enter Practice Tests: "))

new_student = pd.DataFrame(
    [[study_hours,sleep_hours,previous_score,practice_tests]],
    columns=["studyHours","sleepHours","previousScore","practiceTests"]
)

predicted_score = model.predict(new_student)

print("Predicted Exam Score:",predicted_score[0])