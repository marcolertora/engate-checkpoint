
rem Clean.
del *.nsmap dvsH.h dvsStub.h dvs*.c dvs*.cpp

rem Client source creation.
gSOAP\soapcpp2 -p dvs -n -x -L -C -c dime.h

rem Move .c files in .cpp.
move dvsClient.c dvsClient.cpp
move dvsC.c dvsC.cpp
