#pragma once

#include "class_abstract_base.h"

#include <string>


class ClassImplementedDerived : public ClassAbstractBase{
    
    public:
        // Constructor
        ClassImplementedDerived();
        // Destructor
        ~ClassImplementedDerived();

        ClassAbstractBase::STATUS start () override;

        ClassAbstractBase::STATUS stop() override;

    private:

        std::string _related_child_member;

        ClassAbstractBase::STATUS _related_child_method();
};