import os
from pathlib import Path
import streamlit as st
import matplotlib.pyplot as plt
from pyairtable.api.table import Table
from mc_form.questions import QUESTIONS 
from mc_form.cross_wordcloud import wc_generator


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

sw_path = os.path.join(Path(__file__).parent, "stopwords.txt")
stopwords = open(sw_path, "r").read().split()

answers = []
with placeholder.container():
    st.write("Responde las siguientes preguntas:")
    for question in QUESTIONS.values():
        answers.append(st.text_area(question))

    submitted = st.button("Enviar")

if submitted:
    # Persisting the answers
    names = ["question" + str(id + 1) for id in range(len(QUESTIONS))] + ["Status"]
    if "" in answers:
        answers.append("Incomplete")
    else:
        answers.append("Ok")
    data = dict(zip(names, answers))
    table.create(data)

    records = table.all(fields=["question7", "question9"])
    text_data = [
        record["fields"].get("question7", "") + " " + record["fields"].get("question9", "")
        for record in records
    ]
    text = " ".join(text_data).upper()
    img_array = wc_generator(text=text, stopwords=stopwords)

    placeholder.empty()
    st.markdown(
    """
    ## ¡Gracias!

    Recuerda que a pesar de nuestros temores, de nuestras fallas, de nuestras debilidades, tenemos
    a nuestra disposición la cruz de Cristo; allí podemos clavarlo todo en la cruz, dejar atrás
    todo pecado, peso y carga, y correr sin rendirnos en pos de Jesucristo. ¡Las naciones nos
    esperan!
    """
    )

    fig = plt.figure()
    fig.patch.set_facecolor('xkcd:black')
    fig.tight_layout()
    plt.imshow(img_array)
    plt.axis("off")
    st.pyplot(fig)
