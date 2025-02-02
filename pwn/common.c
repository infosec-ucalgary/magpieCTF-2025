#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#include "./common.h"

void ssh_login(const char *__hostname, const char *__user, const char *__dst_ip,
               const char *__src_ip) {
    // randomization
    srand(time(NULL));

    // vars for time
    char _time_buffer[TIME_BUFFER_SIZE];
    time_t _now;
    time(&_now);
    struct tm *_zone_info = localtime(&_now);

    // some flare
    printf("ssh %s@%s\n", __user, __dst_ip);
    sleep(1);

    // printing ssh banner
    strftime(_time_buffer, TIME_BUFFER_SIZE, TIME_FSTRING, _zone_info);
    printf("Linux %s 6.1.21-v8+ #1642 SMP PREEMPT %s aarch64\n", __hostname,
           _time_buffer);

    // printing last login source
    _zone_info->tm_mday = rand() % 28;
    _zone_info->tm_min = rand() % 60;
    _zone_info->tm_hour = rand() % 24;
    strftime(_time_buffer, TIME_BUFFER_SIZE, TIME_FSTRING, _zone_info);
    printf("Last login: %s from %s\n", __src_ip, _time_buffer);
}