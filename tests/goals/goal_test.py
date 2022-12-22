import pytest


@pytest.mark.django_db
def test_goal_create(client, user_login, goal_category):
    """Тест создания цели"""
    response = client.post("/goals/goal/create", {
        'title': 'goal',
        'category': goal_category.data['id'],
        'description': 'About ...',
    })
    assert response.data['title'] == 'goal'


@pytest.mark.django_db
def test_goal_pk(client, user_login, goal):
    """Тест получения цели по id"""
    response = client.get("/goals/goal/1")
    assert response.status_code == 200
    assert response.data['user']['username'] == user_login.data['username']
    assert response.data['title'] == 'goal'


@pytest.mark.django_db
def test_goal_list(client, user_login, goal):
    """Тест получения списка целей"""
    response = client.get("/goals/goal/list")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_goal_failed(client):
    """Тест получения списка целей без авторизации"""
    response = client.get("/goals/goal/list")
    assert response.status_code == 403
