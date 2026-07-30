""" Code for calling the API. """
import aiohttp

from src.config.config import API_URL

_session: aiohttp.ClientSession | None = None


def init_session(session: aiohttp.ClientSession) -> None:
    """ Registers the bot's shared HTTP session for API calls. """
    global _session
    _session = session


class TimeoutException(Exception):
    pass


class InputException(Exception):
    def __init__(self, name: str, message: str):
        self.name = name
        self.message = message


class ServerException(Exception):
    pass


async def send_request(url, data):
    if _session is None:
        raise RuntimeError("HTTP session not initialized")
    async with _session.post(API_URL+url, json=data) as response:
        json = await response.json()
        if response.status in (504, 413):
            raise TimeoutException()
        if response.status == 400:
            raise InputException(
                json.get("name", "BadRequest"),
                json.get("message", "Invalid request"),
            )
        if response.status == 500:
            raise ServerException()
        return json
