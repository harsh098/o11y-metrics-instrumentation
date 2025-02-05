from random import choice
from locust import HttpUser, task


class GenerateLoad(HttpUser):
    @task
    def bombHealthCheck(self):
        endpoint = lambda : choice(["/health", "/health/path"])
        with self.client.get(endpoint(), catch_response=True) as response:
             endpoint()
