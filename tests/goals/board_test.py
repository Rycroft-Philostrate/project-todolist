import pytest


@pytest.mark.django_db
def test_board_create(client, user_login):
    """Тест создания доски"""
    response = client.post("/goals/board/create", {'title': 'name'})
    assert response.data['title'] == 'name'


@pytest.mark.django_db
def test_board_pk(client, user_login, board):
    """Тест получения доски по id"""
    response = client.get("/goals/board/1")
    assert response.status_code == 200
    assert response.data['participants'][0]['user'] == user_login.data['username']


@pytest.mark.django_db
def test_board_list(client, user_login, board):
    """Тест получения списка досок"""
    response = client.get("/goals/board/list")
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_board_failed(client):
    """Тест получения списка досок без авторизации"""
    response = client.get("/goals/board/list")
    assert response.status_code == 403
