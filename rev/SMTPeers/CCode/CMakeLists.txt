cmake_minimum_required(VERSION 3.29)
project(MGPCTF_C_Challenge C)

set(CMAKE_C_STANDARD 11)

# Find the OpenSSL package
find_package(OpenSSL REQUIRED)

add_executable(MGPCTF_C_Challenge
        main.c
        main.c)

# Link the OpenSSL libraries
target_link_libraries(MGPCTF_C_Challenge
        OpenSSL::SSL
        OpenSSL::Crypto)
