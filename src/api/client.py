import logging
from typing import Type, TypeVar

import httpx
from pydantic import BaseModel

# bounded generic type variable to enforce response_model to be either BaseModel
# or BaseModel inheritance
T = TypeVar("T", bound=BaseModel)
timeout = httpx.Timeout(10.0, read=120.0)


class LogizardClient:
    def __init__(self):
        self.client = None

        # !revisit
        self.logger = logging.getLogger(__name__)

    # !revisit
    async def __aenter__(self):
        # timeout_config = httpx.Timeout(
        #     c.API_TIMEOUT_GLOBAL, connect=c.API_TIMEOUT_CONNECT
        # )
        # limits_config = httpx.Limits(
        #     max_connections=c.API_MAX_CONNECTIONS, max_keepalive=c.API_MAX_KEEPALIVE
        # )

        # self.client = httpx.AsyncClient(timeout=timeout_config, limits=limits_config)
        self.client = httpx.AsyncClient(timeout=timeout)

        # !revisit why return self not client
        return self

    # !revisit learn exc_type, exc_val, exc_tb
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            # !revisit why self.client close, how about if other variables instantiated
            await self.client.aclose()

    # response_model expect class definitions (Type[T]) instead of instance (T)
    # response from client.post returns raw byte but implicitly known as json
    # response.json() converst to python dict
    # pydantic model does not accept dict since it's a class, therefore unpack operator
    # (**) is used to convert dict to keyword argumenets which can then be used to
    # instantiate a pydantic class.
    async def post_json(
        self,
        url: str,
        payload: dict,
        response_model: Type[T],
    ) -> T:
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()

            return response_model(**response.json())

        # !revisit all exceptions, raise keyword,
        # and also if raise custom ServiceTimeoutError is better
        except httpx.TimeoutException as e:
            self.logger.error(f"Timeout requesting {url}: {e}")
            raise
        except httpx.HTTPStatusError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for {url}: {e}")
            raise
        except httpx.RequestError as e:
            self.logger.error(f"Network error requesting {url}: {e}")
            raise
