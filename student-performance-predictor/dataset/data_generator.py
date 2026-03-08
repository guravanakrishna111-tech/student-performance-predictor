import pandas as pd
import random
import os

def generate_student_data(num_students):

    data = []

    for i in range(num_students):
        study_hours = random.randint(1,14)
        sleep_hours = random.randint(4,12)
        previous_score = random.randint(50,100)
        practice_tests = random.randint(0,8)

        exam_score = int((3*study_hours)+(0.4*previous_score)+(1.5*practice_tests)+random.randint(-5,5))
        exam_score = min(100,max(0,exam_score))

        data.append([study_hours,sleep_hours,previous_score,practice_tests,exam_score])

    df = pd.DataFrame(
        data,
        columns=["studyHours","sleepHours","previousScore","practiceTests","examScore"]
    )

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir,"dataset","student_data.csv")

    df.to_csv(file_path,index=False)