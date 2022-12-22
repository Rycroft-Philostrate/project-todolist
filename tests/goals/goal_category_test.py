import pytest


@pytest.mark.django_db
def test_goal_category_create(client, user_login, board):
    """Тест создания категории целей"""
    response = client.post("/goals/goal_category/create", {
        'title': 'category',
        'board': board.data['id'],
    })
    assert response.data['title'] == 'category'


@pytest.mark.django_db
def test_goal_category_pk(client, user_login, goal_category):
    """Тест получения категории целей по id"""
    response = client.get("/goals/goal_category/1")
    assert response.status_code == 200
    assert response.data['user']['username'] == user_login.data['username']


@pytest.mark.django_db
def test_goal_category_list(client, user_login, goal_category):
    """Тест получения списка категорий"""
    response = client.get("/goals/goal_category/list")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_goal_category_failed(client):
    """Тест получения списка категорий без авторизации"""
    response = client.get("/goals/goal_category/list")
    assert response.status_code == 403
