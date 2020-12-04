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
    try:
        result_json = text_comparison(document, corpus)
    except:
        antiplag_result = Result(document_id=document, error_msg="Comparison failed")
        aantiplag_result.save()

    antiplag_result = Result(document_id=document, matched_docs=result_json)
    aantiplag_result.save()
