import json

from github import GithubException

from data.config import CERT_PATH, A_PATH


def get_cer_data():
    try:
        from loader import repository
        file = repository.get_contents(CERT_PATH)
        contents = file.decoded_content.decode()
        cer = json.loads(contents)
    except GithubException:
        cer = {}

    return cer


def get_a_list():
    try:
        from loader import repository
        file = repository.get_contents(A_PATH)
        contents = file.decoded_content.decode()
        a = json.loads(contents)
    except GithubException:
        a = []

    return a
