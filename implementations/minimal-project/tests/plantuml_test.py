# pylint: disable=missing-module-docstring
from pathlib import Path

from bash import bash

from eu.xfsc.bdd.minimal_project.components.plantuml import Plantuml


def test_run():
    """
    Given downloads/plantuml-mit-*.jar exists
    When run Plantuml with -auth arg
    Then match version
    """
    plantuml = Plantuml(cli_app_location=str(
        Path(__file__).parent / "../downloads/plantuml-mit-*.jar"
    ))
    command: bash = plantuml.run('-author')
    out = command.stdout.decode()

    assert '(MIT source distribution)' in out, out
