from models import Vehicle
import pytest
from datetime import datetime


vehicles = (
    {"make": "Audi", "model": "A8", "plate_number": "ВК 8888 ВК"},
    {"make": "BMW", "model": "X5", "plate_number": "AA 5555 AA"},
)


@pytest.fixture(autouse=True)
def create_vehicle():
    for vehicle in vehicles:
        car = Vehicle()
        car.make = vehicle["make"]
        car.model = vehicle["model"]
        car.plate_number = vehicle["plate_number"]
        car.save()


def test_get_list_vehicles(client):
    rv = client.get('/vehicles/vehicle')
    json_data = rv.get_json()
    assert rv.status_code == 200
    assert len(json_data['vehicles']) == 2
    assert json_data['vehicles'][0]['make'] == "Audi"


def test_create_vehicle(client):
    rv = client.post('/vehicles/vehicle/', json={
        "make": "Mercedes", 
        "model": "S63amg", 
        "plate_number": "ВК 7777 ВК"
    })
    json_data = rv.get_json()
    assert rv.status_code == 201
    assert json_data['id'] == 3


def test_get_driver_by_not_existing_id(client):
    id = 987
    rv = client.get('/vehicles/vehicle/{}'.format(id))
    json_data = rv.get_json()
    assert rv.status_code == 404
    expected = {"message" : "Vehicle with id = {} not found".format(id)}
    assert expected == json_data



def test_delete_vehicle_by_id(client):
    id = 1
    rv = client.delete('/vehicles/vehicle/{}'.format(id))
    json_data = rv.get_json()
    assert rv.status_code == 200
    expected = {"delete_vehicle" : "Vehicle with id = {} succeed remove".format(id)}
    assert expected == json_data