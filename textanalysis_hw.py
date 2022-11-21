from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import glob, nltk, os, re
from nltk.corpus import stopwords
from io import StringIO 
import random
import altair as alt

st.write('## Analyzing Shakespeare Texts')

st.sidebar.header("Word Cloud Settings")
max_word = st.sidebar.slider("Max Words", 10, 200, 100, 10)
max_font = st.sidebar.slider("Size of Largest Word", 50, 350, 60)
image_size = st.sidebar.slider("Image Width", 100, 800, 400, 10)
stopwords = st.sidebar.slider("Random State", 30, 100, 20)
remove = st.sidebar.checkbox("Remove Stop Words?", value=True)


st.sidebar.header("Word Count Settings")
min_word = st.sidebar.slider("Minimum Count of Words", 5, 100, 40, 5)

# Creating a dictionary not a list 
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}

image = st.selectbox("Choose a txt file", books.keys())
image = books.get(image)


if image != " ":
    raw_text = open(image,"r").read().lower()

    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came'])
    

    tokens = nltk.word_tokenize(raw_text)
    tokens = [w for w in tokens if not w.lower() in stopwords]
    filtered_text = [w for w in tokens if not w.lower() in stopwords]

    frequency = nltk.FreqDist(tokens)
    freq_df = pd.DataFrame(frequency.items(),columns=['word','count'])



tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:
    if remove:
        if image != " ":
            cloud = WordCloud(background_color = "white", 
                            max_words = max_word, 
                            max_font_size=max_font, 
                            stopwords = stopwords, 
                            random_state=random)
            WC = cloud.generate(raw_text)
            word_cloud = cloud.to_file('wordcloud.png')
            st.image(WC.to_array(), width = image_size)
    else:
        if image != " ":
            cloud = WordCloud(background_color = "white", 
                            max_words = max_word, 
                            max_font_size=max_font, 
                            random_state=random)
            WC = cloud.generate(raw_text)
            word_cloud = cloud.to_file('wordcloud.png')
            st.image(WC.to_array(), width = image_size)


with tab2:
    if image != " ":
        st.write('Put your Bar Chart here.')

        shakebar=alt.Chart(freq_df).mark_bar().encode(
            alt.X("word:Q", title= "Words"),
            alt.Y("count:Q", title="Count")
        ).properties(width=500, height=500)
        shakebar

with tab3:
    if image is not None:
        st.write(raw_text)