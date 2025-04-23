"""
Concrete implementation of eu.xfsc.bdd.core.server._spring_boot_actuator.SpringBootActuator.
"""
import requests

from eu.xfsc.bdd.core.defaults import CONNECT_TIMEOUT_IN_SECONDS
from eu.xfsc.bdd.core.server import SpringBootActuator


class SpringBootHelloWorldServer(SpringBootActuator):
    def fetch_root(self) -> requests.Response:
        return requests.get(f"{self.host}/", timeout=CONNECT_TIMEOUT_IN_SECONDS)
