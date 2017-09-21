import asyncio
from random import shuffle
# vim: set ts=4 expandtab sw=4

import plugins
from hangups import ChatMessageSegment

import aiohttp
import io
import json
import os.path
import re
import urllib.parse
import plugins

import aiohttp, logging, io, os, re
logger = logging.getLogger(__name__)

def _initialise(bot):
    plugins.register_user_command(["fact"])

@asyncio.coroutine
def fact(bot, event):
    """
    toast fact
    """

    answers = [
        "\"Toast is good\" - Eru and Sreeja",
        "\"I'm a breakfast type of guy. Don't get me wrong. I can cook, I'm kinda nice on the burner, but I enjoy making breakfast. I do it all... Scrambled eggs... French toast... Pancakes... Breakfast is my thing.\" - Ja Rule",
        "\"Unbuttered toast is a substance half complete, and to be forced to eat it in that state is necessarily to feel deprived.\" - John Thorne, 'Pot on the Fire' (2000)",
        "Did you know the average household in the United States spends about 35 hours a year making toast and an estimated 75 million of those household members eat toast every day? http://quickservant.com/weird-facts-about-toasters/",
        "The first toaster had quite the cute name: El Tosto.http://quickservant.com/weird-facts-about-toasters/",
        "The toasting process is known as the Maillard reaction. When bread is subjected to 310 degrees Fahrenheit, the sugars begin to brown and form the crunchy surface toast is delightedly known for. http://quickservant.com/weird-facts-about-toasters/",
        "We didn’t get the electric toaster until 1905. That same year inventor Albert Marsh made the Nichrome wire, which made the electric toaster possible. http://quickservant.com/weird-facts-about-toasters/",
        "The next best thing beyond the electric toaster has to be sliced bread. That’s because in 1933 sliced bread was invented and the American toaster got a boost in popularity. http://quickservant.com/weird-facts-about-toasters/",
        "In 1926 the pop-up toaster debuted and a pricey gift — known for making appearances as wedding gifts. It would cost $150 by today’s standards. http://quickservant.com/weird-facts-about-toasters/",
        "Toasters aren’t just in the American kitchen. They’re in the museum as well. The Smithsonian’s National Museum of American History has about 100 toasters spanning the 18th-20th centuries. http://quickservant.com/weird-facts-about-toasters/",
        "It is said when Nellie Melba gained weight in her later career, Chef Auguste Escoffier created a thin baked toast for her diet, viola, Melba toast. In 1925, the Mayo Brothers prescribed the “Eighteen Day Reducing Diet” to Ethel Barrymore. It included Melba toast, which made the toast very popular at the time. https://mobile-cuisine.com/did-you-know/melba-toast-fun-facts/",
        "If you take sliced bread from the freezer and toast it, you lower its glycaemic index https://www.ncbi.nlm.nih.gov/pubmed/17426743",
        "Toasters kill more people than sharks do. According to the National Geographic there are 5-15 fatal shark attacks in the world every year. The Consumer Product Safety Commission in the US says that more than 300 people are electrocuted by toasters in the US alone every year. https://semanticmarmot.wordpress.com/tag/sharks-vs-toasters/"
    ]

    shuffle(answers)
    image_id = yield from image_validate_and_upload_single("https://i.imgur.com/yIe47Xw.gif", bot)
    yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)

    yield from bot.coro_send_message(event.conv, answers[0] )



def image_validate_link(image_uri, reject_googleusercontent=True):
    """
    validate and possibly mangle supplied image link
    returns False, if not an image link
            <string image uri>
    """

    if " " in image_uri:
        """immediately reject anything with non url-encoded spaces (%20)"""
        return False

    probable_image_link = False

    image_uri_lower = image_uri.lower()

    if re.match("^(https?://)?([a-z0-9.]*?\.)?imgur.com/", image_uri_lower, re.IGNORECASE):
        """imgur links can be supplied with/without protocol and extension"""
        probable_image_link = True

    elif image_uri_lower.startswith(("http://", "https://", "//")) and image_uri_lower.endswith((".png", ".gif", ".gifv", ".jpg", ".jpeg")):
        """other image links must have protocol and end with valid extension"""
        probable_image_link = True

    if probable_image_link and reject_googleusercontent and ".googleusercontent." in image_uri_lower:
        """reject links posted by google to prevent endless attachment loop"""
        logger.debug("rejected link {} with googleusercontent".format(image_uri))
        return False

    if probable_image_link:

        """special handler for imgur links"""
        if "imgur.com" in image_uri:
            if not image_uri.endswith((".jpg", ".gif", "gifv", "webm", "png")):
                image_uri = image_uri + ".gif"
            image_uri = "https://i.imgur.com/" + os.path.basename(image_uri)

            """imgur wraps animations in player, force the actual image resource"""
            image_uri = image_uri.replace(".webm",".gif")
            image_uri = image_uri.replace(".gifv",".gif")

        logger.debug('{} seems to be a valid image link'.format(image_uri))

        return image_uri

    return False

@asyncio.coroutine
def image_upload_single(image_uri, bot):
    logger.info("getting {}".format(image_uri))
    filename = os.path.basename(image_uri)
    r = yield from aiohttp.request('get', image_uri)
    raw = yield from r.read()
    image_data = io.BytesIO(raw)
    image_id = yield from bot._client.upload_image(image_data, filename=filename)
    return image_id

@asyncio.coroutine
def image_validate_and_upload_single(text, bot, reject_googleusercontent=True):
    image_id = False
    image_link = image_validate_link(text, reject_googleusercontent=reject_googleusercontent)
    if image_link:
        image_id = yield from image_upload_single(image_link, bot)
    return image_id
