# Blog 3 - VESC 6 MK IV Review

Okay so it's been a busy couply of days (my consultancy has just changed from being a sole trader, to a limitied company, which is exciting, but requires me to open new bank accounts, redo all my consultacy agreements with customers, etc, so a lot of work!) but I have been able to do a first review of the schematic for the VESC 6 MK 5, and it's pretty cool...

# Schematic Review

## Page 1
![image](https://user-images.githubusercontent.com/58208872/183266527-f7274d4c-d317-4844-bf3f-5d96175ed2c8.jpeg)

Okay, so, page 1! There's a lot going on here. The most interesting circuit is in the upper left hand side. This seems to generate an analogue voltage, proportional to the motor drive signal. Where have D8 which rectifies the signal coming from SH_A, which is the source of the high side FET in the 3 phase bridge specifically, phase A. This is the output of phase A. Ordinarily, this is a square wave with varying duty cycle - the duty cycle of course varies sinusodally. 

## Modelling the Peak Detector

I'd like to model the above circuit to see if my predictions are true (essentially, a peak detector circuit to give some indication that the motor is moving and it's speed). I'm on a linux machine at the moment, and usually I use LTspice for my modelling (unsupported on linux). I tried QUCS but the learning curve is more than what I want just to test a hypothesis, so I'm using [Circuit JS](https://www.falstad.com/circuit/circuitjs.html) and awesome javascript based simulator, that has a lot of functionality.

## The Math

I would like this to be fairly representable of the real motor, and so I need an estimated frequency, or angular veloity = of the sine wave I'll be using to drive this thing. the math to get this is pretty simple, and I'll write it here as I will no doubt need it again in the future.

According to the pmanufacturer of my wheel](https://www.peipeiscooter.com/10inch-10-inch-10x6-00-5-5-wide-tyre-brushless-gearless-dc-wheel-hub-motor-balance-scooter-hub-motor-hally-motor-phub-188.html) (I still haven't bought it yet, but, I will) the tyre diameter is approximatly 254mm, or 0.254m.

And knowing that (according to a [youtube video](https://www.youtube.com/watch?v=BV0Z4yyjE4Y&t=119s) I watched recently, 10MPH isn't a bad idea of a top speed of a DIY onewheel. Essentially, we want the number of revolutions per second the wheel is going through, since this is directly proportional to the drive frequency. We're all familiur with the equation speed = distance/time, well, that's true in angular quantities too.

$$v$$ is 10MPH, or $$\approx 4.5m/s$$. We now need to convert distance into number of rotations. For example, with a wheel 1 meter in circumference, to reach a speed of 1 meter per second, the wheel would be rotating once per second. If the wheel was only 0.5m in circumference, then it would need to rotate twice as fast to cover 1m in the same time. Hence:

$$ revolutions per second = \frac{velocity}{circumference}

Doing some dimentional analysis shows that this equation is plausible, $$[m \cdot s^-1 ] [m^-1] = [s^-1]$$. Revolutions is a dimentionless quantitiy, and of course, per second is 1/s, so this makes sense. 

$$circumference = \pi \cdot D$$ where $$D$$ is the diameter will tell us 

## Page 2

![image](https://user-images.githubusercontent.com/58208872/183266556-f8792c25-be07-48cd-a8ca-73fb76ba5bba.jpeg)

## Page 3

![image](https://user-images.githubusercontent.com/58208872/183266562-0b57c61a-22bd-4749-812b-d9d241a115da.jpeg)

## Page 4

![image](https://user-images.githubusercontent.com/58208872/183266569-eda4e352-df57-4277-ae18-6fb627f7c2f4.jpeg)

## Page 5

![image](https://user-images.githubusercontent.com/58208872/183266574-983707d4-68b3-41c2-a8c5-e91384d477e6.jpeg)

## Page 6

![image](https://user-images.githubusercontent.com/58208872/183266581-b411b38c-3577-4984-babe-ac1a7e2e92fc.jpeg)
