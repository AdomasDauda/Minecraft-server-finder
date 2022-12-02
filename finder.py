import threading
import time
import socket
from mcstatus import JavaServer
import argparse
from utils import Logger



REFRESH_RATE_TIMER = 1
scanned = 1
# how much you want to wait before closing connection
SCAN_TIMEOUT = 2 

parser = argparse.ArgumentParser(description='files and stuff')
parser.add_argument("-o","--outputfile", type=str, required=True, help="the name of the file to put in the results")
parser.add_argument("-s","--start", type=int, required=True, help="start")
parser.add_argument("-e","--end", type=int, required=True, help="end")
args = parser.parse_args()

OUTPUT_FILE = str(args.outputfile)
OUTPUT_RAW_IP_FILE = OUTPUT_FILE.split(".")[0]+"_raw_ips.txt"
OUTPUT_PLAYER_WITH_SERVER_FILE = OUTPUT_FILE.split(".")[0]+"_found_players.txt"

files = [OUTPUT_FILE, OUTPUT_RAW_IP_FILE, OUTPUT_PLAYER_WITH_SERVER_FILE]

# whre you want to start/end on 1st quadrant
START = args.start
END = args.end

logger = Logger('logs.txt')

logger.addLog(f"New finder instance {START}:{END}")

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
                    yield "209.222.115.30"
                    #yield f"{i}.{j}.{p}.{k}"
    #we ran all the ips
    #yield f"0.0.0.0"

ip_generator_object = ip_generator()

# for measuing the rate
def rate():
    # the amout of servers we are going to scan
    amount_of_servers = (END-1-START)*255*255*255
    start = time.perf_counter()
    next_time = REFRESH_RATE_TIMER + SCAN_TIMEOUT
    while True:
        if time.perf_counter() - start > next_time:
            if scanned != 1:
                next_time = time.perf_counter() - start + REFRESH_RATE_TIMER
                # printing stats
                print(f"{round(scanned / (time.perf_counter() - start))} server pings/second. Progress: {round(scanned/amount_of_servers)*100}% Estimated time left: {round(amount_of_servers/round(scanned / (time.perf_counter() - start))/60/60)}hrs SCANED: {scanned}        ", end='\r')
                last = scanned

threading.Thread(None, target=rate).start()

def scan_ips():
    status = JavaServer("0.0.0.0", 25565)
    # make socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SCAN_TIMEOUT)
    while True:
        ip = next(ip_generator_object)
        try:
            status = JavaServer(ip, 25565, timeout=SCAN_TIMEOUT).status()
        except:
            pass
        else:
            # if connected 
            with open(OUTPUT_RAW_IP_FILE, "a") as file:
                file.write(f"{ip} \n")
                file.close()

            logger.addLog(f"{ip} with socket {status.description}")
    
        # for measuring performance
        global scanned
        scanned += 1

threads_count = 10000
for i in range(threads_count):
    #spawning a bunch of threads really doesnt matter how many
    threading.Thread(None, target=scan_ips).start()

print("Finished loading threads", end='\n')