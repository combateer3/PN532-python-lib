# PN532-python-lib
A light library for me to use in my other RFID/NFC projects. Supports 2 types of reads: single and continuous.

### Dependencices
HubCityLabs's [py532lib](https://github.com/HubCityLabs/py532lib)

### Usage
`read_card` is a blocking function, that will return the tag's UID after the card has been removed for a default 2 seconds.

`read_card_continuous` will also block until it reads a tag.  However, it will immediately return the UID.

### Example
```
import rfid


# get uid
uid = rfid.read_card()
print('I read a card with uid: {}'.format(uid))

... do stuff with uid ...
```
