"""API client for Swtch EV Charger."""

from __future__ import annotations

import asyncio
from aiohttp import ClientError, ClientSession


class SwtchApiError(Exception):
    """Base API error."""


class SwtchApiConnectionError(SwtchApiError):
    """Connection error."""


class SwtchApiClient:
    """Simple API client for the charger."""

    def __init__(self, session: ClientSession, host: str, timeout: int) -> None:
        self._session = session
        self._host = host
        self._timeout = timeout

    @property
    def host(self) -> str:
        """Return charger host."""
        return self._host

    async def async_get_station_info(self) -> dict:
        """Fetch charger station info."""
        url = f"http://{self._host}/api/GetChargingStationInfo"
        try:
            async with asyncio.timeout(self._timeout):
                response = await self._session.get(url)
                response.raise_for_status()
                data = await response.json(content_type=None)
        except (TimeoutError, asyncio.TimeoutError) as err:
            raise SwtchApiConnectionError(f"Timeout connecting to {self._host}") from err
        except ClientError as err:
            raise SwtchApiConnectionError(f"Error connecting to {self._host}: {err}") from err

        if not isinstance(data, dict):
            raise SwtchApiError("Invalid API response")

        return data
