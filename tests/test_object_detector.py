
def test_predict_without_attached_image(client):
    rv = client.post('/predict')
    json_data = rv.get_json()
    assert rv.status_code == 404
    expected = {"error":"image don't find"}
    assert expected == json_data


def test_predict_with_attached_image(client):
    image = "detect_traffic_cones.jpeg"
    data = {
        'image': (open(image, 'rb'), image)
    }
    rv = client.post('/predict', data=data)
    json_data = rv.get_json()
    assert rv.status_code == 200
    expected = {"no_traffic_cones": "0.117523454",  "traffic_cones": "0.8824765"}
    assert expected == json_data


def test_predict_with_attached_no_image(client):
    no_image_file = "app.db"
    data = {
        'image': (open(no_image_file, 'rb'), no_image_file)
    }
    rv = client.post('/predict', data=data)
    json_data = rv.get_json()
    assert rv.status_code == 404
    expected = {"error": "ONLY image are allowed"}
    assert expected == json_data