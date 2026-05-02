# Robot Dog Butler
---

## 28/02/26
Project started today!



## 05/05/26
Today's the day I actually start this! It's been 3 months since I promised my
daughter we would make a robot dog. There's been a few things that have stopped
me:

1. They're expensive
2. They take a lot of time commitment 
3. I don't have a good solution for the BLDC driver, which ties into point 1.

But, last night, I was using Claude to review a previous [BLDC motor design of
mine](https://github.com/maxsimmonds1337/EBIKE/blob/main/KiCAD_Ebike_Controller/Ebike_Controller.pdf) and I realised how awesome (although, I already knew, just didn't think about it for this implementation) it is for asking questions like "how do I size the DC link capacitors" and "why did this latch up my MCU when going down hill and regenerating".

It did a really good job explaining the physics, which was the intuition I was
missing. How much energy a hill is generating:

$$ E = P \cdot t = \tau \cdot \omega \cdot t $$

This was close to 500w of mechanical power into the system, and that has to go
somewhere. Anyway, I digress. The point is, we started talking about FOC (Field
Oriented Control) which is a requirement for the BLDC driver in this project. I
was initially worried about this, but, as Claude showed me, I know most of the
math already: Clarke Transform, P/Q transform, then two controllers (PI). It's
been a few years since I've done those, but It'll be fine.


![images](./images/motors.png)

Anyway, to that end, I thought a cool way to start would be:

1. Look through my collection (see above) of motors, find the highest torque one
2. Find a design of a leg online -> 3D print to match my chosen motor
3. Either buy an odrive or Chinese replica, and see if I can get this leg to
   jump. Will be used initially for a torque test/firmware control

![images](./images/torqueTest.png)

This is the setup used by [Aaed
Musa](https://www.youtube.com/watch?v=GFLa1b1juUo) who's built a couple of dog
bots now, I believe [James Bruton](https://www.youtube.com/@jamesbruton) does
something similar, too.

![images](./images/testJig.png)

The test jig I envision to look like the above. I don't currently have any Al
extrusion, but if I get that far, I'll buy some.


### What I Want To Get From This Project

Before I get too into the weeds on this, I thought it would be a good idea to
quantify what I would like to learn from this project. That way, when it's done,
I can look back and see how far I've come.

- FOC - field orientated control
- More about robots, I see my career and engineering moving towards physical AI,
  having a good foundation on modern robots will help
- Quasi direct drive actuators
- A more intuitive understanding of electric motors
- Control loops for "springy" legs
- Fast prototyping with 3D printing (I have a good background in 3D printing,
  but not so much with fast iterative designs)


There's probably a bunch more, but those are the ones I can think of right now.
Time to find a leg to print!

