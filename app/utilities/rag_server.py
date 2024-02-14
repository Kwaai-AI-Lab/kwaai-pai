import os
import warnings
from embedchain import App
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = "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"


app = App.from_config("utilities/mistral.yaml")

def query(question):
    print(f"Executing query: {question}")

    # Suppress FutureWarning related to InferenceApi deprecation
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=FutureWarning)
        response = app.query(question)
        print(f"Response: {response} \n")

    return response

app.add("./emails.csv")

email_string = """Subject: School Reminder - Back to Class on February 15th ### From: School Notifications <notifications@school.edu> ### Date: 2024-02-15 00:00:00-07:00 ### Body: Dear Parent/Guardian,

This is a reminder that the new school term begins on February 15th. Please ensure that your child is prepared for the upcoming academic year.

If you have any questions or concerns, feel free to contact the school office at notifications@school.edu or call (555) 789-0123.

Wishing your child a successful school year!

Sincerely,
School Administration
"""

if __name__ == "__main__":  
   query("Create a draft email to answer the following email and print only the body : " + email_string)
   