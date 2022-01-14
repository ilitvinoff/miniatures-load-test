import logging
from copy import deepcopy

import gevent
from locust import HttpUser, task

from common.generators import email_generator, password_generator
from common.utils import create_image
from setting import BASE_URL

logger = logging.getLogger(__name__)

CATALOGUE_DATA_TEMPLATE = {
    "name": "1",
    "description": "string",
    "theme": "string",
    "image_list": []
}


class CatalogueUser(HttpUser):
    access_token = ""

    def update_access_token(self):
        response = self.client.post(f"{BASE_URL}login/", json={"email": self.email, "password": self.password})
        if response.status_code != 200:
            logger.error(f"Can't login with email={self.email}; password={self.password}")
            return ""

        json_response_dict = response.json()
        self.access_token = json_response_dict['access']

    def post_image(self) -> int:
        with create_image() as image:
            response = self.client.post(f"{BASE_URL}image/", files={'image': image},
                                        headers={"Authorization": "Bearer  " + self.access_token})
            image_data = response.json()

            if response.status_code != 201:
                logger.error(f"ERROR: image_post. Status Code: {response.status_code}. {image_data['detail']}")

                if response.status_code == 401:
                    self.update_access_token()
                    return self.post_image()

                else:
                    return -1

            return image_data['id']

    @task
    def get_catalogue_list(self):
        self.client.get(f"{BASE_URL}catalogue/",
                        headers={"Authorization": "Bearer  " + self.access_token})

    @task
    def post_catalogue(self):
        data = deepcopy(CATALOGUE_DATA_TEMPLATE)
        data.update({'name': password_generator()})

        image_id = self.post_image()
        data["image_list"].append(image_id)
        response = self.client.post(f"{BASE_URL}catalogue/", json=data,
                                    headers={"Authorization": "Bearer  " + self.access_token})

        catalogue_data = response.json()

        if response.status_code != 201:
            logger.error(f"ERROR: catalogue_post. Status Code: {response.status_code}. {catalogue_data['detail']}")

    def on_start(self):
        self.email = email_generator()
        self.password = password_generator()
        response = self.client.post(f"{BASE_URL}signup/", json={"email": self.email, "password": self.password})
        json_response_dict = response.json()
        self.access_token = json_response_dict['access']

    def on_stop(self):
        while self.tasks:
            task=self.tasks.pop()
            task(self)
            print(len(self.tasks))
            gevent.sleep(1)

        response = self.client.delete(f"{BASE_URL}delete-account/",
                                      headers={"Authorization": "Bearer  " + self.access_token})

        while (response and response.status_code != 204):
            response_data = response.json()
            logger.error(f"ERROR: delete_user. Status Code: {response.status_code}. {response_data['detail']}")

            if response.status_code == 401:
                self.update_access_token()
            response = self.client.delete(f"{BASE_URL}delete-account/",
                                          headers={"Authorization": "Bearer  " + self.access_token})
