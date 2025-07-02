#pragma once

#include "i_interface_name.h"

class ClassAbstractBase : public IInterface {

    public:

        ClassAbstractBase();
        virtual ~ClassAbstractBase() ;

        virtual STATUS start() override = 0;

        virtual STATUS stop() override = 0;

        virtual STATUS baseMethod() override;

    protected:

        std::string _my_name = "ClassAbstractBase";
};