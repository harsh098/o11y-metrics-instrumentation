from locust import HttpUser, task, between
import random

class APIUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def get_root(self):
        response = self.client.get("/")
        self._handle_response(response)

    @task
    def get_item(self):
        item_id = random.choice([1, 2, 0])  # Random choice between valid (1, 2) and invalid (0)
        response = self.client.get(f"/items/{item_id}/")
        self._handle_response(response)

    @task
    def create_item(self):
        data = {
            "name": "Sample Item",
            "description": "A sample item description",
            "price": random.choice([10, -5]),  # Random choice between valid (10) and invalid (-5)
            "tax": 1.5
        }
        response = self.client.post("/items/", json=data)
        self._handle_response(response)

    @task
    def update_item(self):
        item_id = random.choice([1, 2, 0])  # Random choice between valid (1, 2) and invalid (0)
        data = {
            "name": "Updated Item",
            "description": "Updated description",
            "price": random.choice([20, -1]),  # Random price (20 valid, -1 invalid)
            "tax": 2.5
        }
        response = self.client.put(f"/items/{item_id}/", json=data)
        self._handle_response(response)

    @task
    def partial_update_item(self):
        item_id = random.choice([1, 2, 0])  # Random choice between valid (1, 2) and invalid (0)
        data = {
            "name": "Partially Updated Item",
            "price": random.choice([15, -3])  # Random valid or invalid price
        }
        response = self.client.patch(f"/items/{item_id}/", json=data)
        self._handle_response(response)

    @task
    def delete_item(self):
        item_id = random.choice([1, 2, 0])  # Random choice between valid (1, 2) and invalid (0)
        response = self.client.delete(f"/items/{item_id}/")
        self._handle_response(response)

    @task
    def redirect(self):
        response = self.client.get("/redirect/")
        self._handle_response(response)

    @task
    def server_error(self):
        response = self.client.get("/server-error/")
        self._handle_response(response)

    def _handle_response(self, response):
        """Handles responses and prints the status code"""
        if response.status_code == 200:
            print(f"Success: {response.status_code}")
        elif response.status_code == 404:
            print(f"Not Found: {response.status_code}")
        elif response.status_code == 400:
            print(f"Bad Request: {response.status_code}")
        elif response.status_code == 500:
            print(f"Server Error: {response.status_code}")
        elif response.status_code == 301:
            print(f"Redirect: {response.status_code}")
        else:
            print(f"Unhandled Response: {response.status_code}")
