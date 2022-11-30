from mcstatus import JavaServer

status = JavaServer("").status()
print(status.latency)