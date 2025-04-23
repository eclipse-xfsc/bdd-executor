"""Keep Here all Server Interfaces which have tp be tested"""
from ._service import BaseService
from ._spring_boot_actuator import SpringBootActuator

__all__ = ["BaseService", "SpringBootActuator"]
