"""
Clients Runner: Client can be run natively or dockerized.
"""

import abc
import glob
from functools import cached_property
from pathlib import Path

import bash

from ..server import BaseService

CLI_JAVA_RUNNER = ("jar", "docker", "podman")
CLI_SCRIPT_RUNNER = ("script", "docker", "podman")


class Runner(BaseService, abc.ABC):
    """
    Parent Interface for Native and Dockerized Runner
    """
    @abc.abstractmethod
    def command(self, client_arguments: str) -> str:
        """Build CLI command to be executed"""


class Native(Runner, abc.ABC):
    """
    Interface for Native Runner
    """
    cli_app_location: str

    @cached_property
    def executable(self) -> Path:
        """
        Return executable path: java, python script, ...
        """
        paths = glob.glob(self.cli_app_location)

        if len(paths) > 1:
            raise RuntimeError(f"Conflicting in multiple version of client, {paths=}")

        if not paths:
            raise RuntimeError(f"No client can be found in {self.cli_app_location=}")

        return Path(paths[0])

    def is_up(self) -> bool:
        """
        If java's jar with client code available then it can be considered installed
        """
        return bool(self.executable)


class NativeJava(Native):
    """
    Implementation for Java Native Client Wrapper

    NativeJava(cli_app_location="target/trusted-content-resolver-java-client*-full.jar")
    """

    def command(self, client_arguments: str) -> str:
        """
        Call the java client resolve method
        """
        return f"java -jar {self.executable} {client_arguments}"


class NativeScript(Native):
    """
    Prepare commands to run on python virtual env
    """
    cli_app_location: str

    def command(self, client_arguments: str) -> str:
        # command = f"'{self.executable}' '--arguments ...'"
        """
        Call the python client resolve method
        """
        command = f"{self.executable} {client_arguments}"
        print(f"[PRINT:DEBUG] {command=}")
        return command


class Dockerized(Runner, abc.ABC):
    """
    Interface for Dockerized Runner
    """
    image_name: str
    implementation: str  # Literal["docker", "podman"]

    def command(self, client_arguments: str) -> str:
        """
        Call the java client resolve method
        """
        return f"{self.implementation} run --network=host {self.image_name} {client_arguments}"

    def is_up(self) -> bool:
        """
        If java's jar with client code available then it can be considered installed
        """
        print('[DEBUG] java_client.is_up enter')

        command = f"{self.implementation} images -q {self.image_name}"
        response = bash.bash(command)

        assert response.code == 0, response.stderr

        stdout = response.stdout.decode()

        return bool(stdout)
