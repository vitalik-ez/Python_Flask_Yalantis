from models import Driver
import json

def test_example(client, database):
    
    rv = client.get('/drivers/driver')
    print(rv)
    assert rv.status_code == 200
    print(rv.data)
    #expected = {'message': "This page doesn't exist"}
    #assert expected == json.loads(res.get_data(as_text=True))

