# Run on Metro M4 Airlift w RGB Matrix shield and 64x32 matrix display
# show current value of Bitcoin in USD

import time
import board
import terminalio
import random
from random import randrange

from adafruit_matrixportal.matrixportal import MatrixPortal

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise
# You can display in 'GBP', 'EUR' or 'USD'
CURRENCY = "USD"
# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]
cryptos = ["BTC", "ETH", "LTC", "DOGE"]

#matrixportal PRE-LOAD
matrixportal = MatrixPortal(
        default_bg=cwd + "/loading.bmp",
        status_neopixel = board.NEOPIXEL,
        debug=True
    )

def text_transform(val):
    if CURRENCY == "USD":
        return "$%d" % val
    # if CURRENCY == "EUR":
    #     return "‎€%d" % val
    # if CURRENCY == "GBP":
    #     return "£%d" % val
    # return "%d" % val

#Text1 Price
matrixportal.add_text(
        text_font=terminalio.FONT,
        text_position=(19, 22),
        text_color=0xffffff,
        text_transform=text_transform,
    )

matrixportal.preload_font(b"$012345789.")  # preload numbers
matrixportal.preload_font((0x00A3, 0x20AC))  # preload gbp/euro symbol aa

time.sleep(1)#show first image


def getcryptosdata(crypto, profileid):
    print("getcryptosdata start")
    print("profile id:", profileid)
    APIKEY = secrets["API_KEY"]
    #Use this for coinmarketcap (Free API is very limited)
    #DATA_SOURCE = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol="+crypto+"&CMC_PRO_API_KEY="+ APIKEY
    #DATA_LOCATION = ["data",crypto,"quote","USD","price"] #for this API c means current price

    # use this for Nomics.com (real Free API)
    DATA_SOURCE = "https://api.nomics.com/v1/currencies/ticker?ids="+crypto+"&key="+ APIKEY
    DATA_LOCATION = [0,"price"]

    try:
        crypto_data = matrixportal.network.fetch(DATA_SOURCE)
        crypto_price = matrixportal.network.json_traverse(crypto_data.json(), DATA_LOCATION)

    # pylint: disable=broad-except
    except Exception as error:
        print(error)

    #crypto_price = text_transform(crypto_price)
    crypto_price = str(crypto_price)[:8]
    matrixportal.set_text(crypto_price)
    matrixportal.set_background(cwd + "/Crypto_bg_"+str(profileid)+".bmp")

    #Text2 ticker
    matrixportal.add_text(
        text_font=terminalio.FONT,
        text_position=(37, 7),
        text_color=0xFFFFFF,
        text_transform=text_transform,
    )
    matrixportal.set_text(crypto, 1)


while True:
    for crypto in cryptos:
        print(crypto)
        try:
            getcryptosdata(crypto, cryptos.index(crypto)+1) #the index will be used as bg
            print("after getcryptosdata")
            time.sleep(1 * 10)

        except (ValueError, RuntimeError) as e:
            print("Some error occured, retrying! -", e)

