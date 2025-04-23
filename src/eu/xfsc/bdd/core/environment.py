"""
See https://behave.readthedocs.io/en/stable/tutorial.html#environmental-controls
"""
from eu.xfsc.bdd.core.steps import alias

PROD = 'PROD'
STAGING = 'STAGING'


def before_all(context: alias.ContextType) -> None:
    context.aliases = {}
