#ifndef __MAGPIECTF_2025_PWN__
#define __MAGPIECTF_2025_PWN__ 1

// return codes
#define ERR_CHALLENGE_FAILURE 2
#define ERR_NO_MALLOC 3
#define ERR_OTHER 4
#define ERR_NO_FLAG 5

// flag related
#define FLAG "flag.txt"
#define FLAG_SIZE 64

// for flare
#define TIME_BUFFER_SIZE 0x40
#define TIME_FSTRING "%a %b %d %k:%M:%S %Z 1933"

// for plot
#define IP_CORS "10.0.0.254"
#define IP_EXPLO "84.9.10.5"
#define IP_HASH "167.85.6.40"
#define IP_BLUE "89.167.8.45"
#define IP_JAKE "52.129.50.254"

#define IP_NETRUNNER1 "52.129.50.30"
#define IP_NETRUNNER2 "52.129.50.31"

void ssh_login(const char *__hostname, const char *__user, const char *__dst_ip,
               const char *__src_ip);

#endif /** __MAGPIECTF_2025_PWN__ */
