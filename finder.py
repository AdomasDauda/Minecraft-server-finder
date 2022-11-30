from mcstatus import JavaServer
import threading
import argparse
import time


parser = argparse.ArgumentParser(description='files and stuff')
parser.add_argument("-o","--outputfile", type=str, help="the name of the file to put in the results", required=True)
args = parser.parse_args()

MINECRAFT_PORT = 25565

# how often refresh the performance timer thing
REFRESH_RATE_TIMER = 1

THREAD_COUNT = 65536
OUTPUT_FILE = str(args.outputfile)
OUTPUT_RAW_IP_FILE = OUTPUT_FILE.split(".")[0]+"_raw_ips.txt"
OUTPUT_PLAYER_FILE = OUTPUT_FILE.split(".")[0]+"_found_players.txt"
OUTPUT_PLAYER_WITH_SERVER_FILE = OUTPUT_FILE.split(".")[0]+"_found_players_from_servers.txt"

files = [OUTPUT_FILE, OUTPUT_RAW_IP_FILE, OUTPUT_PLAYER_FILE, OUTPUT_PLAYER_WITH_SERVER_FILE]

for file in files:
    try:
        open(file, "x")
    except:
        print(f"{file} was already there")

class onthread(threading.Thread):
    def __init__(self, threadID, rangestarti, rangeendi, rangestartj, rangeendj):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.rangestarti = int(rangestarti)
        self.rangeendi = int(rangeendi)
        self.rangestartj = int(rangestartj)
        self.rangeendj = int(rangeendj)
    def run(self):
        # DRIVER CODE
        scanPorts(self.rangestarti, self.rangeendi, self.rangestartj, self.rangeendj)
        print (f"{self.rangestarti}.{self.rangestartj} - {self.rangeendi}.{self.rangeendj} finished by: " + self.name)

scanned = 0

def scanPorts(rangestarti, rangeendi, rangestartj, rangeendj):
    # to stop dinamicaly allocating memory
    i = 0
    j = 0
    p = 0
    k = 0
    ilist = [i for i in range(rangestarti, rangeendi)]
    jlist = [j for j in range(rangestartj, rangeendj)]
    list = [i for i in range(0, 256)]
    ############################################

    status = JavaServer
    for i in ilist:
        for j in jlist:
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

                        #######################################################################################################################
                        with open(OUTPUT_FILE, "a") as file:
                            file.write(f"{ip}:{MINECRAFT_PORT} Version: {status.version.name} Latency: {status.latency} Curently online: {status.players.online} \n")
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

# for measuing the rate
def rate():
    amount_of_servers = 255*255*255*255
    start = time.perf_counter()
    next_time = REFRESH_RATE_TIMER
    last_scan = 0
    while True:
        if time.perf_counter() - start > next_time:
            next_time = time.perf_counter() - start + REFRESH_RATE_TIMER
            print(f"{round(scanned - last_scan / (time.perf_counter() - start))} server pings/second. Progress: {round(scanned/amount_of_servers)*100}% Estimated time left: {amount_of_servers/round(scanned - last_scan / (time.perf_counter() - start))/60/60}hrs", end='\r')
            last_scan = scanned

threading.Thread(None, target=rate).start()

for i in range(256):
    print(f"                                                                                        ",end='\r')
    print(f"{i}/256 tread groups started",end='\r\n')
    for j in range(256):
        onthread(None, i, i+1, j, j+1).start()