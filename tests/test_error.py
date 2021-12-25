import json

def test_404(client):
    res = client.get('/')
    assert res.status_code == 404
    expected = {'message': "This page doesn't exist"}
    assert expected == json.loads(res.get_data(as_text=True))