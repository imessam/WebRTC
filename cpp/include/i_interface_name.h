#pragma once

#include <string>

class IInterface {

    public:

        virtual ~IInterface() {}

        enum STATUS {
            OK,
            OK_STARTED,
            OK_STOPPED,
            
            ERROR,
            ERROR_CANNOT_START,
            ERROR_CANNOT_STOP
        };


        virtual STATUS start() = 0;

        virtual STATUS stop() = 0;

        virtual STATUS baseMethod() = 0; // base method


        virtual std::string getStatusMessage(STATUS status) const final {
            switch (status) {
            case OK:
                return "OK";
            case OK_STARTED:
                return "OK started";
            case OK_STOPPED:
                return "OK stopped";

            case ERROR:
                return "Error";
            case ERROR_CANNOT_START:
                return "Error cannot start";
            case ERROR_CANNOT_STOP:
                return "Error cannot stop";
            default:
                return "Unknown error";
            }
        }
};