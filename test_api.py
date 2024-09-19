import os
import pytest
from random import randrange
from dotenv import load_dotenv
from requests import Session

load_dotenv()

headers = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'GITHUBAPI',
    'Authorization': 'Bearer ' + os.getenv('TOKEN')
}
new_repo_name = f'GITHUBAPI_TEST_{randrange(1000)}'
username = os.getenv('GITHUB_USERNAME')


@pytest.fixture(scope='module')
def session():
    session = Session()
    session.headers.update(headers)
    yield session
    session.close()


def test_create_public_repo(session):
    response = session.post(
        'https://api.github.com/user/repos',
        json={'name': new_repo_name, 'private': False}
    )
    assert response.status_code == 201, f"Failed to create repository: {response.text}"
    print(f"Repository created: {response.json()['html_url']}")


def test_is_repo_created(session):
    response = session.get(f'https://api.github.com/repos/{username}/{new_repo_name}')
    assert response.status_code == 200, f"Repository was not created: {response.text}"
    print(f"Repository exists: {response.json()['html_url']}")


def test_delete_repo(session):
    response = session.delete(f'https://api.github.com/repos/{username}/{new_repo_name}')
    assert response.status_code == 204, f"Failed to delete repository: {response.text}"
    print(f'Repository deleted: {response.status_code}')
