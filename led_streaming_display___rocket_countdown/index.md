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


That's all for now, tomorrow we'll tackle the multipl>exing issue!

![image](./images/max7219_x_y.png)


## 07/02/26

Okay, so it's been a little longer than "the next day". I should have known.
I've been busy on a few projects in parallel (I have a startup utilising edge
AI, an enclosure for my [3D
printer](../making_an_enclosure_for_3d_printer/index.md), and a few others in
the works). 

Anyway, I've been googling and thinking about
[multiplexing](https://en.wikipedia.org/wiki/multiplexing) vs
[charlieplexing](https://en.wikipedia.org/wiki/charlieplexing). I read some
interesting pros and cons. Originally, I wanted to go with the former, as I was
thinking __"damn if I want 15 or so modules, with 64 LEDS each, that's almost
1000 LEDs. Each requiring a driving pin. No microcontroller has that many pins.

I was thinking of solutions with charlieplexing, shift registers, I2C IO
expanders, and then I realised, there's no point charlieplexing (which has
downsides in refresh rates and brightness, plus 'ghosting' issues between
switching), I was going to have to use shift registers in any case, so IO
expanders were not really needed (can daisy chain the shift registers). The
added complexity of charliplexing (which needs tristate shift registers) was
just not needed.

With 3 pins:

- Data
- Strobe
- Clock

I can drive any number of LEDs with just these three DIO pins - I can add more
whenever I want (just software update) and I can still scroll either vertically
or horizontally. So this really seems like the best of all worlds.

Each shift register output needs to be able to drive the LED and sink current
from it. Typically, this is about 25mA for full brightness. We can PWM LEDs on a
"per module" basis using the output enable (OE) pin on the shift register
(obviously, we'll need to choose one that has this feature, I have 3 in mind,
which I'll show a pro/con for each, but likely we will settle for the simple
74HC595).

This means we can easily use the ESP32, and run as many 8x8 modules that we
need.

### The Shift Register

A lot of this project is defined by the shift register choice. I've been looking
around, asking Gemini, etc., and I think I've come to a decision. The 4 I
thought about were:

- CD4014
- 74HC595
- TPIC6B595
- MAX7219

The winner, based on price and a few other things, was the **74HC959**. Let's
summarise them below:


| IC | Pros | Cons | Price |
| :--- | :--- | :--- | :--- |
| **CD4014** | • Cost is essentially €0 (I have 4) <br> • Good for learning | • PISO (Parallel-In, Serial-Out) is the opposite of what we want <br> • No output latch (flicker) | ~€1-2 |
| **74HC595** | • OE pin allows for PWM <br> • Extremely cheap | • **6mA limit!** Needs a Darlington array (ULN2803) or external transistors to handle the current | ~€0.20 |
| **TPIC6B595** | • **150mA** per output (massive) <br> • Power shift register | • More expensive <br> • Harder to source on LCSC | ~€1.00 |
| **MAX7219** | • Purpose-built display driver <br> • Built-in multiplexing <br> • [LCSC Chinese clones](https://www.lcsc.com/product-detail/C6705351.html) make it affordable | • Genuine Maxim versions are crazy expensive (€15+) <br> • Requires 10µF/0.1µF caps to stay stable | ~€1.00 |

So, let's think, maybe we should go with the MAX7219? Let's think more about
this tomorrow.

## 10/02/26

Okay, a few days late but hey, we're back. Let's pick up where we last were, I
think the MAX7219 is the choice. Specifically, the MAX7219M/TR. For each module
(64 LEDs), I would need only 1 for each 8x8 module. That's pretty good. Also,
it's possible to control the brightness digitally too. Finally, they can be
cascaded - so that works well for this scrolling text.

### The LEDs

So, next step is to take a look at some LEDs. We're going to need a lot, so I
want some cheap ones. I'm not too sure on size yet, either. I'm not sure if I
need SMD or THT - I'm inclinded to thing that THT would be more the look I'm
going for. From NASAs mission control center:

![image](./images/nasa_led.png)

Looking on LCSC [this LED](https://www.lcsc.com/product-detail/C7470870.html) looks to be a good fit. In 1000 quantities, it's about $27.7. That's not too bad, so probably will get these. They're clear (which probably looks better when LEDs are off) and then it's green when it's on.



## 21/02/26

Well it's been a little while, but I have been working (I promise). I've been
getting the base schematic done, I won't share it just yet, I'll wait till it's
done. But here's a few insights I've gotten so far:

1. The wifi link (ESP32) isn't actually an ESP32. I had a look at what I
   actually had and it was a [D1 mini](https://uc2cb756136852eb70d6a7c764aa.dl.dropboxusercontent.com/cd/0/inline2/C7QL3nZnDZNxBcOEiZFGtSBBPEXyqxlR70cme3Fjo7H9jrEw_xGuSXMaOJtRmAoR6fdZL-cHu3gwxdcLE-HGDzPPFSICcu0sYBHyFn336KLB1hG2uhc8YTWx-qEFsVPoqfg6mMdH2nVsf2TnSIG2nWmSDx8tQCkoSmlyi7TgZRf-PpEkmsVTbjltrazOGphf6ygioTYiFPVe0IXAqk2seujc00Cx0sLtUAbXD8ANNNat6iL5Ageq9DuPzW6o4bfN6vgUsyVKne-owqdk4Xzs4bK5gjADMG8lYQfAgtfLK0J_GQORKCzArELZezyPqrbCiisjJ2j57So1muzeelSbOYpinutrX58YMX7_YBIRq68zbw/file), which actually has an ESP82266MOD with 4MB
   of flash (over the SPI pins of the dev board, so those are actually out of
action). Now, these are pretty cheap on LCSC, about $2.5 or so. The "dev board"
is an ESP12F - really low GPIO count, and not many bells and whistles. It needs
a USB 2 UART, a few pullups/downs, and a 3v3 LDO.

2. I realised that, to keep costs down, I should make a PCB with all components
   on every module (IE, wifi, LEDs, USB connectors, etc.) Obviously only one
board (let's call it, the master board) needs a wifi module/USB, etc., but I can
reuse the same PCB board for each. That way, I can get 20 ish made at JLCPCB,
probably 100x100mm, for like $20.

## 23/02/2026

So I want to think about the current requirements of the LED supply.

Since it's rastered (that is, column driven) I think the worst case current,
assuming full brightness, would be $$8 \cdot 20mA = 160mA$$. That's pretty much
nothing!
