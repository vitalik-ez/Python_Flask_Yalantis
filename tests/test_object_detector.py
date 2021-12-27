

def test_get_list_vehicles(model_object_detection):
    rv = client.post('/predict')
    json_data = rv.get_json()
    assert rv.status_code == 200