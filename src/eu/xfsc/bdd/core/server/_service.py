"""
Base model for any service used in TRAIN-BDD
"""
import abc

import pydantic


class BaseService(pydantic.BaseModel, abc.ABC):
    """
    Common methods
    """
    @abc.abstractmethod
    def is_up(self) -> bool:
        """
        Check if service is installed or alive
        """
