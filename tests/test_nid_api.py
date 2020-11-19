from datetime import date

from fastapi.testclient import TestClient

from api import app


ENDPOINT_URL = "nid/extract"
client = TestClient(app)


def test_valid_national_id():
    data = {"nid": "29001011234567"}
    response = client.post(ENDPOINT_URL, json=data)
    data = response.json()

    assert response.status_code == 200
    assert data["century_code"] == "2"
    assert data["year"] == "90"
    assert data["month"] == "01"
    assert data["day"] == "01"
    assert data["birthdate"] == "01 January 1990"
    assert data["governerate_code"] == "12"
    assert data["governerate"] == "Al Dakhlia"
    assert data["identity"] == "3456"
    assert data["gender"] == "female"
    assert data["check_digit"] == "7"


def test_invalid_national_id_length():
    data = {"nid": "290010112345677"}
    response = client.post(ENDPOINT_URL, json=data)

    assert response.status_code == 422
    assert "National ID provided is not 14 digits." in response.text


def test_national_id_must_contain_only_digits():
    data = {"nid": "aaaa10112345677"}
    response = client.post(ENDPOINT_URL, json=data)

    assert response.status_code == 422
    assert "National ID must contain only [0-9] digits." in response.text


def test_national_id_with_invalid_century_code():
    data = {"nid": "19001011234567"}
    response = client.post(ENDPOINT_URL, json=data)

    assert response.status_code == 422
    assert "Invalid century code." in response.text


def test_national_id_with_invalid_birthdate():
    data = {"nid": "29000001234567"}
    response = client.post(ENDPOINT_URL, json=data)

    assert response.status_code == 422
    assert "Invalid Birthdate." in response.text


def test_national_id_with_invalid_future_birthdate():
    future = str(date.today().year + 1)[2:]
    data = {"nid": f"3{future}01011234567"}
    response = client.post(ENDPOINT_URL, json=data)

    assert response.status_code == 422
    assert "Invalid Birthdate." in response.text

def test_national_id_with_invalid_governerate_code():
    data = {"nid": "29001010534567"}
    response = client.post(ENDPOINT_URL, json=data)

    assert response.status_code == 422
    assert "Invalid governerate code." in response.text
