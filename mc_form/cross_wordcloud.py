import os
from typing import Any
from PIL import Image
import numpy as np
from wordcloud import WordCloud

def wc_generator(text: str, stopwords: list) -> Any:
    """Function that retrieves a masked image from a text"""
    path = os.path.dirname(__file__)
    mask = np.array(Image.open(os.path.join(path, "img/cross.jpg")))

    wc = WordCloud(
            mask=mask,
            margin=1,
            random_state=1,
            stopwords=stopwords,
            color_func=lambda *args, **kwargs: "white"
    ).generate(text)
    return wc.to_array()
