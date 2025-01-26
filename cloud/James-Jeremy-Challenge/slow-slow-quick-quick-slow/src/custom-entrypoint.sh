#!/bin/bash

set -euo pipefail

#========================================================================
# Variables.
#========================================================================
NET_INTERFACE="$(ip route show default | awk '/default/ {print $5}')"
RATE_LIMITED_NGINX_PORT="$NGINX_FLAG_PORT"

echo "INTERFACE: $NET_INTERFACE"
echo "NGINX_FLAG_PORT: $NGINX_FLAG_PORT"
echo "NGINX_HTML_PORT: $NGINX_HTML_PORT"

#========================================================================
# Cleanup any tc qdiscs, classes, and filters that we may have created
# before. It will also delete any iptables rules that may still exist.
#
# We are trapping all stop signals that docker will send and running
# this cleanup if they are caught.
#========================================================================
cleanup() {
    set +e
    echo "Cleaning up old tc qdiscs, classes, and filters"
    tc qdisc del dev "$NET_INTERFACE" root >/dev/null 2>&1

    echo "Cleaning up iptables rules and chains"
    iptables -D POSTROUTING -t mangle -o "$NET_INTERFACE" -p tcp --sport "$RATE_LIMITED_NGINX_PORT" -j QOS >/dev/null 2>&1
    iptables -t mangle -F QOS >/dev/null 2>&1
    iptables -t mangle -X QOS >/dev/null 2>&1

    ip6tables -D POSTROUTING -t mangle -o "$NET_INTERFACE" -p tcp --sport "$RATE_LIMITED_NGINX_PORT" -j QOS >/dev/null 2>&1
    ip6tables -t mangle -F QOS >/dev/null 2>&1
    ip6tables -t mangle -X QOS >/dev/null 2>&1
    set -e
}

trap cleanup SIGINT SIGQUIT SIGTERM

cleanup

#========================================================================
# Write out limits.sh. This script will be provided to the players.
#
# It does the following:
# - Creates a root HTB qdisc.
# - Creates two HTB classes, one for super low bandwidth and another
#   with faster bandwidth.
# - Creates a SFQ to help balance traffic in a qdisc class.
# - Creates tc filters that classify the traffic into the HTB classes.
# - Adds fwmarks for each CIDR range using iptables.
#
# Most of the iptables rules are added to a custom chain called QOS. A
# jump to the QOS chain is added to the POSTROUTING chain, only if the
# traffic has a dest port of nginx server that hosts the flag.
#
# The QOS chain contains an iptables rule for each CIDR. If the destination
# address is one of those CIDRs, we add a fwmark of 20. This fwmark is then
# matched by the tc filters. If tc sees the fwmark of 20, it sends the traffic
# to the faster qdisc class with more bandwidth. If it does not have this fwmark,
# then it sends it to the slow bandwidth class.
#========================================================================
cat << EOF > /challenge/init/limits.sh
#!/bin/bash

set -euo pipefail

# This script will run on server start.

#=============================================================
#
#                 ,---------------------------,
#                 |  /---------------------\  |
#                 | |                       | |
#                 | |      Good luck        | |
#                 | |     getting the       | |
#                 | |        flag!          | |
#                 | |                       | |
#                 |  \_____________________/  |
#                 |___________________________|
#               ,---\_____     []     _______/------,
#             /         /______________\           /|
#           /___________________________________ /  | ___
#           |                                   |   |    )
#           |  _ _ _                 [-------]  |   |   (
#           |  o o o                 [-------]  |  /    _)_
#           |__________________________________ |/     /  /
#       /-------------------------------------/|      ( )/
#     /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
#   /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#=============================================================

CIDRS=(
'74.122.200.0/22'
'104.197.15.74/32'
'34.123.172.192/32'
'34.125.50.224/32'
'34.125.82.130/32'
'34.134.193.138/32'
'34.138.187.10/32'
'34.150.152.190/32'
'34.162.185.129/32'
'34.162.202.37/32'
'34.162.229.32/32'
'34.162.29.153/32'
'34.162.88.79/32'
'34.23.207.105/32'
'34.85.139.176/32'
'34.85.240.93/32'
'34.86.56.118/32'
'35.202.121.43/32'
'35.225.44.167/32'
'35.231.56.118/32'
'35.237.165.17/32'
'35.243.148.182/32'
'35.245.56.67/32'
)

is_ipv4_cidr() {
    local cidr="\$1"
    [[ "\$cidr" =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$ ]]
}

is_ipv6_cidr() {
    local cidr="\$1"
    [[ "\$cidr" =~ ^([0-9a-fA-F:]{2,39}){1,4}/[0-9]{1,3}$ ]]
}

INTERFACE="${NET_INTERFACE}"
PORT="${RATE_LIMITED_NGINX_PORT}"

echo "Creating tc qdiscs and classes"
tc qdisc add dev "\$INTERFACE" root handle 1: htb
tc class add dev "\$INTERFACE" parent 1: classid 1:10 htb rate 5kbit
tc class add dev "\$INTERFACE" parent 1: classid 1:20 htb rate 100mbit

tc qdisc add dev "\$INTERFACE" parent 1:10 handle 10: sfq perturb 10
tc qdisc add dev "\$INTERFACE" parent 1:20 handle 20: sfq perturb 10

echo "Creating tc filters"
tc filter add dev "\$INTERFACE" protocol ip parent 1: prio 1 handle 20 fw flowid 1:20
tc filter add dev "\$INTERFACE" protocol ip parent 1: prio 2 u32 match ip sport "\$PORT" 0xffff flowid 1:10
tc filter add dev "\$INTERFACE" protocol ip parent 1: prio 2 u32 match ip6 sport "\$PORT" 0xffff flowid 1:10

echo "Creating iptables chains"
iptables -t mangle -N QOS
iptables -A POSTROUTING -t mangle -o "\$INTERFACE" -p tcp --sport "\$PORT" -j QOS

ip6tables -t mangle -N QOS
ip6tables -A POSTROUTING -t mangle -o "\$INTERFACE" -p tcp --sport "\$PORT" -j QOS

echo "Creating iptables rules"
for CIDR in "\${CIDRS[@]}"; do
    if is_ipv4_cidr "\$CIDR"; then
        iptables -A QOS -t mangle -d "\$CIDR" -m mark --mark 0 -j MARK --set-mark 20
    elif is_ipv6_cidr "\$CIDR"; then
        ip6tables -A QOS -t mangle -d "\$CIDR" -m mark --mark 0 -j MARK --set-mark 20
    else
        echo "Warning: \$CIDR is neither a valid IPv4 or IPv6 CIDR."
    fi
done
EOF

#========================================================================
# Run the limits.sh script that we just created above.
#========================================================================
bash /challenge/init/limits.sh

#========================================================================
# Defer the rest of the entrypoint to the default docker-entrypoint.sh
# that is bundled with the standard nginx image. This file will handle
# the CMD set in the Dockerfile.
#
# We are running this in a subshell. This allows the exec from the nginx
# entrypoint script to run, while still maintaining our SIGQUIT trap.
# This allows the cleanup to run on container stop, while still using the
# existing /docker-entrypoint.sh script from the base image.
#========================================================================
( /docker-entrypoint.sh "$@" ) &

# Wait for the above subshell to quit.
wait $!
