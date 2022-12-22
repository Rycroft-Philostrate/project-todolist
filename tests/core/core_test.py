import pytest


@pytest.mark.django_db
def test_core_signup_error(client):
    """Тест регистрации пользователя с плохим паролем"""
    response = client.post("/core/signup", {
        'username': 'username',
        'password': 'password',
        'password_repeat': 'password',
    })
    assert response.status_code == 400


@pytest.mark.django_db
def test_core_signup(client):
    """Тест регистрации пользователя с хорошим паролем"""
    response = client.post("/core/signup", {
        'username': 'username_2',
        'password': 'Paa11sswo34',
        'password_repeat': 'Paa11sswo34',
    })
    assert response.status_code == 201
    assert response.data['username'] == 'username_2'


@pytest.mark.django_db
def test_core_profile(client, user):
    """Тест получения данных профиля"""
    response = client.get("/core/profile")
    assert response.data['username'] == 'username_2'
    assert response.status_code == 200


@pytest.mark.django_db
def test_core_update_password(client, user):
    """Тест изменения пользователя с правильным паролем"""
    response = client.patch("/core/update_password", {
        'old_password': 'Paa11sswo34',
        'new_password': 'YGds4367ssjr3kwr2-',
    }, content_type='application/json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_core_update_password_error(client, user):
    """Тест изменения пользователя с неправильным паролем"""
    response = client.patch("/core/update_password", {
        'old_password': 'Paa11sswo33',
        'new_password': 'YGds4367ssjr3kwr2-',
    }, content_type='application/json')
    assert response.status_code == 400


@pytest.mark.django_db
def test_core_profile_failed(client):
    """Тест получения данных профиля без авторизации"""
    response = client.get("/core/profile")
    assert response.status_code == 403
