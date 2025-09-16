import streamlit as st
import google.generativeai as genai
import os

api = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Lets creat the UI
st.title(':orange[HEALTHIFY] :- :blue[AI powered personal Health Assistant]')
st.markdown(' ##### This application assist you to have a better and healthier life . You can ask your health related questions and get personalized health recommendations.')
tips = '''Follow the steps below to get started:
* Enter your details in the sidebar.
* Enter your gender, age, height (cms), and weight (kgs).
* Select the number on the fitness scale (0-5). 5-Fittest and 0-Least fit
* After filling the details, write your prompt here and get customized responses
'''
st.write(tips)

# Lets configure the sidebar
st.sidebar.header(':blue[ENTER YOUR DETAILS]')

name= st.sidebar.text_input(':blue[Enter your Name  : ]')
age = st.sidebar.number_input(':blue[Age]', min_value=0, max_value=120, value=25)
gender = st.sidebar.selectbox(':blue[Gender]', options=['Male', 'Female', 'Other'])
weight = st.sidebar.number_input(':blue[Weight (kg)]', min_value=0.0, value=70.0, step=0.1, format="%.1f")
height = st.sidebar.number_input(':blue[Height (cm)]', min_value=0.0, value=175.0, step=0.1, format="%.1f")
bmi = weight / ((height / 100) ** 2)
fitness = st.sidebar.slider(':blue[Fitness Level (0-5)]', min_value=0, max_value=5, value=0)
st.sidebar.write(':blue[Your BMI is]:', round(bmi, 2), 'kg/m^2')

# Lets use genai to get personalized health recommendations from the user inputs
user_query = st.text_input(':blue[Enter your health query here:]')
prompt=f'''Assume you are a health expert. Based on the following user information provided by the user name ,age,gender,height,weight.
 provide personalized health recommendations.
- Name: {name}
- Age: {age}
- Gender: {gender}
- Height: {height} cm
- Weight: {weight} kg
- BMI: {round(bmi, 2)} kg/m^2
- Fitness Level: {fitness}

Your output should be in the following format:
* It start by giving one or two line comment on the details that have been provided by the user.
* It should explain what is the real issue or concern that the user has based on their query and the provided information.
* What could be the possible reasons for the user's issue or concern.
* What are the possible solutions or recommendations to address the user's issue or concern.
* You can also mention what doctors or specialists the user should consult for their issue if required.
* Strictly avoid giving any medical advice or diagnosis.
* You can also suggest lifestyle changes, dietary adjustments, or specific exercises tailored to the user's profile.
* Output should be in bullet points and use tables wherever required.
* In the last give me a 5 point summary of the key points discussed.

User Query: {user_query}
'''


if user_query:
    response = model.generate_content(prompt)
    st.write(response.text)
