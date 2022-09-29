import os
from pathlib import Path
import streamlit as st
from mc_form.questions import *


logo_path = os.path.join(Path(__file__).parent, "img/mc_logo.jpeg")
st.image(image=logo_path)
placeholder = st.empty()

with placeholder.container():
    st.write("Responde las siguientes preguntas:")
    q1 = st.text_area(Q1)
    q2 = st.text_area(Q2)
    st.text_area(Q3)
    st.text_area(Q4)
    st.text_area(Q5)
    st.text_area(Q6)

    submitted = st.button("Submit")

if submitted:
    print(q1)
    print(q2)
    placeholder.empty()
    st.markdown("# ¡Gracias!")
