# train.py
import pandas as pd
from ast import literal_eval
from cdqa.pipeline import QAPipeline

def traing():
    df = pd.read_csv('your-custom-corpus-here.csv', converters={'paragraphs': literal_eval})

    cdqa_pipeline = QAPipeline(reader='bert_qa_vCPU-sklearn.joblib')
    cdqa_pipeline.fit_retriever(df=df)

    cdqa_pipeline = QAPipeline(reader='bert_qa_vGPU-sklearn.joblib')
    cdqa_pipeline.fit_reader('path-to-custom-squad-like-dataset.json')

    cdqa_pipeline.dump_reader('path-to-save-bert-reader.joblib')
    return (cdqa_pipeline)

def predict(cdqa_pipeline, N):
    simple = cdqa_pipeline.predict(query='your question')
    n_best = cdqa_pipeline.predict(query='your question', n_predictions=N)
    weight_best = cdqa_pipeline.predict(query='your question', retriever_score_weight=0.35)
    print ("simple answer: ", simple)
    print ("n best answer: ", n_best)
    print ("weight answer: ", weight_best)
    
if __name__ == "__main__":
    cuda_pipeline = traing()
    predict(cuda_pipeline, N = 3)

