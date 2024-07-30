import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()  # load all env variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += str(page.extract_text())
    return text


# Prompt Template
input_prompt = """
Act as an ATS (Application Tracking System) tailored for the data science, machine learning, NLP, and AI job market, 
which is currently extremely clustered and saturated. Analyze the input, which could be a job description or resume, 
focusing on identifying and matching keywords relevant to these fields. Your task is to determine the extent to which 
the candidate's qualifications and experiences match the job requirements based on the presence of specific keywords 
related to data science techniques, machine learning algorithms, NLP methodologies, and AI technologies. 
Calculate and provide a percentage matching score reflecting the alignment between the candidate's profile and the job's demands. 
Be harsh on giving the matching percentage.
Assign the percentage matching based on job description and the missing keywords with high accuracy
resume : {text}
description : {jd}
I want the response in one single string having the structure {{"Job Description Match" : "%", "Missing Keywords : []", "Profile Summary"
: ""}}
"""


# Streamlit App
st.title("Prit_ATS_tracker")
st.subheader("Get Your Resume ATS")

# Create a container to hold the job description and resume upload
with st.container():
    jd = st.text_area("Paste the Job Description Here", height=200)
    uploaded_file = st.file_uploader("Upload your Latest Resume here", type="pdf", help="Please Upload the PDF")

# Create a button to submit the job description and resume
submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        # Replace placeholders in the prompt template with actual values
        prompt = input_prompt.replace("{text}", text).replace("{jd}", jd)
        response = get_response(prompt)
        # Display the response in a subheader
        st.subheader("ATS Response:")
        st.write(response)