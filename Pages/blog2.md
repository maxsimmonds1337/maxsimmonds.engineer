# Blog 2 - Starting the design!

I don't think I'm going to get much done today, but I told myself I will do atleast _something_ every day. So, now the KiCAD project is setup, I'll start looking at the hierarchical blocks, and get the system design sorted!

## Sub-systems

A list of functional blocks from the VESC 6 MK5 schematic:

- MCU
- CAN
- HES (hall Effect Sensors)
- nRF51822 bluetooth/wireless SoC
- SPI
- I2C
- Servo connection
- SWD connection
- RGB debug LEDs
- IMU / BMI160
- DRV8301 Three Phase Gate Driver with buck reg (with only two current shunt amps...?)
- Three phase bridge driver

Each of these will have it's own block; I'm a fan of hierarchial design, as the top level sheet acts similary to a system block diagram - which is great!

Tomorrow, I will start a review of the current design. There are some things I might add (like snubbers, or at least flyback diodes on the 3-phase bridge). I noticed that the current sense amps used on the phase outputs (while, it doesn't have any filtering, though, not sure it needs it!) have ADs patented design for removing PWM voltage swings, a real neat trick. I once tracked down the patent for that (or, at least, my best guess as it was odly named). They use a succession of chopper amps to acheive this. If I find it again, I'll put it up here. (Okay, litterally a one second google search for "chopper amp analog devices google patents pwm" and I found [it](https://patents.google.com/patent/US6734723B2/en)

It'll also be good to double check the FETs, to make sure they don't exhibit something called "parasitic turn on" which results in shoot-through.

So, there isn't really much to this thing! In fact, I did a design of a E-Bike BLDC driver before (with an STM also) which was very similar:

![image](https://user-images.githubusercontent.com/58208872/182718104-89cccf8a-4ed6-40da-bf18-64e536405794.png)

The main difference is that there was no need for an IMU, so I had a throttle input. I also had an LCD (which I wrote some pretty neat drivers for, I implimented the low level LCD drivers over I2C using an IO expander, so there was only two wires going from the main board, to the LCD board, which then had an I2C IO expander breaking out into the 7+ lines required for an LCD!)

I had some lessons learnt from that project, which I will write up here:

1) Something was causing the MCU to reset when the throttle position was low and I was going down hill (and hence, the motor became a generator). This means that, going down hill, I had to increase the throttle to maximum, which even that wasn't full proof, to stop the MCU crashing and requiring a reset.
2) I never used the SD card. I'm pretty sure that I can store some data into some non-volatile memory on the STM32. I had this card because I wanted to keep track of things like runtime/miles/currents/voltages etc. But I never got around to writing the FW. So, it would be interesting to see how VESC does this
3) Grounding! God, grounding. I went for a star configuration, power had it's own ground, as did digital, as did analogue. This I regret. While I don't _think_ it caused any issues (maybe that's the problem with point 1!), it made layout a huge pain in the ass. And, I think pointlessly so. They no longer recommend split planes, and some ADCs for example (ones with a digital interface) don't even have seperate ground pins anymore. And I'm talking about the 18bit ADCs, so if they don't care, why should I!
4) I had a lot of "diode ORs" because I wasn't sure what I could connect to where, for example, the 3v3 from the on board buck, and the 3v3 of the SWD programmer. I'll be paying close attention to what VESC did
5) Fail Fast! My first commit of the project was Oct 6 2020 and the last (or at least when I said I would send to JLC, was Jan 11 2021! That's 3 months just to get the schematic and layout done, let alone assembly (JLC didn't offer much in the way of assembly at that point), writing the code, testing, and assembling! In fact, I have a photo of the built bike on 25/09/2021! That's almost a year long project. Admitedly, I did start a consultancy around the same time, but still, if I want that subway,I need to be quicker!
6) Use dedicated current sence ICs, don't do it discretly. I was trying to have fun with analogue design, but it isn't worth it. Takes much longer, and the result will rarely be better than a monolithic IC.
7) Use pull up resistors for I2C. I was testing a new method (a current mirror) and while that worked, there's no real need for it.
8) Be careful with the filters on the HES. In fact, I even made an [issue](https://github.com/maxsimmonds1337/EBIKE/issues/12) for it. It resulted in not letting square pulses at higher motor speeds.
9) Finally, review my own schematic before fabrication. This is something I hope to be better at now, after spending a couple of years consulting, I got pretty good at spotting faults before fabrication, and checking schematics and layouts. I have a rudimentary checklist I use (and keep on [github](https://github.com/TheEngineeringOctopus/pcb-checklist). I'll make sure I do it before it goes out!
10) Finally finally, I'll order assembly. Yes it costs a bit extra, but damn is it easier. And if I ever sell any of these (I'll donate a certain % to the VESC community if I do!) then having a click to order process will be helpful.

Well, that's more than I thought I'd do today. Tomorrow I'll review the PCB, and start the hierarchical (or however the hell you spell that word!) blocks.
