# About
 A simple tool built to find minecraft servers on the web using the [mcstatus](https://pypi.org/project/mcstatus/) library
 
 To run:
 
  `
  python finder.py -o <outputfile.txt> -t <thread count number>  
  `
  
  It will output `outputfile.txt` that will have information about servers, and `outputfile_raw_ip.txt` for raw ips of the servers that were detected (usefull when trying to ping them for second time)  
  
  Note: Running it on high thread count is not recomended. 16 threads is enough.
  
  
  
 
# Demo
 Google colab:

![image](https://user-images.githubusercontent.com/107749872/204839162-0c145d3e-bfe1-4225-ab02-335a819a1c86.png)
 
# Depends
 [mcstatus](https://pypi.org/project/mcstatus/) - library for protocol with mc servers
