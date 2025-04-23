# pylint: disable=missing-module-docstring

from eu.xfsc.bdd.minimal_project.components.spring_boot_hello_world import \
    SpringBootHelloWorldServer


def test_fetch_root():
    """
    Test if server reply on fetch_root
    """
    server = SpringBootHelloWorldServer(host="http://127.0.0.1:42511")
    response = server.fetch_root()
    assert response.status_code == 200
