import pytest


@pytest.fixture()
@pytest.mark.django_db
def user_login(client, django_user_model):
    username = "username"
    password = "Paa11sswo34"

    django_user_model.objects.create_user(username=username, password=password)
    response = client.post("/core/login", {"username": username, "password": password}, format='json')
    return response


@pytest.fixture()
@pytest.mark.django_db
def board(client):
    response = client.post("/goals/board/create", {'title': 'name'})
    return response


@pytest.fixture()
@pytest.mark.django_db
def goal_category(client, board):
    response = client.post("/goals/goal_category/create", {
        'title': 'category',
        'board': board.data['id'],
    })
    return response


@pytest.fixture()
@pytest.mark.django_db
def goal(client, goal_category):
    response = client.post("/goals/goal/create", {
        'title': 'goal',
        'category': goal_category.data['id'],
        'description': 'About ...',
    })
    return response


@pytest.fixture()
@pytest.mark.django_db
def goal_comment(client, goal):
    response = client.post("/goals/goal_comment/create", {
        'text': 'goal_comment',
        'goal': goal.data['id'],
    })
    return response


@pytest.fixture()
@pytest.mark.django_db
def user(client):
    response = client.post("/core/signup", {
        'username': 'username_2',
        'password': 'Paa11sswo34',
        'password_repeat': 'Paa11sswo34',
    })
    return response
