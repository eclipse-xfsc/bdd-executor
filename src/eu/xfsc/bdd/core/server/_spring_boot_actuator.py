"""
Spring Boot Actuator Base Model Interface
"""

import abc
from functools import cached_property

import pydantic
import requests

from ..defaults import CONNECT_TIMEOUT_IN_SECONDS
from ._service import BaseService


class SpringBootActuator(BaseService, abc.ABC):
    """
    Interface helper for test spring-boot-actuator based REST API
    """

    host: pydantic.HttpUrl

    @property
    def health_url(self) -> str:
        return f"{self.host}actuator/health"

    @cached_property
    def health(self) -> requests.Response:
        """
        See `https://www.baeldung.com/spring-boot-actuators#6-health-groups`_
        """
        url = self.health_url
        print(f"HTTP GET {url}")
        return requests.get(url, timeout=CONNECT_TIMEOUT_IN_SECONDS)

    def is_up(self) -> bool:
        """
        Expecting acknowledge from `actuator/health` endpoint.
        """
        try:
            response = self.health
        except requests.exceptions.ConnectionError as exc:
            print("Can not connect, please ensure server is up", exc)
            return False

        assert response.status_code == 200, f"{response.status_code=}, {response.text=}"
        response_json = response.json()
        assert response_json['status'] == "UP"

        return True
