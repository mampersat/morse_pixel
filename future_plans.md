# Morse Pixel
## Future Plans

Have as a beta study hall project - give one away to kids and tell them how to build another one. Maybe host a class/hackathon where beta employees run the class. Demo the class in a Beta Bytes of Knowledge

# Location awareness
Gonna need an IP... internet knows where you are

## Beta Bytes of Knowledge pitch

The Morse Pixel Project
Dress Rehersal

## Concept:
The data team at Beta collects and visualizes data. Being able to hold this ability in your hand should inspire kids to think about all the pieces that make this possible. It will undoubtable get people at Beta talking about other ways to use pieces of this thing to do awesome data.

'''
The Protoype:
<picture>

The Beta Version:
<picture>

Financials:
* Cost of package: pico + neopixel + button ~= $10
* Hiring costs saved if one kids dorky parent who gets it working 
* Patents Baby! (or open source)

Open source all the things:
* Details on git repo with all the information needed to fab your own board
* Risk: Miss those sweet, sweet patents
* Reward: Save a life, like Volvo's seatbelt... write the press release

The package:
<pictures>

The challange:
Grafana dashboard subscribed to messsages with properly formatted team name. Bonus points for unicode characters
'''

## The ring version
A ring with a beautifyly mounted jewel. Looks awesome with no blinky powers.

Touch it and it lights up

Pair it with another one that one will light up to, via MQTT messages over the internet

Buy 2, give one to your mom. Save the world.

Give them away one at a time. Charge $100 for the matching ring, or a custom one that matches whatever ring you want.

Basically a smart ring... but don't be so lame about forcing apps onto the people. We're saving the world here.

Dunbars number is 150... people you actually know... this is way too high

ChatGPT says "Overall, many people might wear between 1 to 3 rings regularly"

Pairing invovles touching the rings or something else kewl like leaving one on top of the other an hour

Party mode = throw  your rings into a bucket/glass and shake them and they all pair for 24hrs, there are cheap (or expensive) rings already in 
the pool. Maybe literaly in the pool.

Prototype could be bracelette. Easier to fab at home.


## Airplane Sensor Vesion
Battery + Microcontroller + Sensor + LED

Sensor changes value, MQTT message is transmitter

Either sensor change or MQTT recieved lights the LED

An indepentadly powered sensor and MQTT broadcasting device not much larger than a single neopixel

USB-C for charging and configuration

Possible wireless charging... depends on the size of a reciever thing circle

Maybe power from standard watch type battery? Not sure if they are rechargeable e-cigarette battery = 200 mAh

If device can run for 24hrs it needs to only draw like 10mA

Pico pi draws 2A, so it would last 6 min, according to ChatGPT

ChatGPT says a pico draws 50mA: That's 4hrs in active mode, 13.3 hours in Idle Mode, and 17.5 years in deep sleep mode... whoa

Don't use Beta resources on this project. Including Beta's supsidied Copilot login

Pitch:
1. Show radio + board you fabbed for $5
1. Show prototype board w/Morse Pixel running
1. Show MicroStrain device with one wire... explain it's capabilities... then cut the wire
1. Show jewl - would be kewl if it was wired to a something
1. Indicate it charges in an hour from 0 to 200 mAh: "Anybody know long it takes to use 200 mAh?"
  1. What if this thing woke up when an accelromter tiggere it, lit a pixel and send a MQTT message?
(Problem here... if it doesn't move for an hour and the temperature changes, it's gonna miss that, respond it's designed to instrument things that move... move or die)

It's like a fitbit for your airplane




