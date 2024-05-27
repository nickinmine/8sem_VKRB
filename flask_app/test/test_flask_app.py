import sys
import requests

sys.path.append("D:\\mirea_tasks\\vkr\\python-server\\flask_app")


class TestFlaskApp:

    def test_index_page_status_code(self):
        response = requests.get('http://127.0.0.1:5000')
        assert response.status_code == 200

    def test_index_page_markup(self):
        response = requests.get('http://127.0.0.1:5000')
        assert "<h2>О сайте</h2>" in response.text

    def test_map_page_status_code(self):
        response = requests.get('http://127.0.0.1:5000/map')
        assert response.status_code == 200

    def test_statistics_page_status_code(self):
        response = requests.get('http://127.0.0.1:5000/statistics')
        assert response.status_code == 200

    def test_stations_page_status_code(self):
        response = requests.get('http://127.0.0.1:5000/stations')
        assert response.status_code == 200

    def test_users_page_unauthorized_status_code(self):
        response = requests.get('http://127.0.0.1:5000/users', allow_redirects=False)
        assert response.status_code == 302

    def test_prices_page_unauthorized_status_code(self):
        response = requests.get('http://127.0.0.1:5000/prices', allow_redirects=False)
        assert response.status_code == 302

    def test_page_not_found_status_code(self):
        response = requests.get('http://127.0.0.1:5000/fakepath')
        assert response.status_code == 404

    def test_api_prices_status_code(self):
        response = requests.get('http://127.0.0.1:5000/api/v1/prices')
        assert response.status_code == 200

    def test_api_prices_correct_geojson(self):
        response = requests.get('http://127.0.0.1:5000/api/v1/prices')
        data = response.json()
        assert "type" in data
        assert "FeatureCollection" in data["type"]
        assert "features" in data
        for feature in data["features"]:
            assert "type" in feature
            assert feature["type"], "Feature"
            assert "geometry" in feature
            assert "coordinates" in feature["geometry"]
            assert "type" in feature["geometry"]
            assert "Point" in feature["geometry"]["type"]
            assert "properties" in feature
            assert "address" in feature['properties']
            assert "brand" in feature['properties']
            assert "ai_92" in feature['properties']
            assert "ai_95" in feature['properties']
            assert "ai_98" in feature['properties']
            assert "ai_100" in feature['properties']
            assert "dt" in feature['properties']
            assert "gas" in feature['properties']
