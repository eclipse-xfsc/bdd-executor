"""
Keycloak provide token to authenticate DNS Zone Manager Server
"""
from typing import Optional, cast

import abc
from pathlib import Path

import pydantic
import requests

from ..defaults import CONNECT_TIMEOUT_IN_SECONDS
from ._service import BaseService


class Token:
    """
    Persist and share fetched Keycloak token acros Scenarios
    """
    def __init__(self, directory: Path) -> None:
        self._dir = directory

    def dump(self, value: str) -> Path:
        self._dir.mkdir(parents=True, exist_ok=True)
        path = self._dir / ".token"
        path.write_text(value)
        return path

    def load(self) -> str:
        return (self._dir / ".token").read_text()


class KeycloakServer(BaseService):
    """
    https://www.keycloak.org/server/health
    """
    host: pydantic.HttpUrl
    client_secret: str
    scope: str
    client_id: str
    realm: str

    last_token: str = ""

    def is_up(self) -> bool:
        url = f"{self.host}realms/{self.realm}"
        print(f"[PRINT:DEBUG] KeycloakServer:{url=}")
        response = requests.get(url, timeout=CONNECT_TIMEOUT_IN_SECONDS)

        # print(f"[DEBUG] {response.status_code=}, {response.text=}")

        if response.status_code != 200 or 'realm' not in response.json():
            print(f"[PRINT:DEBUG] {response.status_code=}, {response.text=}")
            return False

        return True

    def fetch_token(self) -> str:
        """
        Fetch token from remote server
        """
        url = f"{self.host}/realms/{self.realm}/protocol/openid-connect/token"
        data = {
            'grant_type': 'client_credentials',
            'client_secret': self.client_secret,
            'scope': self.scope,
            'client_id': self.client_id,
        }
        response = requests.post(
            url=url,
            data=data,
            timeout=CONNECT_TIMEOUT_IN_SECONDS
        )
        return cast(str, response.json()["access_token"])


class BaseServiceKeycloak(BaseService, abc.ABC):
    """
    Interface coupled with Keycloak Component
    """
    http: requests.Session = requests.Session()
    keycloak: KeycloakServer

    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    def _update_header(self, content_type: Optional[str] = None) -> None:
        """
        HTTP session can reuse headers, to be reused for Keycloak:
        - Authorization
        - Content-Type
        """
        self.http.headers['Authorization'] = f"Bearer {self.keycloak.last_token}"
        if content_type:
            self.http.headers['Content-Type'] = content_type
