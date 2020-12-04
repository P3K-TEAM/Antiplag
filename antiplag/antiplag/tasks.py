from celery import shared_task
from models import *
from text_comparison import text_comparison
import json

@shared_task(name='antiplag.tasks.generate_result')
def generate_result(document, elastic_result):
    # One document to check against,
    #up to 10 documents from elastic
    corpus = document
    corpus.append(elactic_result)
    result_json = text_comparison(document, corpus)
    result = json.loads(result_json)

    # Creating database records
    for x in result.items():
        if isinstance(x, dict):
            for doc in x.items():
                antiplag_result = Result(percentage=doc[percentage] ,result='P',document_id=doc)
                antiplag_result.save()
