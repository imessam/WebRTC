from abc import ABC, abstractmethod
from enum import Enum
from typing import final

class IInterface(ABC):
    class STATUS(Enum):
        OK = 0
        OK_STARTED = 1
        OK_STOPPED = 2
        
        ERROR = 3
        ERROR_CANNOT_START = 4
        ERROR_CANNOT_STOP = 5

    @abstractmethod
    def start(self) -> STATUS:
        pass

    @abstractmethod
    def stop(self) -> STATUS:
        pass

    @abstractmethod
    def baseMethod(self) -> STATUS:
        """Base method"""
        pass

    @final
    def getStatusMessage(self, status: STATUS) -> str:

        mapping = {
            IInterface.STATUS.OK: "OK",
            IInterface.STATUS.OK_STARTED: "OK started",
            IInterface.STATUS.OK_STOPPED: "OK stopped",
            IInterface.STATUS.ERROR: "Error",
            IInterface.STATUS.ERROR_CANNOT_START: "Error cannot start",
            IInterface.STATUS.ERROR_CANNOT_STOP: "Error cannot stop",
        }
        return mapping.get(status, "Unknown error")
