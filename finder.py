import threading
import time
import socket
import argparse
from utils import Logger
from mcstatus import JavaServer
import struct

# whre you want to startt on 1st quadrant
START = 20

REFRESH_RATE_TIMER = 1
scanned = 0
found = 0
# how much you want to wait before closing connection
SCAN_TIMEOUT = 2
PORT = 25565

parser = argparse.ArgumentParser(description='files and stuff')
parser.add_argument("-o","--outputfile", type=str, required=True, help="the name of the file to put in the results")
args = parser.parse_args()

OUTPUT_FILE = str(args.outputfile)
OUTPUT_RAW_IP_FILE = OUTPUT_FILE.split(".")[0]+"_raw_ips.txt"
OUTPUT_PLAYER_WITH_SERVER_FILE = OUTPUT_FILE.split(".")[0]+"_found_players.txt"

files = [OUTPUT_FILE, OUTPUT_RAW_IP_FILE, OUTPUT_PLAYER_WITH_SERVER_FILE]

logger = Logger('logs.txt')

for file in files:
    try:
        open(file, "x")
    except:
        print(f"{file} was already there")

def ip_generator():
    # stop dinamicaly generating
    list = [i for i in range(256)]
    # if you want to change where you are scanning from
    for i in range(START,256):
        for j in list:
            for p in list:
                for k in list:
                    yield f"{i}.{j}.{p}.{k}"
    yield f"0.0.0.0"

ip_generator_object = ip_generator()

# for measuing the rate
def rate():
    # the amout of servers we are going to scan
    amount_of_servers = (255-START)*255*255*255
    start = time.perf_counter()
    next_time = REFRESH_RATE_TIMER + SCAN_TIMEOUT
    while True:
        if time.perf_counter() - start > next_time:
            next_time = time.perf_counter() - start + REFRESH_RATE_TIMER
            # printing stats
            try:
                print(f"{scanned / (time.perf_counter() - start)} server pings/second. Progress: {round(scanned/amount_of_servers)*100}% Estimated time left: {round(amount_of_servers/(scanned / (time.perf_counter() - start))/60/60)}hrs SCANED: {scanned} FOUND: {found}        ", end='\r')
            except ZeroDivisionError:
                print(scanned, end='\r')

threading.Thread(None, target=rate).start()

def scan_ips():
    while True:
        # https://stackoverflow.com/questions/54437148/python-socket-connect-an-invalid-argument-was-supplied-oserror-winerror
        # for measuring performance
        ip = next(ip_generator_object)
        sock = socket.socket()
        sock.settimeout(SCAN_TIMEOUT)
        try:
            sock.connect((ip, PORT))
        except TimeoutError:
            pass
        except ConnectionRefusedError:
            pass
        else:
            global found
            found += 1
            logger.addLog(f"found {ip}")
            # if connected
            with open(OUTPUT_RAW_IP_FILE, "a") as file:
                file.write(f"{ip} \n")
                file.close()

            logger.addLog(f"{ip} with socket ")
            sock.close()
            sock = socket.socket()
            sock.settimeout(SCAN_TIMEOUT)

        global scanned
        scanned += 1
    

threads_count = 10000
for i in range(threads_count):
    #spawning a bunch of threads really doesnt matter how many
    threading.Thread(None, target=scan_ips).start()

print("Finished loading threads", end='\n')