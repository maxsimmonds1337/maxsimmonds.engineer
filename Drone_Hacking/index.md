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

<img width="1822" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/8dcd8222-4286-4127-a415-790345b9e432">

I only got one successfull packet port 7070, see above. Now, obviously, I can't tell from the data if it's an image or not. So, let's try to capture a stream from it!

I've had little success capturing packets with wireshark. I only seem to get a few, even though my phone clearly sees a video stream. Maybe I need a packet capture software on my phone instead. Anyone, I started looking more into RTSP, and specifically that with door bird, the service that was mentioned with nmap. I did another scan:

So I can see which options I can use. Now, let see if we can get nmap to tell us the URL...

<img width="760" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/a8868d2a-723f-4a9c-bb76-9ad64c9eb846">

Weeeeellll, crap. I ran all the scripts that nmap has available for RTSP, and was hoping it might come up with the url I need to hit, but nope. All it shows, which is interesting in some ways, are the the methods available to me for RTSP. I suppose that shows it is indeed an RTSP port, and at least I know what I can try and send later. 

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
        pass
    # print(f"Error occurred while checking URL {url}: {e}")

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

I tried bruteforcing the URL with a [list](https://raw.githubusercontent.com/nmap/nmap/master/nselib/data/rtsp-urls.txt) of commonly used routes (RTSP is in the format rtsp://<ip>:<port>/route/to/stream), with the above program, but no luck :( And, what's weird, is that I don't see the RTSP stream in wireshark, so I think it's not capturing all the available packets. I think, the best thing to do now, it to sniff packets directly from my phone, luckily for us, apple has a great way of doing it....

# [4/4/24]

## **sniff sniff** smells like TCP!

<img width="1710" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/75ab832d-ba4c-4c49-b048-b955cecb4da2">

As you can see from the above image, I had a much better response with wireshark this time around, what did I do differently, you ask? Well, let me tell you! I plugged my phone into my Mac, and found its UUID from going into "finder", and clicking on the my Iphone under devices, and then click just under the IPhone name, where it shows how much battery it has, and it cycles through some information about your phone. The UDID is there too!

Then, using rvictl, I start a device using that UDID:

```rvictl -s <UDID>```

It'll say something like ```Starting device UDID [SUCCEEDED] with interface rvi0```. Now we can use the rvi0 interface in wireshark, and see all the packets (as you can see in the image above!).

So, A few intesting points:

- You can clearly see the DHCP server in action, establishing an IP address for the phone (initially, a NAK is sent, negative acknowledgement, probably becauase it usually tries to get 192.168.201.20 first, and I had two phones connected). Then an offer is sent, and and ACK to accept it
- A lot of info is being sent over port 6699 (more on that later) each push (PSH) is responded with an ACK, to say it's been recevied
- The same for ports 7070 and 50000, though it can't be seen in this screenshot

 Let's take a closer look at these ports!

## Port 6699
 
<img width="1667" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/87dd68c1-abba-479a-8625-c3a6e392aaf1">

The first packet that's sent with data on port 6699 is shown above. Looking at it's payload, we see:

```json
{
  "CMD" : 79,
  "PARAM" : 1
}
```

So it looks like we can send cmds over port 6699, currently we don't know what the numbers mean. I can either hit each button on the phone controller in turn, and check the cmds sent, or, and somewhat more interestingly, I can see if I can still get access to the firmware (I have plans for hardware hacking later if I can't get an FTP user/pass over the air!)

There's a whole host of data being sent over port 6699, some more examples:

```json
{
    "REPORT" : 3,
    "PARAM" : {
        "rssi": -39
    }
}
```

```json
{
  "CMD" : 11,
  "PARAM" : {
    "num" : 1,
    "delay" : 0
  }
}
```

```json
{
  "CMD" : 73,
  "PARAM" : {
    "width" : 1920,
    "height" : 1080
  }
}
```

```json
{ "CMD": 73, "RESULT": 0 }
```

I think, at some point, we'll have fun sending these commands. But for now, let's move on to port 50000!

## Port 50000

<img width="1665" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/36d41cba-43c0-469d-baf0-41b05145358e">

Port 50000 isn't really that interesting, it seems to be a heart beat or something similar. As can be seen from above, the drone sends a pattern of bytes: ```66 26 00 00 00 00 00 00 00 26```. This is then ACKd each time. It seems to be the same string each time, here's a few:

1 | 66 26 00 00 00 00 00 00 00 26
2 | 00
3 | 66 26 00 00 00 00 00 00 00 26
4 | 66 26 00 00 00 00 00 00 00 26

You get the point.... I think the packet maybe got dropped or something.

# [09/04/24]

I've been working on this on and off for a few days now, but haven't written it up, so will do that now. I've done two main things since.

## FTP Attempt 2

Not much to report here, I thought that if I tried to access the file storage via the phone, it might send the user/pass over the air unencrypted. Great logic, unfortunatly, the app doesn't actually check the drone's storage, rather, it uses your phone's storage :( Seems that, when you click to take a photo or video, your phone stores the stream directly to your device, and not to the drone locally. I noticed in a previous TCP packet (on port 6699) mentioned an "M_CARD":

```json
    "M_CARD": {
        "online": 0
    },
```

So, the system itself doesn't think it has a memory card (and I checked the hardware too, see next section). I wonder if I can send an update to make it think it has a memory card, and then search for FTP packets, but that's for later.

The long and short is that, I didn't find the user/pass. I search for a packet containing the string "user" or "pass" or even "stupid" (since that's the name of the ftp server) but no dice. Anyway, moving on, let's see if we can get a console read from hardware hacking!


## Hardware Hacking

![46460F59-1AEA-4B82-8846-9D62DB39DA38_1_102_o](https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/a6f7be57-d098-4ac5-8f8d-c061fa3857ff)

So! I decided to solder some wire to all the test pins I could find. Most of them had some silkscreen related to a UART (TX, RX, etc). Others, I couldn't read, so I soldered to them any way. I also soldered some wires to the battery input, and set the current limit to 1A, and the voltage to 4V (replicating the battery). As you can see from the above image, it worked!

Sadly though, with an Arduino as a basic USB to serial decoder (and then later, my oscilliscope) I didn't get anything decent.

![EEE47BBD-D37E-47C4-B14C-EEE05AE62C69_1_102_o](https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/20574157-8f18-4180-87e2-ae3405ca8e45)

This is all I could see on every pin, but it was late (as you can tell from the poor lighting!). I think it's worth another shot though at a later date, because I think we could be on to something. I found this post about another drone, and they looked like they're doing something similar! https://www.reddit.com/r/drones/comments/13e5c1s/hacking_a_dronex_pro_air_camera/ Anyway, I've been quickly typing all this up just to keep track of my notes, it's a little all over the place and I tried a few more things that I haven't written, but that's the main ones. Tomorrow I might look more at the hardware hacking!

# [15/04/24]

It's been a few days since I've done any drone hacking, mostly because I'm running out of ideas and things to try. So far, I have access to the video streams (though, I haven't tried changing to the bottom camera yet, might do that soon!), I can see commands being sent, and that's about it! I was unsuccessful with my hardware hacking; while I can see a UART datastream, I haven't been able to get any discernable information. I've ordered a [UART to USB converter](https://www.amazon.co.uk/dp/B075N82CDL?psc=1&ref=ppx_yo2ov_dt_b_product_details), that should be arriving today:

<img width="572" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/5fdb0256-30c3-40aa-847a-09c2d4567546">

It's a very simple device, but it should allow me to easily attach to the drone, and then run a terminal to see the datastream. I can then easily switch board rates, etc, more easily that with an arduino. I think the issue with using my scope is that packets of data are sent very far apart, which means that my scope doesn't have enough memory to hold them all. At least, that's why I hope I'm not seeing anything!

Any way, in the meantime, I've started working on my [PC remote controller software](https://github.com/maxsimmonds1337/flight_controller). I envision it to look something like this:

![image](https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/37f1c1d8-0d9f-4e42-ad4b-c9db4336356e)


I will make a seperate post about that once it's written!

# [22/05/24]
It's been a while since I've been doing any drone hacking, but I've found some time to take a look again. My Ipad still works with the drone app, which means I can easily stream video and capture all the packets I want! Mostly, I've been working on a flight controller app, a python app that connects to the drone, shows me the video stream, and I can "send" take off and land commands (as of yet, it doesn't actually send a take off cmd, which leads me to my next round of hacking...)

## CMD lists!

The following are all sent on port 6699.

When presseing a button in the drone app, I can see things like below, being sent over TCP:

```
{ 
 "REPORT": 3, 
 "PARAM": 
  { 
    "rssi": -39 
  } 
}
```

Now, out of interest, I can see that there are 3 bars on the battery level display in the app. So, I wonder if that's what the report is. RSSI is kinda obvious, that'll be the drone to controller signal, currently it's showing full signal (4 bars).

Now, if I press to take an image, I see:

```
{
  "CMD" : 11,
  "PARAM" : {
    "num" : 1,
    "delay" : 0
  }
}
```

This looks like CMD 11 is to take a photo, and that we require 1 image, with no delay (I'm presuming!). Now let's see what happens if I press video!


```
{
 "CMD": 4,
 "RESULT": -1
}
{
 "CMD": 5,
 "RESULT": 0
}
```

Looks like the start and finish of the video. Now, I don't know how the video is recorded/stored, but it's still something!

## Roll/Pitch/Yaw, Up, and Down

On port 50000 I saw a lot of the same data being sent, initially I thought maybe this was a heartbeat or something:

```
66240000000000000024
```
This is being sent from the drone to the controller. However, data going from the controller to the drone has a pattern, many of them are like this:

```
6614808080800000000000000000000000000099
```

but, If I move the stick forward (IE, tell the drone to go forwards) I see, at max speed:

```
66147ebf8080000000000000000000000000c199
```

Both start with 66, and end with 99. Almost like quote marks, or start/end bits. Over the next few days, I'll try to decode the other bytes, I suspect they are intensity values for the roll/pitch/yaw and altidude (up/down) with 80 probably being rest.

# [25/05/24]

Okay, so I found a few things out. I found a [blog post](https://hackaday.io/project/19356-reverse-engineering-a-promark-vr-toy-drone/log/51749-comm-protocol-between-camera-and-drone-controller) post that leads me to believe that I'm on the right track regarding the protocol for sending direction cmds to the drone. It also pointed out, rather obviously now I think about it, that 0x66 + 0x99 = 0xFF! So makes sense as a start stop bytes. I also think there's some XOR checksum in there, but I'll look more into this later. Right now, what bothers me, is the laggy as hell video stream. It's clear as day on the app, but with my python code for RTSP streaming, and VLC, it's dog crap.

## [RTSP or not RTSP?]

It got me thinking, maybe, since I see raw TCP packets over port 7070 that it was using a custom protocol for sending them, or it was raw encoded bytes over TCP or something like this, for latency reasons. However, a brief chat with chatGPT and I realised, wireshark assumes the protocol based on the port that's being used. So, I added port 7070 to the RTSP protocol settings in the wireshark preferences, and hey presto!

<img width="1710" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/78c26f28-d93b-4904-8a92-34d12ff69df6">

I started getting things that looked more like RTSP! Then, I decided to search the packets for text containing the elusive RTSP, and, yep, you guessed it, I found something!

<img width="1710" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/62184d4d-214b-488e-b4aa-41df507cba6a">

This is a teardown signal, that I think closes the RTSP streaming. I pressed the "stop" button a few times in the app, so I think perhaps it sends this cmd when doing so! But, this proves the RTSP url I've been using (which, I found on the web from a totally different drone, it just so happened to use the same URL). This is good news, because it means that this must be the source of the video, and there isn't some other stream that low latency that I'm missing!

I recently found out about the "follow stream" feature of wireshark, it's so helpful for things like this. I've found a packet of interest, and I want to see all the payloads sequentially. I highlight the packet, right click -> Follow -> TCP Stream, and boom:

<img width="1143" alt="image" src="https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/e59c3970-70ec-41a2-8cb9-b0d4e759d7c0">

# [26/05/24]

Okay, so, I can clearly see the URL now, but as I said before, it's laggy as hell over VLC or my python code. So, I think my next plan is to see if I can record a stream, and play it back. 

## Recording a RTSP stream

There's a few options to record a stream, VLC, mpv, or FFMPEG to name a few. I briefly tried them all, and seemed to have the most success with mpv, so will look into that more deeply.

# [05/04/25]

So it's been a while since I looked into this (actually, close to a year!). I recently started a new job at Starship, a robot delivery service. They use, as you would expect, videostreams to help remotely assist bots. It got me excited about being able to hack this drone and fly it from my laptop again. 

## RTSP

I've been reading more about RTSP, and wanted to write a barebone client in Go. I've been able to successfully connect to the drone with TCP on port 7070, and issue an `OPTIONS` cmd:

<img width="1710" alt="image" src="https://github.com/user-attachments/assets/69fe15d7-c6b2-42b7-84f7-896b85d59222" />

I actually managed to get a pretty good connection going:

```
max@Mac go % go run main.go
Connecting to RTSP stream...
Connection established!

Enter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): OPTIONS

Enter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): 
Received:
RTSP/1.0 200 OK
CSeq: 1
Date: Thu, Jan 01 1970 01:14:49 GMT
Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE, GET_PARAMETER, SET_PA
RAMETER


DESCRIBE

Enter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): 
Received:
RTSP/1.0 404 Stream Not Found
CSeq: 2
Date: Thu, Jan 01 1970 01:15:05 GMT


^C
Received signal: interrupt
max@Mac go % go run main.go
Connecting to RTSP stream...
Connection established!

Enter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): DESCRIBE

Enter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): 
Received:
RTSP/1.0 200 OK
CSeq: 2
Date: Thu, Jan 01 1970 01:25:06 GMT
Content-Base: rtsp://192.168.201.1:7070/H264VideoSMS/
Content-Type: application/sdp
Content-Length: 484

v=0
o=- 3737324 1 IN IP4 192.168.201.1
s=Session streamed by "OnDemandRTSPServer"
i=H264VideoSMS
t=0 0
a=tool:LIVE555 Streaming Media v2015.07.23
a=type:broadcast
a=control:*
a=range:npt=0-
a=x-qt-text-nam:Session streamed by "OnDemandRTSPServer"
a=x-qt-text-inf:H264VideoSMS
m=video 0 RTP/AVP 96
c=IN IP4 0.0.0.0
b=AS:35000
a=rtpmap:96 H264/90000
a=fmtp:96 packetization-mode=1;profile-level-id=4D001F;sprop-parameter-sets=Z0
0AH+VAKALYgA==,aO4xEg==
a=control:track1

SETUP

Enter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): 
Received:
RTSP/1.0 200 OK
CSeq: 3
Date: Thu, Jan 01 1970 01:25:54 GMT
Transport: RTP/AVP;unicast;destination=192.168.201.21;source=192.168.201.1;cli
ent_port=8000-8001;server_port=6970-6971
Session: 51B6236A;timeout=65


PLAY

Enter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): 
Received:
RTSP/1.0 454 Session Not Found
CSeq: 4
Date: Thu, Jan 01 1970 01:26:04 GMT


Read error: read tcp 192.168.201.21:54189->192.168.201.1:7070: read: operation
 timed out
max@Mac go % 
```
Seems I initially had the stream URL incorrect, but after correcting it in the code, I managed to be able to `DESCRIBE` and `SETUP` the stream. Playing didn't seem to work, I got a `454 Session not found` I'm guessing I need to supply the sessionID along with the request. Let's see if the RFC says anything about that.

<img width="605" alt="image" src="https://github.com/user-attachments/assets/49f35bf8-9267-4019-bc00-13f4906ada60" />

Looks like I _should_ be sending the session, so let's adapt the code and grab any sessions that are sent:

```go
package main

import (
	"bufio"
	"fmt"
	"net"
	"os"
	"os/signal"
	"strings"
	"syscall"
)

var sessionID string

func main() {
	rtspAddr := "192.168.201.1:7070"
	rtspURL := "rtsp://192.168.201.1/H264VideoSMS"

	fmt.Println("Connecting to RTSP stream...")
	rtspStream, err := net.Dial("tcp", rtspAddr)
	if err != nil {
		panic(err)
	}
	defer rtspStream.Close()
	fmt.Println("Connection established!")

	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)

	commands := make(chan string)
	quit := make(chan struct{})

	// Goroutine: Handle SIGINT (Ctrl+C)
	go func() {
		sig := <-sigs
		fmt.Printf("\nReceived signal: %s\n", sig)
		close(quit)
		os.Exit(0)
	}()

	// Goroutine: Send commands to RTSP server
	go func() {
		for {
			select {
			case cmd := <-commands:
				var req string
				switch strings.ToUpper(cmd) {
				case "OPTIONS":
					req = fmt.Sprintf("OPTIONS %s RTSP/1.0\r\nCSeq: 1\r\n\r\n", rtspURL)
				case "DESCRIBE":
					req = fmt.Sprintf("DESCRIBE %s RTSP/1.0\r\nCSeq: 2\r\nAccept: application/sdp\r\n\r\n", rtspURL)
				case "SETUP":
					req = fmt.Sprintf("SETUP %s RTSP/1.0\r\nCSeq: 3\r\nTransport: RTP/AVP;unicast;client_port=8000-8001\r\n\r\n", rtspURL)
				case "PLAY":
					req = fmt.Sprintf("PLAY %s RTSP/1.0\r\nCSeq: 4\r\nSession: %s\r\n\r\n", rtspURL, sessionID)
				default:
					fmt.Println("Unknown command:", cmd)
					continue
				}
				_, err := rtspStream.Write([]byte(req))
				if err != nil {
					fmt.Println("Write error:", err)
					return
				}
			case <-quit:
				return
			}
		}
	}()

	// Goroutine: User input
	go func() {
		reader := bufio.NewReader(os.Stdin)
		for {
			fmt.Print("\nEnter RTSP command (OPTIONS, DESCRIBE, SETUP, PLAY): ")
			text, _ := reader.ReadString('\n')
			text = strings.TrimSpace(text)
			if text == "exit" || text == "quit" {
				close(quit)
				os.Exit(0)
			}
			commands <- text
		}
	}()

	// Main loop: Read from RTSP stream
	buf := make([]byte, 4096)
	for {
		select {
		case <-quit:
			fmt.Println("Exiting reader loop...")
			return
		default:
			n, err := rtspStream.Read(buf)
			if err != nil {
				fmt.Println("Read error:", err)
				return
			}
			if n > 0 {
				fmt.Printf("\nReceived:\n%s\n", buf[:n])
				if sessionID == "" {
					sessionID = getSessionFromResponse(string(buf))
				}
			}
		}
	}
}

func getSessionFromResponse(res string) string {

	if strings.Contains(res, "Session:") {
		lines := strings.Split(res, "\r\n")
		for _, line := range lines {

			if strings.HasPrefix(line, "Session:") {
				parts := strings.Split(line, ":")
				if len(parts) > 1 {
					sessionID = strings.TrimSpace(strings.Split(parts[1], ";")[0])
					fmt.Println("Session ID captured:", sessionID)
				}
			}
		}
	}
	return ""
}
```

And dang, battery for the drone ran out before I could test - looks like I'll pick this up tomorrow. At some point, I'll take a battery out of it's container, and hard wire a PSU in so it's better for developing (and maybe diasble the damn LEDs!). I have a spare drone with a damaged rotor motor, so I'll probably use that if I can find it (I moved countris and who knows where it is now!)

# [9/04/2025]

So I've managed to get a stream establied using my previous crappy code. It was nice to manually run command in a CLI type way, but I think now we need something a bit more sophisticated. I've started a "service object struct" like so:

```go
package RTSPClient

import (
	"bufio"
	"errors"
	"fmt"
	"log"
	"net"
	"os"
)

type RTSPClient struct {
	conn        net.Conn
	reader      *bufio.Reader
	addr        string
	url         string
	sessionID   string
	cSeq        int
	previousCmd string
	logger      *log.Logger
}

// NewRTSPClient generates a new client. `host` is the host address, IE
// 192.168.0.1, `port` is the port address, for example 7070, and path is the
// RTSP streaming URL, like H264VideoSMS
// TODO: This only work with ipv4 address, not ipv6
func (c *RTSPClient) NewRTSPClient(host string, port string, path string) (*RTSPClient, error) {
	urlAndPort := fmt.Sprintf("%s:%s", host, port)
	conn, err := net.Dial("tcp", urlAndPort)
	if err != nil {
		return nil, err
	}

	url := fmt.Sprintf("rtsp://%s/%s", host, path)

	return &RTSPClient{
		conn:        conn,
		addr:        urlAndPort,
		url:         url,
		cSeq:        1,
		previousCmd: "",
		logger:      log.New(os.Stdout, "[RTSP] ", log.LstdFlags),
	}, nil
}

// sendRtspCmd is used to send an RTSP command, for example, `OPTIONS` to an
// RTSP server.
func (c *RTSPClient) sendRtspCmd(cmd string) error {
	req := fmt.Sprintf("%s %s RTSP/1.0\r\nCSeq: %d\r\n\r\n", cmd, c.addr, c.cSeq)
	_, err := c.conn.Write([]byte(req))
	if err != nil {
		c.logger.Printf("error sending %s command: %s", cmd, err)
	}
	c.cSeq++
	c.previousCmd = cmd
	return nil
}

// Options sends the `OPTIONS` command
func (c *RTSPClient) Options() error {
	return c.sendRtspCmd("OPTIONS")
}

// DESCRIBE sends the `DESCRIBE` command
func (c *RTSPClient) DESCRIBE() error {
	return c.sendRtspCmd("DESCRIBE")
}

// SETUP sends the `SETUP` command
func (c *RTSPClient) SETUP() error {
	if c.previousCmd != "DESCRIBE" {
		c.logger.Printf("it is recomended to send the DESCRIBE command before SETUP")
	}
	return c.sendRtspCmd("DESCRIBE")
}

// PLAY sends the `PLAY` command
func (c *RTSPClient) PLAY() error {
	if c.sessionID == "" {
		return errors.New("no sessionID, issue command `SETUP` before `PLAY`")
	}
	return c.sendRtspCmd("PLAY")
}
```

 I haven't tested it yet, I'll probably do that tomorrow. But for now, it looks pretty good. 

# [20/04/2025]

A quick update, I've been slowly working on the RTSP video feed, and I've made some progress. I've got a seperate [repo](https://github.com/maxsimmonds1337/droneRtspClient] with all the code, but here's the client:

```go
package RTSPClient

import (
	"errors"
	"fmt"
	"io"
	"log"
	"net"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

type Info struct {
	Conn         net.Conn // holds the tcp connection
	Addr         string
	Url          string
	Timeout      time.Duration
	Session      string
	PreviousResp *RtspResponse
	CSeq         int
	PreviousCmd  string
	ffmpegCmd    *exec.Cmd
	ffmpegIn     io.WriteCloser
	Logger       *log.Logger
}

type RtspResponse struct {
	StatusLine string
	Headers    map[string]string
	Body       string // TODO: maybe have a dedicated struct for this - SdpResponse
}

// NewRTSPClient generates a new client. `host` is the host address, IE
// 192.168.0.1, `port` is the port address, for example 7070, and path is the
// RTSP streaming URL, like H264VideoSMS
// TODO: This only work with ipv4 address, not ipv6
func NewRTSPClient(host string, port string, path string, logger *log.Logger) (*Info, error) {
	urlAndPort := fmt.Sprintf("%s:%s", host, port)
	conn, err := net.Dial("tcp", urlAndPort)
	if err != nil {
		return nil, err
	}

	url := fmt.Sprintf("rtsp://%s:%s/%s", host, port, path)

	return &Info{
		Conn:         conn,
		Addr:         urlAndPort,
		Timeout:      0,
		Url:          url,
		CSeq:         1,
		PreviousCmd:  "",
		PreviousResp: &RtspResponse{},
		Logger:       logger,
	}, nil
}

// sendRtspCmd is used to send an RTSP command, for example, `OPTIONS` to an
// RTSP server.
func (c *Info) sendRtspCmd(cmd string, headers map[string]string) error {
	var sb strings.Builder

	//TODO: remove the hardcoded track, needs better unpacking SDP packet
	header := fmt.Sprintf("%s %s RTSP/1.0\r\nCSeq: %d\r\n", cmd, c.Url, c.CSeq)
	sb.Write([]byte(header))
	if c.Session != "" {
		sessionHeader := fmt.Sprintf("Session: %s\r\n", c.Session)
		sb.Write([]byte(sessionHeader))
	}

	for k, v := range headers {
		sb.Write([]byte(k + ": " + v + "\r\n"))
	}

	sb.Write([]byte("\r\n"))
	req := sb.String()

	c.Logger.Printf("Sending request:\r\n%s", req)
	// I suspect there's an issue with this because server time is wrong
	// and so this fails straight away
	// if c.Timeout != 0 {
	// 	c.Conn.SetDeadline(time.Now().Add(c.Timeout))
	// }
	_, err := c.Conn.Write([]byte(req))
	if err != nil {
		c.Logger.Printf("error sending %s command: %s", cmd, err)
	}
	c.CSeq++
	c.PreviousCmd = cmd
	return nil
}

// Options sends the `OPTIONS` command
func (c *Info) Options() (RtspResponse, error) {
	err := c.sendRtspCmd("OPTIONS", nil)
	if err != nil {
		return RtspResponse{}, err
	}
	return c.getResponse()
}

// Describe sends the `DESCRIBE` command
func (c *Info) Describe() (RtspResponse, error) {

	headers := map[string]string{
		"Accept": "application/sdp",
	}
	err := c.sendRtspCmd("DESCRIBE", headers)
	if err != nil {
		return RtspResponse{}, err
	}
	return c.getResponse()

}

// Setup sends the `SETUP` command and returns the session captured, if sent
func (c *Info) Setup() (RtspResponse, error) {
	if c.PreviousCmd != "DESCRIBE" {
		c.Logger.Printf("it is recomended to send the DESCRIBE command before SETUP")
	}
	headers := map[string]string{
		"User-Agent": "rtsp_test (LIVE555 Streaming Media v2015.09.24)",
		"Transport":  "RTP/AVP/TCP;unicast;interleaved=0-1",
	}
	//TODO: make this not hardcoded
	c.Url = c.Url + "/track1"
	err := c.sendRtspCmd("SETUP", headers)
	if err != nil {
		return RtspResponse{}, err
	}

	res, err := c.getResponse()
	if err != nil {
		return RtspResponse{}, err
	}

	c.Session = res.Headers["Session"]
	if c.Session == "" {
		return res, errors.New("no session returned from RTSP Stream")
	}

	if res.Headers["timeout"] != "" {
		timeout, err := strconv.Atoi(res.Headers["timeout"])
		if err != nil {
			c.Logger.Printf("failed to convert string to int: %s", err)
		}
		c.Timeout = time.Duration(timeout)
	}

	return res, nil
}

// Play sends the `PLAY` command
func (c *Info) Play() (RtspResponse, error) {
	if c.Session == "" {
		return RtspResponse{}, errors.New("no session, issue command `SETUP` before `PLAY`")
	}

	headers := map[string]string{
		"User-Agent": "rtsp_test (LIVE555 Streaming Media v2015.09.24)",
		"Range":      "npt=0.000-",
	}
	err := c.sendRtspCmd("PLAY", headers)
	if err != nil {
		return RtspResponse{}, err
	}
	return RtspResponse{}, nil //c.getResponse()
}

func (c *Info) getResponse() (RtspResponse, error) {
	res := make([]byte, 4096)
	n, err := c.Conn.Read(res)

	if err != nil {
		c.Logger.Printf("error reading response from RTSP")
		return RtspResponse{}, err
	}

	if n == 0 {
		c.Logger.Printf("no response from RTSP")
		return RtspResponse{}, nil
	}

	c.Logger.Printf("Response: \r\n %s \r\n", res)
	resp, err := parseStringRtspResponse(string(res))
	c.PreviousResp = &resp
	return resp, err
}

func parseStringRtspResponse(strResp string) (RtspResponse, error) {
	var responseStruct RtspResponse

	if strResp == "" {
		return RtspResponse{}, nil
	}

	sections := strings.Split(strResp, "\r\n\r\n")
	if len(sections) == 0 {
		return RtspResponse{}, nil
	}

	headers := sections[0]
	if len(sections) > 1 {
		body := sections[1]
		responseStruct.Body = body
	}

	headerMap := make(map[string]string)
	for header := range strings.SplitSeq(headers, "\r\n") {
		splitHeader := strings.SplitN(header, ":", 2)
		if len(splitHeader) < 2 {
			continue
		}
		//TODO: this whole thing could be done a lot better, anything after a ';' is a
		// param, so maybe we store these somehow better? also, if it sends more that 2 params
		// this will shit itself
		if splitHeader[0] == "Session" {
			splitSessionParams := strings.Split(splitHeader[1], ";")
			if len(splitSessionParams) == 2 {
				session := strings.TrimSpace(splitSessionParams[0])
				timeout := strings.TrimSpace(splitSessionParams[1])

				headerMap["Session"] = session
				headerMap["timeout"] = strings.Split(timeout, "=")[1]
			}

		} else {
			key := strings.TrimSpace(splitHeader[0])
			val := strings.TrimSpace(splitHeader[1])
			headerMap[key] = val
		}
	}

	responseStruct.Headers = headerMap
	return responseStruct, nil
}

func (c *Info) setupFFmpegPipe() error {
	// FFmpeg command to process the incoming RTP stream
	cmd := exec.Command("ffmpeg", "-f", "h264", "-i", "-", "-c:v", "copy", "-f", "mp4", "output.mp4")

	// Set up a pipe to feed RTP data into FFmpeg
	ffmpegIn, err := cmd.StdinPipe()
	if err != nil {
		return fmt.Errorf("failed to create FFmpeg pipe: %w", err)
	}

	// Start the FFmpeg process
	err = cmd.Start()
	if err != nil {
		return fmt.Errorf("failed to start FFmpeg: %w", err)
	}

	c.ffmpegCmd = cmd
	c.ffmpegIn = ffmpegIn

	return nil
}

func (c *Info) ReadRtpPacketAndStreamToFFmpeg() {
	// Open the FFmpeg pipe for the first time
	err := c.setupFFmpegPipe()
	if err != nil {
		log.Fatalf("Error setting up FFmpeg pipe: %s", err)
		return
	}
	defer c.ffmpegIn.Close()

	// Start reading RTP packets and piping them to FFmpeg
	for {
		// Buffer for the RTP packet
		buf := make([]byte, 4)
		_, err := io.ReadFull(c.Conn, buf)
		if err != nil {
			c.Logger.Printf("Error reading RTP packet header: %s", err)
			return
		}

		// If it's not an RTP packet, skip it and continue reading
		if buf[0] != '$' {
			c.Logger.Printf("Not an RTP packet")
			continue
		}

		// Channel and payload length
		channel := buf[1]
		length := int(buf[2])<<8 | int(buf[3])

		// Allocate buffer for payload data
		payload := make([]byte, length)
		_, err = io.ReadFull(c.Conn, payload)
		if err != nil {
			log.Fatalf("Read payload error: %v", err)
		}

		c.Logger.Printf("Received RTP packet on channel %d with length %d bytes", channel, length)

		// If it's RTP data (channel 0), pipe it to FFmpeg
		if channel == 0 {
			mediaPayload := payload[12:]
			c.handleRTPPayload(mediaPayload)
		}
	}
}

const startCode = "\x00\x00\x00\x01"

var currentFU []byte
var sps, pps []byte

func (c *Info) handleRTPPayload(payload []byte) {
	if len(payload) < 1 {
		return
	}

	nalType := payload[0] & 0x1F

	switch nalType {
	case 7: // SPS
		sps = append([]byte(startCode), payload...)
		c.saveNAL(sps)
	case 8: // PPS
		pps = append([]byte(startCode), payload...)
		c.saveNAL(pps)
	case 5: // IDR (keyframe)
		c.saveNAL([]byte(startCode)) // start code
		c.saveNAL(payload)           // payload
	case 1, 6: // Non-IDR slice or SEI
		c.saveNAL([]byte(startCode))
		c.saveNAL(payload)
	case 28: // FU-A
		if len(payload) < 2 {
			return
		}
		fuIndicator := payload[0]
		fuHeader := payload[1]
		start := (fuHeader & 0x80) != 0
		end := (fuHeader & 0x40) != 0
		reconstructedNALType := fuHeader & 0x1F
		nalHeader := (fuIndicator & 0xE0) | reconstructedNALType

		if start {
			currentFU = []byte{nalHeader}
			currentFU = append(currentFU, payload[2:]...)
		} else {
			currentFU = append(currentFU, payload[2:]...)
		}

		if end {
			c.saveNAL([]byte(startCode))
			c.saveNAL(currentFU)
			currentFU = nil
		}
	default:
		// Handle other types if you want, or just ignore
	}
}

func (c *Info) saveNAL(nal []byte) {

	// Write the RTP payload to FFmpeg's input pipe
	_, err := c.ffmpegIn.Write(nal)
	if err != nil {
		log.Printf("Error writing RTP data to FFmpeg: %s", err)
		return
	}
}

func (c *Info) Close() error {
	var err error

	if c.ffmpegIn != nil {
		c.Logger.Println("Closing ffmpeg input pipe...")
		_ = c.ffmpegIn.Close() // ignore error, not worth losing sleep
	}

	if c.ffmpegCmd != nil {
		c.Logger.Println("Waiting for ffmpeg to finish...")
		if waitErr := c.ffmpegCmd.Wait(); waitErr != nil {
			c.Logger.Printf("ffmpeg exited with error: %v", waitErr)
			err = waitErr // record error to return
		}
	}

	//TODO: wrap this
	err = c.Conn.Close()
	return err
}
```

The current issue I have is that the `output.mp4` can't be played, and for now I don't know why. It's most likely that I'm not parsing the RTP payload correctly. A friend of mine had a great idea, which is to generate some packets using gstreamer, and use those in some unit tests to see what's wrong. So, that's my plan now! 
