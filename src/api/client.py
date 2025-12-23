import logging

import httpx


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
        self.client = httpx.AsyncClient()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()

    async def post_json(self, url, payload):
        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()

            return response.json()

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
