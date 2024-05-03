from locust import HttpUser, TaskSet, task, between
from random import randint

PLAYERS_NUMBER = 5


class UserBehavior(TaskSet):
    @task
    def change_position(self):
        for player_id in range(PLAYERS_NUMBER):
            url = f"/positions/{player_id}"
            body = {
                "x": randint(-10, 10),
                "y": randint(-10, 10)
            }
            self.client.post(url, json=body)

    @task
    def get_positions(self):
        self.client.get(f"/positions")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)
