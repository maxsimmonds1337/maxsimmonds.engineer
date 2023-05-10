# My First Go At GO!

My wife and I recently had our first child. A lot of concerns and worries arise out of having a baby, and you become hyperfocused on their outputs (wee's, poo's, etc!). So, I wrote this tracking app, that has a go backend that's hosted on GCP. It connects to a mySQL DB (also hosted on GCP) to store data such as outputs, and inputs like breast milk, formula, etc. 

There's a few things I want to add, like websockets for the timers (which currently stop when a phone is used and locked), and alerts for large drops in outputs or inputs.

## The submission form
![image](https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/e76e4323-3830-4fb4-819d-325186c1afdb)

## The dashboard
![image](https://github.com/maxsimmonds1337/maxsimmonds.engineer/assets/58208872/87c06c1d-2610-4812-a619-54bd012890fd)

There's currently an issue with the timers not working on phones, due to the use of client side JS for their function. I'm porting this to WebSockets in a hope that'll fix it. Hence the red line if flat above.

## Challenges and experience

- WebSockets
- Running an app with users (all 3 of them!) and a dev enviroment
-- I've been using docker for local dev testing, hosting a mySQL server. Then I push updates to GCP when they're ready
