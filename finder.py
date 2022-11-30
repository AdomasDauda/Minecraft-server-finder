from mcstatus import JavaServer
import threading
import argparse
import time


parser = argparse.ArgumentParser(description='files and stuff')
parser.add_argument("-o","--outputfile", type=str, help="the name of the file to put in the results")
#parser.add_argument("-e","--exluded", type=str, help="excluded ips")
parser.add_argument("-t","--threadcount", type=int, help="amount of threads that is going to be used (recomented 256)")
args = parser.parse_args()

SCAN_IP_START_FROM = 0
SCAN_IP_COUNT = 256
MINECRAFT_PORT = 25565

THREAD_COUNT = args.threadcount
OUTPUT_FILE = str(args.outputfile)
OUTPUT_RAW_IP_FILE = OUTPUT_FILE.split(".")[0]+"_raw_ips.txt"
OUTPUT_PLAYER_FILE = OUTPUT_FILE.split(".")[0]+"_found_players.txt"
OUTPUT_PLAYER_WITH_SERVER_FILE = OUTPUT_FILE.split(".")[0]+"_found_players_from_servers.txt"

files = [OUTPUT_FILE, OUTPUT_RAW_IP_FILE, OUTPUT_PLAYER_FILE, OUTPUT_PLAYER_WITH_SERVER_FILE]

if (THREAD_COUNT > 256):
    exit("TOO MANY THREADS SPECIFIED (max 256) (recomened 16)")

for file in files:
    try:
        open(file, "x")
    except:
        print(f"{file} was already there")

per_thread_ip_count = SCAN_IP_COUNT/THREAD_COUNT
left_over = SCAN_IP_COUNT % THREAD_COUNT

print(f"left over: {left_over} per thread: {per_thread_ip_count}")

class onthread(threading.Thread):
    def __init__(self, threadID, rangestart, rangeend):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.rangestart = int(rangestart)
        self.rangeend = int(rangeend)
    def run(self):
        # DRIVER CODE
        scanPorts(self.rangestart, self.rangeend)
        print (f"{self.rangestart} - {self.rangeend} finished by: " + self.name)

scanned = 0

def scanPorts(rangestart, rangeend):
    # to stop dinamicaly allocating memory
    i = 0
    j = 0
    p = 0
    k = 0
    ilist = [i for i in range(rangestart, rangeend)]
    list = [i for i in range(0, 256)]
    ############################################

    status = JavaServer
    for i in ilist:
        for j in list:
            for p in list:
                for k in list:
                    # the ip we are testing
                    ip = f"{i}.{j}.{p}.{k}"
                    # lets do some checks
                    try:
                        status = JavaServer(ip, MINECRAFT_PORT).status()
                    except OSError:
                        # if server doesnt respond
                        pass
                    else:
                        # if server responds
                        print(f"Found a server at: {ip}:{MINECRAFT_PORT} with latency: {status.latency} and {status.players.online} players online. \n")
                        with open(OUTPUT_FILE, "a") as file:
                            file.write(f"{ip}:{MINECRAFT_PORT} Latency: {status.latency} Curently online: {status.players.online}")
                            file.close()
                        with open(OUTPUT_RAW_IP_FILE, "a") as file:
                            file.write(f"{ip}:{MINECRAFT_PORT} \n")
                            file.close()

                        # try and pull players from the server
                            try: 
                                query = JavaServer(ip, MINECRAFT_PORT).query()
                                with open(OUTPUT_PLAYER_FILE, "a") as file:
                                    for player in query.players.names:
                                        file.write(f"{player}\n")
                                    file.close()
                                with open(OUTPUT_PLAYER_WITH_SERVER_FILE, "a") as file:
                                    file.write(f"{ip}:{MINECRAFT_PORT} players online: {query.players.names}\n")
                                    file.close()
                            except:
                                print(f"Could not get player names from the server {ip}")
                    status = None
                    global scanned
                    scanned += 1

for i in range(THREAD_COUNT):
    if i == THREAD_COUNT:
        # because we give more to our last thread if we didnt spread it equaly
        onthread(i, i*per_thread_ip_count+SCAN_IP_START_FROM, i*per_thread_ip_count+per_thread_ip_count+left_over+SCAN_IP_START_FROM).start()
    onthread(i, i*per_thread_ip_count+SCAN_IP_START_FROM, i*per_thread_ip_count+per_thread_ip_count+SCAN_IP_START_FROM).start()

# for measuing the rate
def rate():
    print("RATE ON")
    start = time.perf_counter()
    next_time = 5
    while True:
        if time.perf_counter() - start > next_time:
            next_time = time.perf_counter() - start + 5
            print(f"{round(scanned / (time.perf_counter() - start))} server pings/second", end='\r')

threading.Thread(None, target=rate).start()