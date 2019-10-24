# query.py
import os
import pandas as pd
from ast import literal_eval

from cdqa.utils.filters import filter_paragraphs
from cdqa.pipeline import QAPipeline

from cdqa.utils.download import download_model, download_bnpp_data

download_bnpp_data(dir='./data/bnpp_newsroom_v1.1/')
download_model(model='bert-squad_1.1', dir='./models')

df = pd.read_csv('./data/bnpp_newsroom_v1.1/bnpp_newsroom-v1.1.csv', converters={'paragraphs': literal_eval})
df = filter_paragraphs(df)
df.head()

cdqa_pipeline = QAPipeline(reader='./models/bert_qa_vCPU-sklearn.joblib')
cdqa_pipeline.fit_retriever(df=df)

#query = 'Since when does the Excellence Program of BNP Paribas exist?'
query = ' what activity did the BNP Paribas offer?'


prediction = cdqa_pipeline.predict(query)

print('query: {}'.format(query))
print('answer: {}'.format(prediction[0]))
print('title: {}'.format(prediction[1]))
print('paragraph: {}'.format(prediction[2]))



