import requests
import json
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
import uuid


class CallApi:
    """
    implement handle http request
    """

    def __init__(self):
        self.urls = "http://58.9.110.21:29925/api/payment/" + str(uuid.uuid4())
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }

        self.method = "POST"

    def run(self, amount):
        print(f"run url = {self.urls}")
        print(f"run header = {self.headers}")
        dataPayload = {
            "request_type": "QR",
            "request_status": 0,
            "txn_amount": int(amount),
            "merchant_info_id": "c03d9043-c383-4422-a4ca-5fe43ad122c5",
            "confirm_items_id": "0"
        }

        print(f"run payload = {dataPayload}")

        try:
            response = requests.request(
                "POST", self.urls, headers=self.headers, data=json.dumps(dataPayload), timeout=5)

            print(f"response status code : {response.status_code}")

            if response.status_code == 200 or response.status_code == 201:
                # print(f"response : {response.json()}")
                print(f"response qrdata : {response.json().get('qrRawData')}")
                return response.json().get('qrRawData')
                # pass
                # try:
                #     return ResponseAPIObj(response.status_code, SUCCES, json.dumps(response.json(), indent=4))
                # except JSONDecodeError:
                #     log.error("There was a problem accessing the data.")

        except requests.exceptions.HTTPError as error:
            return error
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err
