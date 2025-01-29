from scapy.all import *
import random
from datetime import datetime, timedelta

# Base start time range for packets (randomized per packet)
base_start_time = datetime(1970, 1, 11, 0, 0, 0)  # Earliest possible date
end_start_time = datetime(1970, 1, 11, 23, 59, 59)  # Latest possible date

# Jake's IP address
jake_ip = "192.168.127.12"

packets = []  # List to store packets


# Function to generate random start times within the range
def random_start_time():
    delta = end_start_time - base_start_time
    random_seconds = random.randint(0, int(delta.total_seconds()))
    return base_start_time + timedelta(seconds=random_seconds)


# Function to generate random MAC addresses
def random_mac():
    return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])


# Function to generate random IPv4 addresses
def random_ip(exclude=None):
    while True:
        ip = ".".join([str(random.randint(1, 254)) for _ in range(4)])
        if ip != exclude:
            return ip


# Function to create TCP packets
def create_tcp_packet(src_ip, dst_ip, sport, dport, payload=""):
    return Ether(src=random_mac(), dst=random_mac()) / IP(src=src_ip, dst=dst_ip) / TCP(sport=sport, dport=dport,
                                                                                        flags="PA") / Raw(load=payload)


# Function to create UDP packets
def create_udp_packet(src_ip, dst_ip, sport, dport, payload=""):
    return Ether(src=random_mac(), dst=random_mac()) / IP(src=src_ip, dst=dst_ip) / UDP(sport=sport, dport=dport) / Raw(
        load=payload)


# Generate packets related to Jake with the embedded flag
flag = "MAGPIE{aHR0cHM6Ly93d3cueW91dHViZS5jb20vc2hvcnRzL0xRQmV3UEZQM2hB}"  # Define the flag

# Optionally split the flag into parts
split_flag = ["MAGPIE{Part1-aHR0cHM6Ly93d3cue", "Part2-W91dHViZS5jb20vc2hvcnR", "Part3-zL0xRQmV3UEZQM2hB}"]

for i in range(50):  # 50 packets linked to Jake
    if i == 25:  # Embed the full flag or parts
        # Uncomment below to split flag across multiple packets
        packets.append(create_tcp_packet(jake_ip, random_ip(), random.randint(1024, 65535), 80, payload=split_flag[0]))
        packets.append(create_tcp_packet(jake_ip, random_ip(), random.randint(1024, 65535), 80, payload=split_flag[1]))
        packets.append(create_tcp_packet(jake_ip, random_ip(), random.randint(1024, 65535), 80, payload=split_flag[2]))

        # Embed the full flag in one packet
        #clue = flag
    else:
        clue = random.choice([
            "CIA-Contracts",
            "Krypto-sold-for-money",
            "Jake_rules",
            "Hacking_legacy",
            "Krypto_blackhat",
            "Crypto_exposed",
            "Secret_algo",
            "Hidden_in_plain_sight",
            "Krypto_infiltrated",
            "Exploiting_weakness",
            "Encrypted_trade",
            "CIA_breach",
            "Krypto_corruption",
            "Hash_reversed",
            "Eternal_puzzle",
            "Silent_witness",
            "Silent_infiltration",
            "Money_over_morals",
            "Krypto's_double_game",
            "Underground_deals",
            "The_ultimate_betrayal",
            "Cryptic_plan",
            "Krypto_shady_deals",
            "Cold_case_reopened",
            "Top_secret_tech",
            "Encrypted_footprint",
            "Exposed_trade",
            "CIA_insider",
            "Backdoor_witness",
            "Spying_for_Krypto",
            "Hidden_solutions",
            "The_real_Krypto",
            "Blackhat_snitch",
            "System_compromise",
            "Puzzle_solved_in_code",
            "Deep_web_dealings",
            "Coded_in_secret",
            "Undetected_infiltration",
            "Exploits_unleashed",
            "Backdoor_breach",
            "Infiltrator_unmasked"
        ])

    pkt = create_tcp_packet(jake_ip, random_ip(), random.randint(1024, 65535), 80, payload=f"{clue} {i}")
    packets.append(pkt)

    # Generate a random start time for the packet
    random_time = random_start_time().timestamp()

    # Ensure the timestamp is within the valid range for PCAP
    if random_time < 0:
        random_time = 0  # Clamp to 0 if negative
    elif random_time > 4294967295:
        random_time = 4294967295  # Clamp to the max value

    pkt.time = random_time

# Generate noise packets to confuse users with more realistic domains
for i in range(1950):  # Remaining packets for noise
    protocol = random.choice(["TCP", "UDP", "ICMP", "DNS"])
    src_ip = random_ip(exclude=jake_ip)
    dst_ip = random_ip(exclude=jake_ip)

    if protocol == "TCP":
        payload = random.choice([
            f"Uploading file {i}.pdf",
            f"Session {i}: Data transfer",
            f"HTTP/1.1 200 OK - Response",
            f"POST /api/upload Data {i}",
            f"GET /home HTTP/1.1"
        ])
        packets.append(
            create_tcp_packet(src_ip, dst_ip, random.randint(1024, 65535), random.randint(1, 1024), payload=payload))

    elif protocol == "UDP":
        payload = random.choice([
            f"Querying database {i} records",
            f"Video stream {i}: Data",
            f"DNS request to resolve www.example{i}.com",
            f"VoIP call setup message {i}",
            f"Broadcast message {i} from server"
        ])
        packets.append(
            create_udp_packet(src_ip, dst_ip, random.randint(1024, 65535), random.randint(1, 1024), payload=payload))

    elif protocol == "ICMP":
        packets.append(Ether(src=random_mac(), dst=random_mac()) / IP(src=src_ip, dst=dst_ip) / ICMP(type="echo-reply"))

    elif protocol == "DNS":
        domain = random.choice([
            f"server{i}.corp.com",
            f"api{i}.cloud.net",
            f"mail{i}.tech.org",
            f"db{i}.secure.io",
            f"vpn{i}.private.co",
            f"files{i}.storage.biz",
            f"www{i}.data-center.org"
        ])
        packets.append(
            Ether(src=random_mac(), dst=random_mac()) / IP(src=src_ip, dst=dst_ip) / UDP(sport=53, dport=53) / DNS(rd=1,
                                                                                                                   qd=DNSQR(
                                                                                                                       qname=domain)))

    # Generate a random start time for the noise packet
    random_time = random_start_time().timestamp()

    if random_time < 0:
        random_time = 0
    elif random_time > 4294967295:
        random_time = 4294967295

    packets[-1].time = random_time

# Write packets to a PCAPNG file
try:
    wrpcap("mansion-security.pcapng", packets)
    print("PCAPNG file created: mansion-security.pcapng")
except Exception as e:
    print(f"Error writing PCAP: {e}")
