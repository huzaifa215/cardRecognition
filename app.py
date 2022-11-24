import streamlit as st
from PIL import Image
import pickle
import pandas as pd
import base64
import re
from nanonets import NANONETSOCR
model = NANONETSOCR()
model.set_token('YFkl9K2QBl2joxrBQf1hyGquJSEB1Jvm')


def extract_id(string):
  if "\n" in string:
    string = string.replace("\n","")
  id = re.search(r"(F|S)20[1-2][0-9][0-9]{6}",string)
  if id:
    student_id = string[id.start():id.end()+1]
    return student_id.strip()
  else:
    return "Unable to extract ID"

icon = Image.open('validating-ticket.png')
st.set_page_config(page_title='Student Validation System', page_icon = icon)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg.jpg')    
st.header('Welcome to student validation')

uploaded_file = st.file_uploader("Upload Picture to be validated", type=[".png",".jpg"], accept_multiple_files=False)
if uploaded_file is not None:
  image_address = "Images{}".format(" \ ".strip() + uploaded_file.name.strip())
  #image_address = "Images\ ".strip() + uploaded_file.name
  #image_address = "Images\{}".format(uploaded_file.name)
  string = model.convert_to_string(image_address)
  student_id = extract_id(string)
  if student_id.isalnum():
    students = pd.read_csv('students.csv')
    for index,id in enumerate(students['Student Id']):
      if id == student_id:
        st.checkbox("Use container width", value=False, key="use_container_width")
        st.dataframe(students.loc[index], use_container_width=st.session_state.use_container_width)
  else:
    st.write("Not a good day!")
 
