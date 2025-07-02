from modules.i_interface_name import IInterface
from modules.class_implemented_derived import ClassImplementedDerived

import pytest

@pytest.fixture
def class_implemented_derived() -> ClassImplementedDerived:
   return ClassImplementedDerived()

def test_start_stop(class_implemented_derived: ClassImplementedDerived):

   assert class_implemented_derived.start() == IInterface.STATUS.OK_STARTED
   assert class_implemented_derived.stop() == IInterface.STATUS.OK_STOPPED

