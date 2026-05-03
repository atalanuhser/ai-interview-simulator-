import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pdf_reader import parse_cv, parse_job_description
from app.ai.interview_engine import start_interview, send_answer
from app.ai.scoring import parse_final_scores


def run_interview_pipeline(candidate_name: str, position: str, cv_file, job_input):
    cv_text = parse_cv(cv_file)
    job_text = parse_job_description(job_input)
    chat, first_question = start_interview(candidate_name, position, job_text, cv_text)
    return chat, first_question, cv_text, job_text


def process_answer(chat, user_answer: str):
    next_q, finished, final_data = send_answer(chat, user_answer)
    if finished and final_data:
        scores = parse_final_scores(final_data)
        return None, True, scores
    return next_q, False, None
