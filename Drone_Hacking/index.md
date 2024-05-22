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

