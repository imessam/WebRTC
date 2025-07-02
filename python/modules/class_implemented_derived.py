from i_interface_name import IInterface
from class_abstract_base import ClassAbstractBase

class ClassImplementedDerived(ClassAbstractBase):
    def __init__(self):

        super().__init__()

        self._my_name = "ClassImplementedDerived"

        self._related_child_member = ""

    def __del__(self):
        # Destructor: cleanup resources if needed.
        pass

    def start(self) -> IInterface.STATUS:
        # Override start method.
        # Add your implementation here.
        return IInterface.STATUS.OK_STARTED

    def stop(self) -> IInterface.STATUS:
        # Override stop method.
        # Add your implementation here.
        return IInterface.STATUS.OK_STOPPED

    def _related_child_method(self) -> IInterface.STATUS:
        # Private helper method.
        # Add your implementation here.
        pass
