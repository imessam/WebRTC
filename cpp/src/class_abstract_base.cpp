#include "class_abstract_base.h"

#include <iostream>


ClassAbstractBase::ClassAbstractBase() {}

ClassAbstractBase::~ClassAbstractBase() {}

ClassAbstractBase::STATUS ClassAbstractBase::baseMethod() {

    ClassAbstractBase::STATUS status = ClassAbstractBase::STATUS::OK;

    bool isOk = true;

    if (!isOk) {
        status = STATUS::ERROR;
    }

    std::cout << this->_my_name << " :: " << this->getStatusMessage(status) << std::endl;

    return status;
}