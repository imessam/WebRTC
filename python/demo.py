import sys
import os 

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
if base_path not in sys.path:
    sys.path.insert(0, base_path)

# from libs.another_module.python.modules import *

from modules.i_interface_name import IInterface
from modules.class_implemented_derived import ClassImplementedDerived

def main():

    class_implemented_derived = ClassImplementedDerived()

    if class_implemented_derived.start() != IInterface.STATUS.OK_STARTED:
        return 1
    
    if class_implemented_derived.stop() != IInterface.STATUS.OK_STOPPED:
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())