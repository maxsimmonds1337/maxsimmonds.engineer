# Blog 5 - (More) Schematic Capture!

So, I guess in my previous blog, I lied. I said "over the next few days I'd hope to be done". Well, it's been more than a month and I only did some more of the schematic capture today. But, I guess, it's better than nothing! There's a couple of reasons, firstly, I started a new job so most of my free time has been coding (mostly C, going through the CS50x course, and most recently, GO). Secondly, I've been unwilling to make new posts, as I'm writing some code that auto generates my blog posts. Currently, I have to manually add a blog entry (both in the index, and make the actual post). This is a bit annoying, and I wanted to not do it again until I had written that blog gen code, but that's take me a while too (because of the other things I'm doing!).

So, I put aside my perfectionism and have copied and pasted to make my blog entry!

Any way, I made a small amount of progress, so thought I'd capture that here.

# Progress

Actually, checking back on the last [blog 4](blog4.md) I've made a fair bit of progress, more than I thought! Most of the front page peripherals are done, things like connectors (USB, headers, etc), the "roll to start" circuit is captured, and so is the bluetooth module. I've also done the MCU, and most of the BLDC driver (in fact, if I have any time before I decide to sleep tonight, I might even finish that). 

## Front Page

<img width="1294" alt="image" src="https://user-images.githubusercontent.com/58208872/221044797-f9f1d70b-c8ab-4d9e-aa8e-6fdb5a56a506.png">

Here's the front page! Obviously not finished. The BLDC driver needs it's sheet entries pulled in, and there's a few missing components (a few status LEDs, the 6 axis IMU, and that's about it!). So not long now.

## MCU

<img width="1230" alt="image" src="https://user-images.githubusercontent.com/58208872/221044863-d3224cfa-8ae3-4371-91e5-17b4cb621d53.png">

This is done! When I give the schematic the once over, it might change slightly, but this is it pretty much done. I remember a post earlier (maybe I'll link it in one day!) where I was trying to determine which MCU was used. Well, using my neat trick below (check out the old BOM section) I found it in the BOM. I very much doubt they changed the MCU in revisions, too much OSS (open source software) lost. It's the STM32F405RGT6 (I was right!).

## BLDC Driver

<img width="1249" alt="image" src="https://user-images.githubusercontent.com/58208872/221044979-d9f7e326-0de5-484d-b76c-1f104bee1626.png">

There's a little left to do here, the supply sense circuit, which is a simple N channel MOSFET that's enabled when the 5V buck is on (or, atleast, above the gate threshold of the FET), the voltage (I think they're bridge voltage, but I can't remember!) filter circuit with analogue switch (to add or remove filtering), and an LDO. Though, I recall thinking to myself that I didn't need this, so I'll check my notes from the first few blogs to see. 

## The Olb BOM

One of the tricks I found to help speed up the schematic capture was to look at the old version of the VESC (V4) and check out its [BOM](./BLDC4.12_BOM.csv). I've done this for some of the components, like the MCU, and a few specfic diodes (like the one used in the buck) where the actual part is important, and I'm too lazy to do the calcs for them...
