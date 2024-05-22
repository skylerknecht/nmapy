# nmapy
Python Nmap Parser

### Example usage
There are common scans that operators will run to identify live systems, open ports and running services. I follow this methodology to enumerate a client's environment.

```
skyler@debian~# git clone https://github.com/skylerknecht/nmapy
skyler@debian~# mkdir scanning
skyler@debian~/scanning# sudo nmap --initial-rtt-timeout=300ms --max-rtt-timeout=900ms --max-retries=2 -sn --reason -PE -PS3,7,9,13,17,19,21-23,25-26,37,53,79-82,88,100,106,110-111,113,119,135,139,143-144,179,199,254-255,280,311,389,427,443-445,464-465,497,513-515,543-544,548,554,587,593,625,631,636,646,787,808,873,902,990,993,995,1000,1022,1024-1033,1035-1041,1044,1048-1050,1053-1054,1056,1058-1059,1064-1066,1069,1071,1074,1080,1110,1234,1433,1494,1521,1720,1723,1755,1761,1801,1900,1935,1998,2000-2003,2005,2049,2103,2105,2107,2121,2161,2301,2383,2401,2601,2717,2869,2967,3000-3001,3128,3268,3306,3389,3689-3690,3703,3986,4000-4001,4045,4899,5000-5001,5003,5009,5050-5051,5060,5101,5120,5190,5357,5432,5555,5631,5666,5800,5900-5901,6000-6002,6004,6112,6646,6666,7000,7070,7937-7938,8000,8002,8008-8010,8031,8080-8081,8443,8888,9000-9001,9090,9100,9102,9999-10001,10010,32768,32771,49152-49157 -PU53,67-69,111,123,135,137-139,161-162,445,500,514,520,631,996-999,1434,1701,1900,3283,4500,5353,49152-49154 -iL client.scope -oA client.discovery
skyler@debian~/scanning# ./run_nmapy --file *.discovery.gnmap --display livehosts > client.live
skyler@debian~/scanning# nmap --stats-every 300s --open --reason --max-retries=2 --initial-rtt-timeout=250ms --max-rtt-timeout=900ms --max-scan-delay=5 -Pn -n -sT -p1-65535 -iL client.live -oA client.65k
skyler@debian~/scanning# ./run_nmapy --file *.65k.gnmap --display liveports --delimiter , > client.ports
skyler@debian~/scanning# nmap -Pn -sT -sV --version-all -p $(cat *.ports) -iL client.live -oA client.version
```