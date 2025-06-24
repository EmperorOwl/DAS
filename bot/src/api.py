""" Code for calling the API. """
import aiohttp

from src.config.config import API_URL


class TimeoutException(Exception):
    pass


class InputException(Exception):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message


class ServerException(Exception):
    pass


async def send_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL+url, json=data) as response:
            json = await response.json()
            # If timeout, raise error
            if response.status == 413:
                raise TimeoutException()
            if response.status == 400:
                raise InputException(json["name"], json["message"])
            if response.status == 500:
                raise ServerException()
            return json
