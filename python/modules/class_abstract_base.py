from i_interface_name import IInterface

from abc import abstractmethod

class ClassAbstractBase(IInterface):
    def __init__(self):
        self._my_name = "ClassAbstractBase"

    @abstractmethod
    def start(self) -> IInterface.STATUS:
        """Starts the interface. Should return a STATUS-like result."""
        pass

    @abstractmethod
    def stop(self) -> IInterface.STATUS:
        """Stops the interface. Should return a STATUS-like result."""
        pass

    def base_method(self) -> IInterface.STATUS:
        """Default implementation of baseMethod."""
        
        status = IInterface.STATUS.OK

        print(f"{self._my_name} :: {self.getStatusMessage(status)}")

        return status
