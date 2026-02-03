# LED Streaming Display - Rocket Countdown
---

## 02/02/26

### Requirements

Okay, so, as I said. I want to have a scrolling LED, wall mounted display that
can show:

- Temperature
- Time 
- Date 
- Latest Rocket Launch
- Other stuff

Basically, anything that I want to put on it. It'll be Wi-Fi enabled (either by
ESP32, or RPI or something, not yet decided. If I can get away with the low pin
count of the ESP, then that makes the most sense).

In terms of loose requirements, in no particular order:

1. Should be made as cheaply as possible. That means using whatever I have to
   hand, and buying very little extra
2. I want quite a few modules. About 10-15. So buying the standard 8x8
   modules, and the MAX7219 (almost 20€ or so each!)
3. 1xn is required. 2xn might be possible, but maybe left for the future.
4. Single colour LEDs, (RED). Future project could utilise RGB, and/or single
   wire protocol, addressable.
5. USB powered
6. Easily readable from a few meters. That means large modules, and enough of
   them to make readability better.
7. Be able to make some noise. I think a simple buzzer would suffice initially,
   maybe there's scope for a speaker, but to have an alarm or stopwatch, I want
   it to make some noise.r a speaker, but to have an alarm or stop watch
function then I want it to make some noise.
8. Easily be able to update the display, so needs some sort of UI. I want to be
   able to do this from my phone and or laptop.

The main parts of the design will be:

1. Plastic enclosure module
    1.1 Will be 3D printed. Designed in either Onshape or Freecad (preferably
the former if my free period is still available)
2. Electronics
    2.1 Some type of power supply - could be directly from USB, I don't
anticipate the current to be too high, I'll be driving one column at a time
(will need to check if I can keep the refresh rate >50Hz with a 15 module long
display while keeping the brightness reasonable).
    2.2 Controller - so this will be something like ESP32, or RPI (something
with Wi-Fi)
    2.3 Driver - now this is were the project gets interesting. A simple
solution is to buy 15 MAX7219's, that's like $$ 15 x 20 = £300 $$ !!! And that's
before we add the rest of the stuff in. Likely I will be charliplexing this,
rather than simple x/y multiplexing. That'll save me some pins, at the expense
of software complexity (but hey, bits are free!). I'm thinking of something like
shift registers, maybe some IO expanders, I'm not sure yet. But this will be the
problem we need to solve first, and it'll drive the constraints.
3. UI - this will be pretty simple, so doesn't warrant much here.


That's all for now, tomorrow we'll tackle the multiplexing issue!

![image](./images/max7219_x_y.png)






