import threading
import time
import socket
import argparse
from utils import Logger
from mcstatus import JavaServer
import struct



REFRESH_RATE_TIMER = 1
scanned = 0
found = 0
# how much you want to wait before closing connection
SCAN_TIMEOUT = 2
PORT = 25565

parser = argparse.ArgumentParser(description='files and stuff')
parser.add_argument("-o","--outputfile", type=str, required=True, help="the name of the file to put in the results")
parser.add_argument("-s","--start", type=int, required=True, help="start")
parser.add_argument("-e","--end", type=int, required=True, help="end")
args = parser.parse_args()

# whre you want to startt on 1st quadrant
START = args.start
END = args.end

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
    for i in range(START,END):
        for j in list:
            for p in list:
                for k in list:
                    yield f"{i}.{j}.{p}.{k}"
    yield f"0.0.0.0"

ip_generator_object = ip_generator()

# for measuing the rate
def rate():
    # the amout of servers we are going to scan
    amount_of_servers = (END-1-START)*255*255*255
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
            sock.close()
        except ConnectionRefusedError:
            sock.close()
        else:
            global found
            found += 1
            logger.addLog(f"{ip} is online with open {PORT} port")
            sock.close()

        global scanned
        scanned += 1
    
def get_server_info(ip):
    try:
        status = JavaServer(ip, PORT).status()
    except:
        logger.addLog(f"{ip} is not a minecraft server")
    else:
        # if connected
        # add ip to ip list
        with open(OUTPUT_RAW_IP_FILE, "a") as file:
            file.write(f"{ip} \n")
            file.close()
        # add stuff to out file
        with open(OUTPUT_FILE, 'a') as file:
            file.write(f"{ip} Latency: {status.latency} Online players: {status.players.online}\n")
            file.close()

        # try and extract players
        try:
            query = JavaServer(ip, PORT).query()
        except:
            logger.addLog(f"{ip} was a minecraft server but has no query open")
        else:
            with open(OUTPUT_PLAYER_WITH_SERVER_FILE, 'a') as file:
                for player in query.players.names:
                    file.write(player)                
                file.close()

threads_count = 10000
for i in range(threads_count):
    #spawning a bunch of threads really doesnt matter how many
    threading.Thread(None, target=scan_ips).start()

print("Finished loading threads", end='\n')