"""
PlantUML is an open-source tool allowing users to create diagrams from a plain text language
"""
import bash

from eu.xfsc.bdd.core.client.runner import NativeJava


class Plantuml(NativeJava):
    def run(self, arg: str) -> bash:
        command = self.command(arg)
        return bash.bash(command)
