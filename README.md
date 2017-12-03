# SMS Bot [![Build Status](https://travis-ci.org/Aahung/sms-bot.svg?branch=master)](https://travis-ci.org/Aahung/sms-bot) [![Coverage Status](https://coveralls.io/repos/github/Aahung/sms-bot/badge.svg?branch=master)](https://coveralls.io/github/Aahung/sms-bot?branch=master)

<p align="center">
    <img title="screen shot" src="screenshot.png" />
</p>

Project for [UBC Hacks' Local Hack Day 2017](https://hackday.mlh.io/ubchacks?em=537). To fulfill the theme "accessibility," we aim to provide information services for people unable to access the internet (e.g., elders).

## Capabilities

### Weather (Vancouver)

We provide rain volume and temperature (feel) information. (provider: [The Weather Network](https://www.theweathernetwork.com))

```
weather now
weather today
weather tomorrow
```

### Stock Price
(provider: [IEX](https://iextrading.com))

```
stock appl
stock fb
```

### Exchange Rate
(provider: [Fixer](http://fixer.io))

```
exchange 3 CAD to usd
exchange RUB to usd
exchange HKD
exchange 0.8 gbp
```

### UBC Exam (CPSC only)
(provider: [UBC](http://ubc.ca))

```
ubc exam cpsc 110
ubc exam CPSC 310
```

### UBC Professor Phone
(provider: [UBC](http://ubc.ca))

```
ubc prof well smith
ubc prof john doe
```

## Tech Details

- [Twilio](https://www.twilio.com/) for sending/receiving SMS
- [AWS Lambda](https://aws.amazon.com/lambda/) for backends. 
