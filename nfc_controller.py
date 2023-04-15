"""
    This example will attempt to connect to an ISO14443A
    card or tag and retrieve some basic information about it
    that can be used to determine what type of card it is.   
   
    To enable debug message, set DEBUG in nfc/PN532_log.h
"""
import time
import binascii
from threading import Thread

from pn532pi import Pn532, pn532
from pn532pi import Pn532I2c
from pn532pi import Pn532Spi
from pn532pi import Pn532Hsu

# Set the desired hardware interface to True
SPI = False
I2C = True
HSU = False

if SPI:
    PN532_SPI = Pn532Spi(Pn532Spi.SS0_GPIO8)
    nfc = Pn532(PN532_SPI)
# When the number after #elif set as 1, it will be switch to HSU Mode
elif HSU:
    PN532_HSU = Pn532Hsu(0)
    nfc = Pn532(PN532_HSU)

# When the number after #if & #elif set as 0, it will be switch to I2C Mode
elif I2C:
    PN532_I2C = Pn532I2c(1)
    nfc = Pn532(PN532_I2C)


class RFIDTag:
    # Class for adding RFID tags to look for with the NFC reader
    # Example:
    # RFIDTag(b'041c676cdf6181',callback_stub , 'HOLOTAPE_ZETA_INVADERS' )
    # uuid - Tag Identifier that should be in byte code format
    # function_callback - do we want to call anything when we find the tag?
    #  label - how the tag gets identified by the controller
    uuid_ = ""
    read_ = False
    label_ = ""
    callback_ = None

    def __init__(self, uuid, function_callback, label):
        self.uuid_ = uuid
        self.callback_ = function_callback
        self.label_ = label

    def found(self):
        self.read_ = True
        self.callback_(self)

    def synchronously_process_tag_if_read(self):
        self.callback_()
        self.read_ = False


class NFCController(Thread):
    # Controller class for PN532 NXP NFC Analogue front end
    # Example use
    # n = NFCController()
    # ... AD TAGS TO TRACK
    # n.start() - to kick off the monitoring thread
    rfid_tag_list_ = []

    def __init__(self):
        super().__init__()
        nfc.begin()

        versiondata = nfc.getFirmwareVersion()
        if not versiondata:
            print("Didn't find PN53x board")
            raise RuntimeError("Didn't find PN53x board")  # halt

        # Got ok data, print it out!
        print(
            "Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format(
                (versiondata >> 24) & 0xFF,
                (versiondata >> 16) & 0xFF,
                (versiondata >> 8) & 0xFF,
            )
        )
        # Set the max number of retry attempts to read from a card
        # This prevents us from waiting forever for a card, which is
        # the default behaviour of the pn532.
        # nfc.setPassiveActivationRetries(0xFF)

        # configure board to read RFID tags
        nfc.SAMConfig()

        print("Waiting for an ISO14443A card")

    def run(self):
        while True:
            try:
                # Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
                # 'uid' will be populated with the UID, and uidLength will indicate
                # if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
                success, uid = nfc.readPassiveTargetID(
                    pn532.PN532_MIFARE_ISO14443A_106KBPS
                )

                if success:
                    print("Found a card!")
                    # TODO[dchapman] Figure out why ISO14443A doesn't need this nasty hack / msg gate it
                    time.sleep(1)
                    self.check_taglist_for_result(binascii.hexlify(uid))
            except:
                # we mostly want this to fail quietly and keep tyrying
                # should put some sane error handling here when / if we care
                nfc.SAMConfig()
                time.sleep(1)

    def check_taglist_for_result(self, present_uuid):
        for tag in self.rfid_tag_list_:
            if tag.uuid_ == present_uuid:
                tag.found()

    def add_tag(self, tag):
        self.rfid_tag_list_.append(tag)

    def remove_tag_by_lable(self, label):
        for tag in self.rfid_tag_list_:
            if tag.label_ == label:
                self.rfid_tag_list_.remove(tag)
                return True
        return False


# This is just a callback for test code, in use this would call a state change or update based
# on what tag is present
def callback_stub(tag):
    print(f"FOUND {tag.label_}")


if __name__ == "__main__":
    n = NFCController()
    n.add_tag(RFIDTag(b"041c676cdf6181", callback_stub, "HOLOTAPE_ZETA_INVADERS"))
    n.add_tag(RFIDTag(b"04e3786ddf6180", callback_stub, "HOLOTAPE_PIPFALL"))
    n.start()
