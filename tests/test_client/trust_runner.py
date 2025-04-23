# pylint: disable=missing-module-docstring
from pathlib import Path

import bash

from eu.xfsc.bdd.core.client.runner import NativeScript


def test_native_script():
    """
    Given a python script file examples/python_script.py
    When run the script with arg "from unitest"
    Then bash command output match
    '''
    Hello BDD: from unitest
    '''
    """
    location = str(Path(__file__).parent / '../../examples/python_script.py')
    python = NativeScript(cli_app_location=location)
    command = python.command('"from unitest"')
    bash_command = bash.bash(command)

    assert bash_command.stdout.decode() == "Hello BDD: from unitest\n"
