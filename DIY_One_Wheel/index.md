# Self Balancing Unicycle - SBS V1.0

Welcome to my page on the SBS V1.0, more commonly known as the OneWheel!

I haven't given much thought in the way I should present/record my progress with this. Generally, I try to make a perfect framework for something, and religiously follow this best guess to it's own detriment, so I think this time I will do an ad-hoc, random succession of "blog posts" and see how that goes...


---

## [Blog Post 0 - Day 0](blog0.md)
Posted: 01/08/2022

---

## [Blog Post 1 - A free subway...](blog1.md)
Posted: 02/08/2022

---

## [Blog Post 2 - Starting the design!](blog2.md)
Posted: 03/08/2022

---

## [Blog Post 3 - VESC 6 MK IV Review](blog3.md)
Posted: 05/08/2022

---

## [Blog Post 4 - Schematic Capture!](blog4.md)
Posted: 17/01/2023

---

## [Blog Post 5 - (More) Schematic Capture!](blog5.md)
Posted: 23/02/2023

---

# [16/05/2025] 
## A New Way of Posting

So, it's been a while (almost 3 years, according to this !?) that I've posted. A lot has changed, I have a 2 year old girl, changed 2 (maybe 3?) jobs, even changed profession (from EE to SWE). I've been a SWE for a number of years now, and I've been missing the electronics side of things. Recently, I bought a mechanical calculator (from about 1950s, USSR) and I wanted to make it a clock (will be posting about that at some point). But, that's got me back into the swing of EE, and as summer draws closer, I really want that damn one wheel!

As I've been updating my [drone hacking](../Drone_Hacking/index.md) section, I found it a lot easier to post with one long page. And, tbg, it's going to be easier to read and see what's going on. It also means there's less overhead for me to actually update something (new file each time, updated _manually_ the table of contents above, etc). So screw it, let's just do this.

## Where the hell is the project at?

Well, not much different from [blog post 5](blog4.md). But I've picked the schematics back up again. Currently, I'm on a bus (for 2.5 hours!) across Estonia to go to a business hackathon. I've been working on a business idea I'd like to launch, and this seems like a pretty good place to try, so there's that.

But, this gives me a lot of time to sort a few things out, like updating my blog lol. Anyway, I was working on my drone hacking previously, and then things have all gotten out of hand and I'm working on several (this, mechanical calc clock build, 3d printer build, and that buisness idea) all at once. I probably need a bit more focus but hey ho. 

So, in terms of what's currently captured in a schematic:

- BLE / WiFi module, actually this looks obsolete now, so will have to redo this
- Wheel rotation circuit
- MCU
- BLDC 3 phase driver
- USB conn
- CAN

And so what we have left to do:

- The bridge (6 FETs and current sense)
- IMU

And that's it, so actually, not a lot! I'll need to go through the whole BOM and see if there's any issues (like the EOL BLE module) and maybe some hard to source components. When I started this project, it was during the huge issues with part shortages, I'm hoping things have calmed down now.

