"""
Validate bash commands results
"""
# pylint: disable=missing-function-docstring
import re
from dataclasses import dataclass

import bash
from behave import then  # pylint: disable=no-name-in-module


@dataclass
class ContextType:
    bash: bash.bash
    text: str


@then("success command output match regexp")  # type: ignore[misc]
def match_with_regexp_success_output(context: ContextType) -> None:
    regexp = context.text.strip()

    assert context.bash.code == 0, f"Failed with code={context.bash.code} and error={context.bash}"

    stdout = context.bash.stdout.decode()
    assert re.search(regexp, stdout), f"{regexp=}\n, command output does not match {stdout=}"
