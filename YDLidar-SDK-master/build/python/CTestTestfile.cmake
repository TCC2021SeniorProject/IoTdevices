# CMake generated Testfile for 
# Source directory: /home/pi/Roomba/IoTdevices/YDLidar-SDK-master/python
# Build directory: /home/pi/Roomba/IoTdevices/YDLidar-SDK-master/build/python
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(ydlidar_py_test "/usr/bin/python" "/home/pi/Roomba/IoTdevices/YDLidar-SDK-master/python/test/pytest.py")
set_tests_properties(ydlidar_py_test PROPERTIES  ENVIRONMENT "PYTHONPATH=:/home/pi/Roomba/IoTdevices/YDLidar-SDK-master/build/python" _BACKTRACE_TRIPLES "/home/pi/Roomba/IoTdevices/YDLidar-SDK-master/python/CMakeLists.txt;42;add_test;/home/pi/Roomba/IoTdevices/YDLidar-SDK-master/python/CMakeLists.txt;0;")
subdirs("examples")
