from pathlib import Path

import bash
import requests
from behave import when, given

from eu.xfsc.bdd.core.steps import *

from eu.xfsc.bdd.minimal_project.components.plantuml import Plantuml
from eu.xfsc.bdd.minimal_project.components.spring_boot_hello_world import SpringBootHelloWorldServer


class ContextType:
    plantuml: Plantuml
    plantuml_bash_result: bash.bash
    hw_server: SpringBootHelloWorldServer

    text: str
    bash: bash.bash
    requests_response: requests.Response


@given("MIT Plantuml is downloaded")
def check_plantuml_downloaded(context: ContextType) -> None:
    context.plantuml = Plantuml(cli_app_location=str(Path(__file__).parent / "../downloads/plantuml-mit-*.jar"))
    assert context.plantuml.is_up()


@given("spring-boot-hello-world server is up")
def check_hello_world_up(context: ContextType) -> None:
    context.hw_server = SpringBootHelloWorldServer(host="http://127.0.0.1:42511")  # type: ignore[arg-type]
    assert context.hw_server.is_up()


@when("run Plantuml client with `{arg}` argument")
def run_plantuml_with_arg(context: ContextType, arg: str) -> None:
    context.bash = context.plantuml.run(arg)


@when("fetch root hello-world endpoint")
def fetch_hello_world_root_endpoint(context: ContextType) -> None:
    context.requests_response = context.hw_server.fetch_root()
