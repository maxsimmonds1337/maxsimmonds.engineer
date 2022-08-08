# Blog 3 - VESC 6 MK IV Review

Okay so it's been a busy couply of days (my consultancy has just changed from being a sole trader, to a limitied company, which is exciting, but requires me to open new bank accounts, redo all my consultacy agreements with customers, etc, so a lot of work!) but I have been able to do a first review of the schematic for the VESC 6 MK 5, and it's pretty cool...

# Schematic Review

## Page 1
![image](https://user-images.githubusercontent.com/58208872/183266527-f7274d4c-d317-4844-bf3f-5d96175ed2c8.jpeg)

Okay, so, page 1! There's a lot going on here. The most interesting circuit is in the upper left hand side. This seems to generate an analogue voltage, proportional to the motor drive signal. Where have D8 which rectifies the signal coming from SH_A, which is the source of the high side FET in the 3 phase bridge specifically, phase A. This is the output of phase A. Ordinarily, this is a square wave with varying duty cycle - the duty cycle of course varies sinusodally. 

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
