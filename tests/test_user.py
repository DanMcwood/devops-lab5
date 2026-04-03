from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]


def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={'email': 'noone@mail.com'})
    assert response.status_code == 404


def test_create_user_with_valid_email():
    new_user = {
        "name": "Test User",
        "email": "test_user@mail.com"
    }

    response = client.post("/api/v1/user", json=new_user)

    assert response.status_code in [200, 201]

    user_id = response.json()
    assert isinstance(user_id,int)


def test_create_user_with_invalid_email():
    new_user = {
        "name": "Duplicate",
        "email": users[0]["email"]
    }

    response = client.post("/api/v1/user", json=new_user)

    assert response.status_code in [400, 409]


def test_delete_user():
    new_user = {
        "name": "Delete Me",
        "email": "delete_me@mail.com"
    }

    # создаем пользователя
    create_response = client.post("/api/v1/user", json=new_user)
    assert create_response.status_code in [200, 201]

    # удаляем по email
    delete_response = client.delete(
        "/api/v1/user",
        params={"email": new_user["email"]}
    )

    assert delete_response.status_code == 204

    # проверяем что удалился
    get_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert get_response.status_code == 404
