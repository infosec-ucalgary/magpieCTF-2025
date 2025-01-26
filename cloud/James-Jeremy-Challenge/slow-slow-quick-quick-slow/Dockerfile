FROM nginx:1.27-bookworm

WORKDIR /challenge

RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y iproute2 iptables jq

RUN mkdir ./flag
RUN mkdir ./init

COPY src/rand-file-gen.sh ./rand-file-gen.sh
RUN ./rand-file-gen.sh > ./flag/flag

COPY src/html/ /challenge/html/

COPY src/default.conf.template /etc/nginx/templates/default.conf.template
COPY src/custom-entrypoint.sh /custom-entrypoint.sh

ENTRYPOINT ["/custom-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
