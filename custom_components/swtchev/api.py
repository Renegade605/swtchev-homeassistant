"""API client for Swtch / Joint Tech EVL007 chargers."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp


class SwtchApiError(Exception):
    """Base error for the Swtch API client."""


class SwtchApiConnectionError(SwtchApiError):
    """Raised when the charger cannot be reached."""


class SwtchApiResponseError(SwtchApiError):
    """Raised when the charger returns an unexpected response."""


class SwtchApiAuthError(SwtchApiError):
    """Raised when the token is missing, invalid, or expired."""


class SwtchApiClient:
    """Client for the Swtch/Joint Tech local charger API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        host: str,
        timeout: int = 10,
        token: str | None = None,
    ) -> None:
        """Initialize the API client."""
        self.session = session
        self.host = host
        self.timeout = timeout
        self.token = token

    def _headers(self) -> dict[str, str]:
        """Build request headers, including auth if a token is set."""
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def _get(self, path: str) -> Any:
        """Perform a GET request against the charger's local API."""
        url = f"http://{self.host}{path}"
        try:
            async with self.session.get(
                url,
                headers=self._headers(),
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as resp:
                if resp.status == 401:
                    raise SwtchApiAuthError(
                        "Authorization header required or token rejected"
                    )
                if resp.status != 200:
                    raise SwtchApiResponseError(
                        f"Unexpected status {resp.status} from {path}"
                    )
                try:
                    return await resp.json(content_type=None)
                except ValueError as err:
                    raise SwtchApiResponseError(
                        f"Invalid JSON response from {path}"
                    ) from err
        except asyncio.TimeoutError as err:
            raise SwtchApiConnectionError(
                f"Timed out connecting to charger at {self.host}"
            ) from err
        except aiohttp.ClientError as err:
            raise SwtchApiConnectionError(
                f"Error connecting to charger at {self.host}: {err}"
            ) from err

    async def async_get_station_info(self) -> Any:
        """Fetch charging station info."""
        return await self._get("/api/GetChargingStationInfo")

    async def async_get_network_info(self) -> Any:
        """Fetch network info."""
        return await self._get("/api/GetNetworkInfo")
