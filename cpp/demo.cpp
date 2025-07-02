#include "class_implemented_derived.h"

int main(int argc, char** argv) {

    ClassImplementedDerived class_implemented_derived;

    if (class_implemented_derived.start() != ClassImplementedDerived::STATUS::OK_STARTED) {
        return 1;
    }

    if (class_implemented_derived.stop() != ClassImplementedDerived::STATUS::OK_STOPPED) {
        return 1;
    }

    return 0;
} 