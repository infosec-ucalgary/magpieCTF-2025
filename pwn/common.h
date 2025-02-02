#ifndef __COMMON_PWN_CTF__
#define __COMMON_PWN_CTF__ 1

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
#define IP_CORS "74.6.9.245"
#define IP_EXPLO "84.9.10.5"
#define IP_HASH "167.85.6.40"
#define IP_BLUE "89.167.8.45"
#define IP_JAKE "10.0.0.254"

void ssh_login(const char *__hostname, const char *__user, const char *__dst_ip,
               const char *__src_ip);

#endif /** __COMMON_PWN_CTF__ */
