import pytest


@pytest.mark.django_db
def test_goal_comment_create(client, user_login, goal):
    """Тест создания комментария"""
    response = client.post("/goals/goal_comment/create", {
        'text': 'goal_comment',
        'goal': goal.data['id'],
    })
    assert response.data['text'] == 'goal_comment'


@pytest.mark.django_db
def test_goal_comment_create(client, user_login, goal_comment):
    """Тест получения комментария по id"""
    response = client.get("/goals/goal_comment/1")
    assert response.status_code == 200
    assert response.data['user']['username'] == user_login.data['username']


@pytest.mark.django_db
def test_goal_comment_list(client, user_login, goal_comment):
    """Тест получения списка комментариев"""
    response = client.get("/goals/goal_comment/list")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_goal_comment_failed(client):
    """Тест получения списка комментариев без авторизации"""
    response = client.get("/goals/goal_comment/list")
    assert response.status_code == 403
