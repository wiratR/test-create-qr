import requests
import json
from requests.api import request
from requests.exceptions import HTTPError
from json.decoder import JSONDecodeError
from utils.helper import create_ref


class CallApi:
    """
    implement handle http request
    """

    def __init__(self, reuestId):
        self.urls = "http://58.9.110.21:50247/api/payment/" + str(reuestId)
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/json"
        }

        self.method = "POST"

    def get_confirm_status(self):
        isConfirm = False
        try:
            response = requests.request(
                "GET", self.urls, headers=self.headers, timeout=5)

            print(f"response status code : {response.status_code}")
            if response.status_code == 200 or response.status_code == 201:
                # print(f"response : {response.json()}")
                print(f"response : {response.json().get('request_status_id')}")
                # print(f"response qrdata : {response.json().get('qrRawData')}")
                # return response.json().get('qrRawData')
                if response.json().get('request_status_id') == 1:
                    isConfirm = True
                return isConfirm
        except requests.exceptions.HTTPError as error:
            return error
        except requests.exceptions.ConnectionError as errc:
            return errc
        except requests.exceptions.Timeout as errt:
            return errt
        except requests.exceptions.RequestException as err:
            return err

    def run(self, amount):
        print(f"run url = {self.urls}")
        print(f"run header = {self.headers}")
        dataPayload = {
            "request_type": "QR",
            "request_status_id": 0,
            "txn_amount": int(amount),
            "ref1": str(create_ref()),
            "merchant_info_id": "c03d9043-c383-4422-a4ca-5fe43ad122c5",
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
