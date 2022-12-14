# Blog 3 - VESC 6 MK IV Review

Okay so it's been a busy couply of days (my consultancy has just changed from being a sole trader, to a limitied company, which is exciting, but requires me to open new bank accounts, redo all my consultacy agreements with customers, etc, so a lot of work!) but I have been able to do a first review of the schematic for the VESC 6 MK 5, and it's pretty cool...

# Schematic Review

## Page 1
![image](https://user-images.githubusercontent.com/58208872/183266527-f7274d4c-d317-4844-bf3f-5d96175ed2c8.jpeg)

Okay, so, page 1! There's a lot going on here. The most interesting circuit is in the upper left hand side. This seems to generate an analogue voltage, proportional to the motor drive signal. Where have D8 which rectifies the signal coming from SH_A, which is the source of the high side FET in the 3 phase bridge specifically, phase A. This is the output of phase A. Ordinarily, this is a square wave with varying duty cycle - the duty cycle of course varies sinusodally. 

## Modelling the Peak Detector

I'd like to model the above circuit to see if my predictions are true (essentially, a peak detector circuit to give some indication that the motor is moving and it's speed). I'm on a linux machine at the moment, and usually I use LTspice for my modelling (unsupported on linux). I tried QUCS but the learning curve is more than what I want just to test a hypothesis, so ~~I'm using [Circuit JS](https://www.falstad.com/circuit/circuitjs.html) and awesome javascript based simulator, that has a lot of functionality.~~ I remoted into my Windows PC to use LTSpice.

## The Math

I would like this to be fairly representable of the real motor, and so I need an estimated frequency of the sine wave I'll be using to drive this thing. The math to get this is pretty simple, and I'll write it here as I will, no doubt, need it again in the future.

According to the [manufacturer of my wheel](https://www.peipeiscooter.com/10inch-10-inch-10x6-00-5-5-wide-tyre-brushless-gearless-dc-wheel-hub-motor-balance-scooter-hub-motor-hally-motor-phub-188.html) (I still haven't bought it yet, but, I will) the tyre diameter is approximatly 254mm, or 0.254m.

And knowing that (according to a [youtube video](https://www.youtube.com/watch?v=BV0Z4yyjE4Y&t=119s) I watched recently, 10MPH isn't a bad idea of a top speed of a DIY onewheel. Essentially, we want the number of revolutions per second the wheel is going through, since this is directly proportional to the drive frequency. We're all familiur with the equation speed = distance/time, well, that's true in angular quantities too.

$v$ is 10MPH, or $\approx 4.5 m/s$. We now need to convert distance into number of rotations. For example, with a wheel 1 meter in circumference, to reach a speed of 1 meter per second, the wheel would be rotating once per second. If the wheel was only 0.5m in circumference, then it would need to rotate twice as fast to cover 1m in the same time. Hence:

$$ revolutions per second = \frac{velocity}{circumference} $$

Doing some dimentional analysis shows that this equation is plausible, $[m \cdot s^-1 ] [m^-1] = [s^-1]$. Revolutions is a dimentionless quantitiy, and of course, per second is 1/s, so this makes sense. Plugging in our number of a wheel 0.5m in diameter at a speed of 1m/s, gives 2 revs per second; a good sanity check. 

So, we need the circumference, which, from school we remember is:

$$circumference = \pi \cdot D$$

where $D$ is the diameter/. This then gives us a diameter of $0.254*\pi = \frac{\pi}{4} \approx 0.79 m$. At a speed of 10MPH or 4.5m/s, we get an RPM of $\frac{4.5}{0.79} = 5.7/s$. That's about 350rpm, which is not a bad speed!

To correctly represent this in the electrical model, we need a voltage source that has a frequency of 6hz. The generated voltage would depend on the motor constant, I have the following from the manufacturer:

![image](https://user-images.githubusercontent.com/58208872/184012881-c1455874-284c-4814-87e5-8c90e8d95380.png)

I took two points from the graph, specifically, the voltage at the top given RPM (700RPM) and the voltage at the lowest given RPM (441RPM). The motor constant in particular I am interested in (there's [more that one](https://www.precisionmicrodrives.com/reading-the-motor-constants-from-typical-performance-characteristics) is the electrical motor constant. This tells you how much voltage a motor will produce when acting as a generator, or, as back EMF. I'm not quite sure how, under normal driving conditions, the phase outputs will be in terms of voltage, but this is my best guess for now.

$$ K_{e1} = \frac{70}{700} = 0.1$$

$$ K_{e2} = \frac{60.32}{441} = 0.14$$

Taking an average, I get 0.17.

Usually, $K_e$ is given in radians per second, but since I already have most things in RPM, I'll keep it like this for now. That means that, at ~350 RPM, the voltage would be $350 \cdot 0.17 = 59.5V$.

## The Simulation

![image](https://user-images.githubusercontent.com/58208872/184019356-7a9c22bf-fdff-463a-9d0f-e3a802587504.png)

Apologies for the poor screenshot, that's the best I can do whilst remote desktopping! But, as we predicted, it's just a peak detector, the zener kicks in and clamps, the 39k is there to limit zener current, and I suppose acts as a low pass filter with the 100n, with a corner frequency of 40Hz. That's an order of magnitude above the drive frequency, but at least 2 orders of magnitude below the PWM switching frequency (somewhere I expect to be around 20Khz, though I haven't checked the code)

### Motor Simulation

Okay, it's been waaaay too long since I posted here. I got a little carried away with the motor simulation, I wanted to get a more representative voltage for the "SH_A" input, and it evolved too:

![image](https://user-images.githubusercontent.com/58208872/184970418-3f4ba319-a76f-4afe-a242-40c18afa2d9a.png)

And it's half working, half not. I copied it from [stackExchange](https://electronics.stackexchange.com/questions/391240/3-phase-inverter-simulation). Anyway, it's taken up too much time and makes me not want to continue! So, I'm drawing a line under this, and will pick it up if/when I have time. Now, back to the MK IV!

I'm still unsure what's going on with that circuit on the front page, I'll check the code to see if that helps, and may post on the forum failing that. Anyway, for now, I'll keep it in my design and move on!

## Page 2

![image](https://user-images.githubusercontent.com/58208872/183266556-f8792c25-be07-48cd-a8ca-73fb76ba5bba.jpeg)

Not much going on here! Just a CAN phy which Mouser has good stock of. Moving on!

## Page 3

![image](https://user-images.githubusercontent.com/58208872/183266562-0b57c61a-22bd-4749-812b-d9d241a115da.jpeg)

This is just the MCU, when I do the schematic I'll check to see if we need buffers on the ADC inputs, and whether we want/need any filtering. There may be filtering elsewhere in the schematic. The schematic doesn't actually give the full part number for the STM, so I'll see if I can check the cod and see if a compiler flag gives any hints.

## Page 4

![image](https://user-images.githubusercontent.com/58208872/183266569-eda4e352-df57-4277-ae18-6fb627f7c2f4.jpeg)

Now this has a little more happening. There seems to be a filter that you can switch in a capacitor to ground, to add a high pass filter to the current measurements on the 3 phase BLDC output. There's a potential divider with gain:

$$ Gain = \frac{R_1}{R_1 + R_2} = \frac{2.2k}{2.2k+39k} = 0.053 $$

Therefore, with a battery input of 60V (which I believe this is rated for, though I have some concerns that I will raise later!), that gives a voltage at "sens_x" of 3.2V. This then goes into the ADC of the MCU. This could be used for sensorless operation, but the code will enlighten me on that. The analogue switch introduces a 100nF capacitor, yeilding a cutoff frequency of:

%% f_c = \frac{1}{2 \cdot \pi R \cdot C} = \frac{1}{2 \cdot \pi 2.2k \cdot 100n} = 723 Hz. That's an order of magnitude below what I would expect the switching frequency to be (about 20k).

There's another circuit on here that tells the MCU when the battery is present. That's Q7 and the two resistors. Again, it's the same gain as before, it's the same resistors, but the MOSFET is there to only be switched on (and therefore connect the two resistors as a potential divider) when the buck converter is online. This buck converter only comes online when the battery is connected. The output of this potential divider goes to the MCU, for reading the battery voltage.

When EN_GATE is low, the driver IC is in low power (20uA). There's a pull down on this page, but isn't required, since the IC has it's own internal 100k pull down. I believe the sequence of turn on is like follows:

1) External switch connects battery power to the DRV8301 IC
2) EN_GATE is low, since the MCU isn't yet on. Therefore, no switching occurs, and the motor can't move. Current consumption of the IC is low.
3) The EN_BUCK line is floating (there's no pull down) which means as soon as supply power is available, the buck comes online.
4) The 5V buck goes into a 3v3 LDO, which powers the MCU. At the same time (and therefore possibly overloading the MCU inputs) the battery sense voltage we discussed previously, is connected to the MCU ADC pin
5) Finally, I presumme the MCU pulls the EN_GATE pin high, to allow for switching - perhaps when footpads are depressed, or something

I might add a diode in reverse across the LDO for protection, LDO's can die when the output voltage is higher then their inputs. This generally occurs during power down, with large bulk capactitors on the output. Diodes can be reversed biased usually, and then forward biase in the above condition, saving the LDO.

## Page 5

![image](https://user-images.githubusercontent.com/58208872/183266574-983707d4-68b3-41c2-a8c5-e91384d477e6.jpeg)

This has just the IMU on it, nothing fancy here. Comms is over I2C.

## Page 6

![image](https://user-images.githubusercontent.com/58208872/183266581-b411b38c-3577-4984-babe-ac1a7e2e92fc.jpeg)

Finally we get to the power stuff! Here's the 3 phase BLDC driver, or inverter, circuit. This page also has the current shunts on there. The current shunts are 0.5mOhms, so pretty small! This is good for reducing heat loss (P = I^2R, if R is small then so too is the power loss) but can be bad for noise. There's a filter on the current measurments, with a cut off of 159k (with the analogue switch off) or 9950hz with the switch on.

It looks like the maximum current this circuit can safely measure (without damage to the ADCs) is 330A. The AD8418 current sense ICs have an internal gain of 20V/V, and the resistor gives a gain of 0.0005 V/A. So:

$$ \frac{3.3}{20} = 0.165V $$

$$ V = I \cdot R = \frac{0.165}{0.0005} = 330A $$

I have no idea if that's good or bad, but seems like nothing bad happened with their design so I will assume that's got some good margin on it!

Lastly, I might add some snubbers to the FETs to help with driving the inductive load.

That's all for now, tomorrow I can finally start capturing this schematic as is, with a couple of mods, and move to layout!
