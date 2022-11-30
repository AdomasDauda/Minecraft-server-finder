from mcstatus import JavaServer
from mcstatus import P
import threading
import argparse

parser = argparse.ArgumentParser(description='files and stuff')
parser.add_argument("-o","--outputfile", type=str, help="the name of the file to put in the results")
#parser.add_argument("-e","--exluded", type=str, help="excluded ips")
parser.add_argument("-t","--threadcount", type=int, help="amount of threads that is going to be used (recomented 256)")
args = parser.parse_args()

#excludediplist = []

# with open(args.excluded) as excludedfile:
#     lines = excludedfile.readlines()
#     for line in lines:
#         if not line.startswith("#"):
#             excludediplist.append(line)

SCAN_IP_COUNT = 256
MINECRAFT_PORT = 25565

THREAD_COUNT = args.threadcount
OUTPUT_FILE = str(args.outputfile)
OUTPUT_RAW_IP_FILE = OUTPUT_FILE.split(".")[0]+"_raw_ips.txt"

if (THREAD_COUNT > 256):
    exit("TOO MANY THREADS SPECIFIED (max 256)")

try:
    open(OUTPUT_FILE, "x")
    open(OUTPUT_RAW_IP_FILE, "x")
except:
    print("file was already there")

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
        print ("Exiting Thread " + self.name)

def scanPorts(rangestart, rangeend):
    for i in range(rangestart, rangeend):
        for j in range(0,256):
            for p in range(0,256):
                for k in range(0,256):
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
                            file.write(f"{ip}:{MINECRAFT_PORT} Latency: {status.latency} Curently online: {status.players.online} \n")
                            file.close()
                        with open(OUTPUT_RAW_IP_FILE, "a") as file:
                            file.write(f"{ip}:{MINECRAFT_PORT}")
                            file.close()

for i in range(THREAD_COUNT):
    if i == THREAD_COUNT:
        # because we give more to our last thread
        onthread(i, i*per_thread_ip_count, i*per_thread_ip_count+per_thread_ip_count+left_over).start()
    onthread(i, i*per_thread_ip_count, i*per_thread_ip_count+per_thread_ip_count).start()

