# Inductive Charger from Scratch
---

I have a project, actually, [a business](https://ncode.london/) that needs
custom wireless charging and wireless comms. I thought I would document that
process here - one, so that I can remember where I left off, and two, it might
be interesting.

## 26/02/26
Project started today!

I needed to make an Amazon order today, so I wanted to add some stuff instead of
ordering a small basket. I remembered I would need an inductive charging
solution, so I started thinking, what would I need?

## Requirements

The project has some interesting requirements:

1. Must wirelessly charge a device that's shaped as a ball
2. Must be able to sustain the operating power of the ball device (a few watts,
   probably).
3. Must be able to also charge during operation - let's say, 10W target power on
   the receiver side
4. The ball must be removable from the device
5. We must be able to transmit, either higher level, or lower level, motor
   commands to the base
6. The motor commands shall be:
     - LEFT_100MS
     - RIGHT_100MS
     - DOWN_100MS
     - UP_100MS
7. The ball must be magnetically attached to the base, with sufficient force to
   not be removed during operation at extreme (180 deg) angles.


So, with that, I thought: "Okay, I can't use a traditional flat coil". The
reason being that my ball in spherical. If I want a decently sized coil (the
radius is proportional to the distance at which the transmitter and receiver can
be apart, roughly, the distance at which the inductive coupling can transmit
power with reasonable efficiency is $$\frac{1}{2} \cdot d mm$$ where $$d$$ is the
diameter of the coil). The math on that is pretty interesting, but I don't have my
apple pen to draw out diagrams nicely, when I do get that back, I will update
this. But, essentially, at distances of one $$r$$ then the maximum possible
power transfer is a measly 12.5%.

That means, I need to keep the distance that separates the two coils as small as
possible. BUT, the other issue, is that the inductance of the coil (more
inductance means greater power transmission) 
