#include "class_implemented_derived.h"

#include <iostream>

ClassImplementedDerived::ClassImplementedDerived() {
    this->_my_name = "ClassImplementedDerived";
    this->_related_child_member = "related child member";
}

ClassImplementedDerived::~ClassImplementedDerived() {}

ClassImplementedDerived::STATUS ClassImplementedDerived::start() {

    ClassImplementedDerived::STATUS status = ClassImplementedDerived::STATUS::OK_STARTED;

    bool isStarted = true;

    if (!isStarted) {
        status = ClassImplementedDerived::STATUS::ERROR_CANNOT_START;
    }

    std::cout << this->_my_name << " :: " << this->getStatusMessage(status) << std::endl;

    return status;
}

ClassImplementedDerived::STATUS ClassImplementedDerived::stop() {
    
    ClassImplementedDerived::STATUS status = ClassImplementedDerived::STATUS::OK_STOPPED;

    bool isStopped = true;

    if (!isStopped) {
        status = ClassImplementedDerived::STATUS::ERROR_CANNOT_STOP;
    }

    std::cout << this->_my_name << " :: " << this->getStatusMessage(status) << std::endl;

    return status;
}