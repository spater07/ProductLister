from bestdeals import app

def test_scrap_data():
    for rule in app.url_map.iter_rules():
        print("Hello")
        print(rule)
    response = app.test_client().get("/scrap-data")
    assert response.status_code == 200
    assert response.data == b'Hello from scrappy service, nice to meet you.'