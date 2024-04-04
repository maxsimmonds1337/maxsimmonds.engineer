# Hacking a Snaptain A15F Drone
---

## [29/03/2024]
Recently, I dug out my old toy drone that I bought of Amazon for 35£, on a half price deal. It was a Snaptian A15F, which has an HD camera, remote control, and app (called Snaptain Mate), which allows you to view the live stream of the HD video. It also allows you to control the drone via phone only, pretty neat.

Anyway, my phone (IPhone 14 Max) seems to be no longer supported, I can't connect to the drone and get a steam of video. So that got me thinking, the way you connect to the drone is via an unsecured WiFi connection. This thing is literally a flying router!

Great! I can connect to my drone, get a video stream, and maybe even write my own flight software and fly it from my laptop (though, I'm not yet sure on the input, keyboard might be a bit werid, maybe magic mouse or track pad?).

My objectives are:

- Get a live video stream
- Control the drone from my laptop
- Fly from my laptop alone (using the live video stream)

So, here's my log of what I've been doing, to try and get the above!

### nmap
The first thing I did was do a network scan and see what's going on in this drone. Initially, I ran a simple port scan, and didn't see anything (only that ports 5000 and 7000 are open, but on my laptop, which was weird.) No other open ports. Then, I realised, I can use the -Pn flag. This was hinted in nmaps output when I tried scanning previously:

```
Note: Host seems down. If it is really up, but blocking our ping probes, try -Pn
```

So, here's the output:

```
max@Maxs-Air dronehack % nmap 192.168.201.1 -Pn
Starting Nmap 7.94 ( https://nmap.org ) at 2024-03-29 19:18 GMT
mass_dns: warning: Unable to determine any DNS servers. Reverse DNS is disabled. Try using --system-dns or specify valid servers with --dns-servers
Nmap scan report for 192.168.201.1
Host is up (0.057s latency).
Not shown: 995 filtered tcp ports (no-response)
PORT      STATE SERVICE
21/tcp    open  ftp
2121/tcp  open  ccproxy-ftp
6699/tcp  open  napster
7070/tcp  open  realserver
50000/tcp open  ibm-db2
```

That's a whole lot of ports! I was surpised to see ibm-db2 server running there, but I think it's unlikely it's running that. More likely that it uses the same port and nmap is just guessing.

Anyway, I played around establishing some TCP connections, seeing what I got. I did get a random stream from one of the ports (I forget which one now), but I got something very interesting from port 2121:
```
"220 Welcome to Stupid-FTPs server"
```

Well that's interesting! Obviously, I immediatly googled to see what results I'd get, and I saw a repo called Stupid-FTPd server. Super weird that this drone would be using code from a repo, that's barely got any stars, PRs etc. Just looks kinda like a hobby project. In any case, here's the [link](https://github.com/gamman/stupid-FTPd/) . It turns out to be super useful to have the source code, I could see all the commands available, defualt conf, etc. I tried the default user name and pass given in the default conf, but no success.

So, my next step was to write a bruteforce method. I found some generic default FTP user/passes [here](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt). A simple python script to loop through them:

```python
import ftplib

HOST = '192.168.201.1'
PORT = 2121

server = ftplib.FTP()
success = False

while not success:
    # Open the userlist file for each iteration to reset the iterator
    with open("userlist.txt", "r") as unamelist:
        for uname in unamelist:
            uname = uname.strip()  # Strip newline characters
            # Reopen the passlist file for each iteration to reset the iterator
            with open("passlist.txt", "r") as passlist:
                for passw in passlist:
                    passw = passw.strip()  # Strip newline characters

                    print(f'trying {uname}:{passw}')

                    try:
                        server.connect(HOST, PORT)
                        server.login(uname, passw)
                        success = True
                        break  # Break out of the inner loop if login is successful

                    except Exception as e:
                        print(f"Server response: {e}, trying again...")

            if success:
                break  # Break out of the outer loop if login is successful

if success:
    print(f'Success! {uname}:{passw}')
else:
    print('Credentials not found')

# You don't have to print this, because this command itself prints directory contents 
server.dir()
```

But no luck :(.

# [30/03/24]

So I left the brute force code running last night, until the drone battery died and it stopped:
<img width="395" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/7cc5d465-8a26-470f-9ea3-419478455282">
No luck, as you can see. I was trying variations of the SSID that the drone has. Previously, I know old sky routers (back when WEP was used!) used to have part of the WEP key in the SSID.... Stupid, I know. But, I thought perhaps something similar was happening here, maybe the FTP PW was part of the SSID, to make some sort of automation easier when flashing the drones, or some such thing. Well, if that's the case, I couldn't get it to work. I'm beginning to worry that the pass/user is randomly assigned, or is something that's not easily bruteforced.

An issue I came across is that each connection/test takes ~3s. That does not scale well. While I can take apart a drone battery, and wire it up to a bench supply, so I could have the drone running indefinitely, 3s for every attempted will take ages, even longer since I can't even be sure of the username! Apparently an app called hydra, with concurrent connections, might be a better way forward, but let's see how metasploit handles this...

## Metasploit

I haven't used Metasploit before, but after googling looking for FTP exploits, it looks like it might be useful. Specifically, it has a DB of exploits you can search through, so let's see what it can do. First, I ran an nmap scan through metasploit:

<img width="1708" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/75959c96-df8c-4bd9-a2a3-e5ddda18b717">

So, a little bit more info than what I got when I did a native nmap scan, but nothing that amazing. However, it does seem to think that port 7070 is the video stream (given that, for some reason, it's talking about a doorbird, which is a video doorbell.). Also, it's captured the data that's spewed out of port 50000 when a TCP connection is established, so that's cool. Anyway, I check the DB, and no luck for an exploit for stupidFTP:

<img width="224" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/bc4e5ac3-cbd9-4176-ac1f-edc39af5ecc3">

No luck for the doorbird either. I searched for FTP, which as you can imagine, had many hits, and tried out a few that seemed platform agnostic:

<img width="531" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/aa55bcd9-f67c-4431-bdd4-8d5e7df2d850">

No luck there either :( I think it catches an exception because, when I try to login manually with anon, it returns a server error and closes the connection. I tried a BF method too, but seems metasploit has the same issue as my code, single connections and not concurrent, so taking a long while. The last password in this list is kinda how I feel right now:

<img width="729" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/47756d2c-a51f-4ad0-8e77-f7545812e097">


## TCPDump
So, wireshark didn't seem to be working. I reviewed some previously captured data from when I connected a phone to the drone, and used my laptop for packet sniffing. I noticed that the version number is updated on the app after connecting to the drone, so that means some data's been sent - but my laptop didn't catch it. So Wireshark seems to be having some issues.

# [2/04/2024]

So, some updates:

- I got wireshare working. There were two issues, one, apparently, having WS in promiscious mode isn't enough, you also need to have it in [monitor mode](https://wiki.wireshark.org/CaptureSetup/WLAN) . Secondly, when it's in monitor mode, you can't be connected to a wifi station at that point. So, with that in mind, I was able to get some data (see below!)

- Hydra wasn't working. Well, it was, but it wasn't. While I can make up to 8 concurrent connections to the drone's FTP server (that speeds up my bruteforcer by 8 times!) I'm still no closer to hacking it. I tried multiple passwords/users etc. But since I can't even know the username, I have to also go through a username list and a password list (or attempt a bruteforce, which, for context a 5 char password consisting of [a-z][A-Z][0-9] is 4 billion passwords. I can manage 8 tests every 3 seconds, so about 2 a second, that's 2 billion seconds, a long time!)

<img width="1336" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/fe4d27b8-bf8c-47cd-9e67-6b7b49478b2b">

Above is an image of hydra in action, with concurrent requests. Very cool, but not likely to result in anything. I dabbled with using an RPI, and hard wiring a bench power supply to the drone, and just leave it running, and maybe I'll do this later. I had just about managed to set the pi up so that I could connect to it over SSH via the ethernet port (on my wifi) and then have it's wifi adapater connect to the drone (on a different network, 192.168.201.X) for the hacking, but that's as far as I got. Remember the objectives, I tell myself!)

So, I think I will drop the attempt, for now, at gaining access to the FTP server. It's not that important for my objectives anyway, which are to fly the drone from my laptop. Let's get back to wireshark...

## Wireshark attempt 2

<img width="1710" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/a95caa51-0e2c-42e3-9e76-bfffe7f347d0">

So, this time with WS running in monitor mode, I connected to the drone via my wife's phone (who's successfully connects, unlike my iphone 14 MAX, here's is just an Iphone 14) and captured all the data. 

### Port 6699

On port 6699, the one that I currently suspect send the video data, I got this amazing data dump, you can see above. Now, extracting the data we can read it a little more clearly (its JSON format):

```
"CMD": 0,
"PARAM": {
    "M_LED_MODE": 1,
    "M_AWB": 0,
    "M_AE": 0,
    "M_CTS": 0,
    "M_BHT": 0,
    "Wifi_Param": {
        "ssid": "SNAPTAIN-A15-GD0214",
        "ap_head": "SNAPTAIN-A15-",
        "channel": "2",
        "hw_mode": "g",
        "pass_phrase": "12345678",
        "mac": "E8E380B179A8"
    },
    "M_CARD": {
        "online": 0
    },
    "Sensor_Param": {
        "saturation": 0,
        "brightness": 0,
        "contrast": 0,
        "flip": 0,
        "angle": 0,
        "flow_x": -1,
        "flow_y": -1,
        "flow_sensitivity": 30
    },
    "FirmWare": "3.1.00",
    "build_date": "Jul  8 2020",
    "build_time": "14:03:25",
    "baud_rate": "115200",
    "flow_protocol": "1",
    "client": "XA",
    "app_flag": ""
},
"RESULT": 0
```

Now, this explains how the app version is received on the app (and what first tipped me off that, while my phone doesn't receive a video stream, it does at least connect to the drone and receive _some_ data, as this version appears in the app, maybe i'll do a data dump of my phone at some point and compare). Interestingly, it yeilds a passcode for the wifi, but the wifi doesn't actually need a pass. I, of course, tried this pass with a few user names (user, root, snap, snaptain, admin, etc) but no luck. Oh well.

Now, I wonder if the ```CMD``` param is how we send commands to the drone? Something I'll look at later too. 

So, back to the other ports we have available. Metasploit gave a better service description that what I could get with native nmap, here's a reminder:

[21] - Stupid FTP
[2121] - Stupid FTP
[6699] - Napster?
[7070] - Door Bird
[50000] - ibm db2?

The two with question marks, I'm guessing, are ones it can't verifiy through any output. 6699 is the port that we recived data about the wifi etc. Let's take a look at some of the output from the other ports

### Port 7070

So, port 7070 is the one that nmap thinks is the RTSP port. I decided to run an nmap script, in fact all the scripts that relate to RTSP:

<img width="775" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/c01dfb09-aef6-457b-ad17-6e8ff9ac81f2">

Unfortunately, I didn't get much. I can see that it is indeed an RTSP protocol, as I can see the RTSP methods. Ideally, I would have liked the URL. Usually, it's something like:

```rtsp://<ip>:<port>/route/for/stream```

I guess we'll have to try and guess it :/. Oddly enough, I'm not seeing any packets in wireshark with the stream up, I thought I would, but apprently not!

I've tried accessing many URLs, I even found the documentation for a doorbird that uses RTSP, to see what the route might be, but no luck. I even tried BF all of [these](https://raw.githubusercontent.com/nmap/nmap/master/nselib/data/rtsp-urls.txt) with the following:

``` python
import requests

def check_rtsp_url(url):
    try:
        response = requests.options(url)
        if response.status_code == 200:
            print(f"Valid RTSP URL found: {url}")
        else:
            print(f"Not a valid RTSP URL: {url}")
    except Exception as e:
        print(f"Error occurred while checking URL {url}: {e}")

def main():
    # IP address and port
    ip_address = "192.168.201.1"
    port = "7070"

    # Path to the word list containing possible routes for RTSP
    wordlist_path = "wordlist.txt"

    # Read the word list
    with open(wordlist_path, "r") as file:
        wordlist = file.readlines()

    # Iterate over each word in the word list and construct RTSP URLs
    for word in wordlist:
        route = word.strip()
        url = f"rtsp://{ip_address}:{port}/{route}"
        check_rtsp_url(url)

if __name__ == "__main__":
    main()
```




Someting seems odd, because I think I should be seeing more activity on wireshark than what I am. I think the next step will be sniff packets with a Remote Vitual Interface, as explained here (https://www.linkedin.com/pulse/easy-guide-apple-ios-packet-capture-amit-singh/)[https://www.linkedin.com/pulse/easy-guide-apple-ios-packet-capture-amit-singh/] 







