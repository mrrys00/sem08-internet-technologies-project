import random

from locust import HttpUser, TaskSet, task, between

sample_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Ryan", "Sophia", "Thomas", "Ursula", "Victor", "Wendy", "Xander", "Yvonne", "Zach"]

class UserBehavior(TaskSet):
    @task
    def get_demo(self):
        headers = {
            "Content-Type": "application/json"
        }
        if bool(random.randint(0,1)):
            limit = random.randint(-1, 2**4)
            self.client.get(f"/demo?limit={limit}", headers=headers)
        else:
            self.client.get("/demo", headers=headers)

    @task
    def post_demo(self):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "StringField": random.choice(sample_names),
            "IntField": random.randint(2**0, 2**32),
            "BoolField": bool(random.randint(0,1))
        }
        # triggers 422 unprocessable entity in 6.25% cases
        if random.randint(0,2**4) == 0:
            del data["StringField"]
        # forces service to use default value of IntField in 6.25% cases
        if random.randint(0,2**4) == 0:
            del data["IntField"]

        self.client.post("/demo", json=data, headers=headers)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 2)
