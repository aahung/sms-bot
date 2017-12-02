# SMS Bot

![screenshot](screenshot.png)

Project for [UBC Hacks' Local Hack Day 2017](https://hackday.mlh.io/ubchacks?em=537). To fulfill the theme "accessibility," we aim to provide information services for people unable to access the internet (e.g., elders).

## Capabilities

### Weather (Vancouver)

We provide rain volume and temperature (feel) information.

```
weather now
weather today
weather tomorrow
```

### Stock Price
```
stock appl
stock fb
```

### Exchange Rate
```
exchange 3 CAD to usd
exchange RUB to usd
exchange HKD
exchange 0.8 gbp
```

## Tech details

- [Twilio](https://www.twilio.com/) for sending/receiving SMS
- [AWS Lambda](https://aws.amazon.com/lambda/) for backends. 