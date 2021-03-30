from celery import shared_task
from langdetect import detect
import os
from math import ceil

from .models import Result, Submission, Document
from nlp.elastic import Elastic
from nlp.text_comparison import text_comparison
from nlp.text_preprocessing import extract_text_from_file, preprocess_text

from .constants import EMAIL_SENDER
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings

@shared_task(name="antiplag.tasks.process_documents")
def process_documents(submission_id):
    try:
        submission = Submission.objects.get(id=submission_id)
    except:
        return

    # update submission status
    submission.status = Submission.SubmissionStatus.PROCESSING
    submission.save()

    documents = submission.documents.all()

    for document in documents:

        # extract file contents
        if document.type == Document.DocumentType.FILE:
            document.text_raw = process_file(document.file)

        # preprocess text
        document.language = detect_language(document.text_raw)
        document.text = process_raw_text(document.text_raw, document.language)

        # save the document
        document.save()
    # document comparison
    compare_documents(documents)

    # update submission status
    submission.status = Submission.SubmissionStatus.PROCESSED
    submission.save()

    # send email when done
    if submission.email is not None:
        try:
            validate_email(submission.email)
        except ValidationError as e:
            print(_("bad email, details:"), e)
        else:
            send_mail(_("Antiplag - Your check has finished!"),
                _("Check the results of your check at https://antiplag.sk/result/") + str(submission.id) + "/" ,
                EMAIL_SENDER,
                [submission.email],
                fail_silently=False)

def process_file(file):
    return extract_text_from_file(file.path)


def detect_language(text_raw):
    return detect(text_raw)


def process_raw_text(text, language):
    # TODO: Would not work in parallel
    os.environ["w2n.lang"] = language
    return preprocess_text(
        text,
        words_to_numbers=True,
        remove_numbers=False,
        tokenize_words=False,
        lemmatize=False,
        remove_stopwords=True,
    )[1]


def compare_documents(
    documents, threshold=0.15, similar_count=10, round_decimal_places=2
):
    """
    Compare given documents against each other and N most similar documents from elastic
    """
    round_factor = 10 ** round_decimal_places

    for doc in documents:
        # returns list of dictionaries
        # {
        #   "document_name": "referaty-zemegula"
        #   "text": "Co je zemegula? Je to hoax, zem je predsa plocha."
        # }
        similar_documents = Elastic.find_similar(doc.text, similar_count)

        # make new list and remove current doc
        user_documents = list(documents)
        user_documents.remove(doc)

        result_similarity = 0
        compared_count = 0

        results = []
        # Compare current document with elastic docs
        for similar_doc in similar_documents:
            similarity = None
            try:
                # returns percentage representing how similar docs are
                similarity = text_comparison(doc.text, similar_doc["text"])

                result_similarity += similarity['first_to_second']['similarity']
                compared_count += 1
            except:
                # TODO: Should uncomparable documents be included?
                similarity = None

            if similarity['first_to_second']['similarity'] > threshold:
                results.append(
                    {
                        "name": similar_doc["name"],
                        "percentage": ceil(similarity['first_to_second']['similarity'] * round_factor) / round_factor,
                        "intervals": similarity['first_to_second']['intervals'],
                        "elastic_id": similar_doc["elastic_id"],
                        "text": similar_doc["text"],
                    }
                )

        # Compare current document against user uploaded docs
        for user_doc in user_documents:
            try:
                # returns percentage representing how similar docs are
                similarity = text_comparison(doc.text, user_doc.text)

                result_similarity += similarity['first_to_second']['similarity']
                compared_count += 1
            except:
                # TODO: Should uncomparable documents be included?
                similarity = None

            results.append(
                {
                    "name": str(user_doc),
                    "percentage": similarity['first_to_second']['similarity'],
                    "intervals": similarity['first_to_second']['intervals']
                    })

        if compared_count > 0:
            result_similarity /= compared_count

        Result.objects.create(
            document=doc,
            matched_docs=results,
            percentage=ceil(result_similarity * round_factor) / round_factor,
        )
