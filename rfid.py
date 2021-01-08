from py532lib.i2c import *
import card_timer


def parse_uid(card_data):
    uid = bytearray(4) # mifare classic uses 4 byte uid
    for i in range(4):
        offset = len(card_data) - 4 + i
        uid[i] = card_data[offset]

    return uid


# this is a blocking function
# returns uid of card
# will continuously return as long as the card remains on the reader
def read_card_continuous():
    card_data = pn532.read_mifare().get_data()
    return parse_uid(card_data)


def read_card():
    # get card read
    uid = read_card_continuous()
    # wait until card is removed
    card_timer.card_removal_wait(pn532.read_mifare)
    return uid


pn532 = Pn532_i2c()
pn532.SAMconfigure()

