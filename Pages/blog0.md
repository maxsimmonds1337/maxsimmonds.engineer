# Blog 0 - Day 0

There are a number of things I could start looking at for this project, specifically, I could look more into the motor (I've already decided a [Phub 188A from peiscooter is the way](https://www.peipeiscooter.com/10inch-10-inch-10x6-00-5-5-wide-tyre-brushless-gearless-dc-wheel-hub-motor-balance-scooter-hub-motor-hally-motor-phub-188.html)). I could look at the frame, and start thinking more about the mechanical build, or I could look at the hardware or software. 

I'm currently waiting to order the motor, it's a pretty big investment for something that's not a requirment in my life right now. So that leaves only a few other options. Being an electronics engineer, I guess the first thing my mind goes to is the electronics, and hey, a little bit of dopeamine from getting some electronics working my keep me working on the SBS for many months to come!

## Electronics/Hardware

To my mind at the moment, there are several main subsystems for the hardware:

- BLDC hub motor
- 3 phase Inverter / ESC (electronic speed controller)
- IMU (intertial measurement unit)
- Feetpads (to determine when your feet are on the board, kinda like a [deadman switch](https://en.wikipedia.org/wiki/Dead_man%27s_switch) )
- Front and rear lights (these will be LEDs, the neopixel kind, 5050 LEDs that are singularly addressable)
- The microcontroller, though, really, this is going to be part of the ESC
- Batteries (almost certainly going to be 18650s)

And that's all I can think off. Each section above will have it's own pages/post (dependig on how I decide to go forward with documentation). I will start with the ESC, though. A fellow engineer has done so much of the hardwork here already, a guy called [Benjamin Vedder](http://vedder.se/2015/01/vesc-open-source-esc/) has made an open source ESC, which he's called VESC - for obvious reasons. While the schematics are freely available, the gerbers/layout is not. That suits me quite well (otherwise I would feel like I'm cheating, copying the main subsystem from someone else!). The code, though, most importantly is open source and freely available too. While I can (and have!) written code for STM32 uPs for ESCs (I made a 1000W BLDC ebike controller), I know that I will get bogged down on that - building a SBS from scratch is going to be a long project, anything to speed it up is welcomed. I can always go back and write my own code if needed, but I would rather give back to the community of the VESC, so I hope to make some merge requests for that.

### ESC 

The first thing I'm going to look at is the ESC. As mentioned, the schematics are available (in [KiCAD](https://www.kicad.org/)) from his other [site](https://vesc-project.com/node/311). It seems that he has two sites, and a github. The second site I linked has the schematics for the newer versions of the ESC. I will attempt to make the VESC 6 MK IV. There only seems to be a pdf of [schematics](https://vesc-project.com/sites/default/files/Benjamin%20Posts/VESC_6_mk5.pdf) available. That's not the end of the world, though, I will most likely make some small modifications to the design as I go, and layout of a PCB is pretty enjoyable anyway, and gives it a personal touch!

What I do need to check, though, is that the firmware is available for the VESC 6 MK IV, that would be a show stopper!

#### ESC Firmware

So, looks like all the firmware is [here](https://github.com/vedderb/bldc). The [README](https://github.com/vedderb/bldc/README.md) states that it should work for all board kinds, and to run 'make' to see. I haven't pulled the code (yet!) but I did dig through the MakeFile, which looks really interesting. There's some code that refers to a 'Big Hammer' to build for all boards:

``` make
	@echo "   [Big Hammer]"
	@echo "     all_fw               - Build firmware for all boards"
	@echo "     all_fw_package       - Packaage firmware for boards in package list"
```

There's also some code for getting a list of boards:

``` make
# Strip the paths down to just the names. Do this by first using `notdir` to remove the paths, then the prefix (hw_), then remove the suffix (.h). Finally, sort into lexical order.
ALL_BOARD_NAMES := $(sort $(subst .h,,$(subst hw_,,$(filter hw_%, $(notdir $(TARGET_PATHS))))))
```

Now that's one hell of a make command!
