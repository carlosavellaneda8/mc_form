import os
from pathlib import Path
import streamlit as st
from pyairtable import Table
from mc_form.questions import Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8


@st.cache(persist=True, allow_output_mutation=True)
def get_airtable(api_key, base_id, table_name) -> Table:
    """Returns the airtable Table to persist the data"""
    return Table(api_key, base_id, table_name)


logo_path = os.path.join(Path(__file__).parent, "img/mc_logo.jpeg")
st.image(image=logo_path)
placeholder = st.empty()
api_key = st.secrets["api_key"]
base_id = st.secrets["app_key"]
table_name = st.secrets["table"]
table = get_airtable(api_key=api_key, base_id=base_id, table_name=table_name)
del api_key, base_id, table_name

answers = []
with placeholder.container():
    st.write("Responde las siguientes preguntas:")
    answers.append(st.text_area(Q1))
    answers.append(st.text_area(Q2))
    answers.append(st.text_area(Q3))
    answers.append(st.text_area(Q4))
    answers.append(st.text_area(Q5))
    answers.append(st.text_area(Q6))
    answers.append(st.text_area(Q7))
    answers.append(st.text_area(Q8))

    submitted = st.button("Enviar")

if submitted:
    # Persisting the answers
    names = ["question" + str(id + 1) for id in range(8)] + ["Status"]
    if "" in answers:
        answers.append("Incomplete")
    else:
        answers.append("Ok")
    data = dict(zip(names, answers))
    table.create(data)

    print(data)
    placeholder.empty()
    st.markdown("# ¡Gracias!")
