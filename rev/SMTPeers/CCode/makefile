worx: 
	cc -DSMTP_OPENSSL smtp.c -c -o smtp.o
	cc -DSMTP_OPENSSL main.c -c -o main.o
	cc main.o smtp.o -o smtp_test -lssl -lcrypto
