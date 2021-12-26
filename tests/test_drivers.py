from models import Driver
import json
import pytest
from datetime import datetime, timedelta


drivers = (
    {"first_name": "Vitalii", "last_name": "Yezghor", "created_at": datetime(2020, 9, 15)},
    {"first_name": "Bill", "last_name": "Gates", "created_at": datetime(2021, 12, 15)},
)


@pytest.fixture(autouse=True)
def create_drive():
    for driver in drivers:
        driver1 = Driver()
        driver1.first_name = driver["first_name"]
        driver1.last_name = driver["last_name"]
        driver1.save()


def test_get_list_drivers(client):
    rv = client.get('/drivers/driver')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert len(json_data['drivers']) == 2
    assert json_data['drivers'][0]['first_name'] == "Vitalii"


def test_create_driver(client):
    rv = client.post('/drivers/driver', json={
        "first_name" : "Vitaliy",
        "last_name" : "Yezghor"
    })
    json_data = rv.get_json()
    assert rv.status_code == 201
    assert json_data['id'] == 3


def test_update_driver(client):
    rv = client.put('/drivers/driver', json={
        "first_name" : "Vitaliy",
        "last_name" : "Yezghor"
    })
    json_data = rv.get_json()
    assert rv.status_code == 201
    assert json_data['id'] == 3


def test_get_driver_by_id(client):
    rv = client.get('/drivers/driver/1')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert json_data['driver']['id'] == 1
    assert json_data['driver']['first_name'] == "Vitalii"
    assert json_data['driver']['last_name'] == "Yezghor"
    

def test_get_drivers_created_at__gte(client):
    date = datetime.today() + timedelta(days=1)
    rv = client.get('/drivers/driver?created_at__gte={}'.format(date.strftime("%d-%m-%Y")))
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert len(json_data['drivers']) == 0


def test_get_drivers_created_at__lte(client):
    date = datetime.today() + timedelta(days=1)
    rv = client.get('/drivers/driver?created_at__lte={}'.format(date.strftime("%d-%m-%Y")))
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert len(json_data['drivers']) == 2


def test_delete_driver_by_id(client):
    id = 1
    rv = client.delete('/drivers/driver/' + str(id))
    json_data = rv.get_json()
    assert rv.status_code == 200
    expected =  {"delete_driver" : "Driver with id = {} succeed remove".format(id)}
    assert expected == json_data

