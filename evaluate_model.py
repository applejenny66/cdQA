#evaluate_model.py

#annotation
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

def datatojson(df):
    from cdqa.utils.converters import df2squad
    json_data = df2squad(df=df, squad_version='v1.1', output_dir='.', filename='dataset-name')
    return (json_data)

#annotator -> add ground truth qa pairs
#evaluate pipeline object

def evaluatepipeline(json, cdqa_pipeline):
    from cdqa.utils.evaluation import evaluate_pipeline
    evaluate_pipeline(cdqa_pipeline, 'path-to-annotated-dataset.json')

def evaluatereader(json, cdqa_pipeline):
    from cdqa.utils.evaluation import evaluate_reader
    evaluate_reader(cdqa_pipeline, 'path-to-annotated-dataset.json')

if __name__ == "__main__":
    # define df
    cdqa_pipeline = traing()
    json_data = datatojson(df)
    evaluatepipeline(json_data, cdqa_pipeline)
    evaluatereader(json_data, cdqa_pipeline)
