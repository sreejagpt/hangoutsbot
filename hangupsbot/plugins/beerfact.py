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
    plugins.register_user_command(["beerfact"])

@asyncio.coroutine
def beerfact(bot, event):
    """
    beer fact
    """

    answers = [
        "Germans celebrate Father's day by having \"oddly dressed men pulling wagons filled with beer into parks and drinking until they pass out.\" http://www.spiegel.de/international/zeitgeist/father-s-day-in-germany-is-one-big-booze-fest-a-833802.html",
        "The first athlete to be disqualified at the Olympics for drug use was a Swedish pentathlete who drank two beers before his shooting event to calm his nerves. https://en.wikipedia.org/w/index.php?title=Hans-Gunnar_Liljenwall",
        "Did you know an Amsterdam anti-litter campaign hired alcoholics to pick up trash and paid them in beer? http://www.bbc.com/news/world-europe-25548061",
        "Microbiologist Raul Cano, successfully revived yeast that had been stuck in amber for 25 million years. He then co-founded a brewery that uses the same 45 million-year-old species of yeast to brew beer. http://www.bbc.com/news/world-europe-25548061",
        "Wisconsin Police busted a teen kegger in which the keg was filled with root beer. The party organizer was trying to show that they didn't need to drink alcohol for a party. http://www.nbcnews.com/id/23851011/ns/us_news-weird_news/t/cops-bust-teens-root-beer-kegger/",
        "A Florida-based beer company created fully edible 6-pack rings from brewing byproducts such as wheat and barley; the rings are just as strong as the plastic variety, yet completely digestible and biodegradable. http://blogs.discovermagazine.com/d-brief/2016/05/18/edible-six-pack-rings/#.V44rojUjrgY",
        "During the global hop shortage of 2008, the Samuel Adams Beer Company sold 20,000 pounds of their excess hops to over 200 craft breweries, at cost. This helped prevent the breweries from going out of business. http://www.chicagotribune.com/bluesky/hub/chi-inc-samuel-adams-jim-koch-bsi-hub-ngux-story.html",
        "Weird Al turned down $5 million, in the late 80s, to endorse a beer company. He thought it was ethically wrong because, \"a lot of his fans were young and impressionable.\" http://www.vintagevinylnews.com/2010/11/weird-al-yankovic-regrets-turning-down.html",
        "'The Villages', An over-55 community, has the highest consumption of draft beer and STD rate in the state of Florida. http://www.slate.com/articles/life/florida/features/2013/oh_florida/the_villages_scandals_irs_stds_golf_carts_and_made_up_history.html",
        "Beer bottles are brown because brown glass blocks harmful UV sunlight, preserving the taste. However due to a shortage during WWII most beer companies were forced to use clear glass and higher quality beer makers chose green to distinguish themselves. http://berghoffbeer.com/blog/what-does-the-color-of-your-beer-bottle-mean/",
        "Carlsberg beer used to have a Swastika (as a symbol of purity) in its logo. They removed it in 1940 after the Nazi's appropriated it. http://www.historynet.com/swastika-imprinted-bottle.htm"
        "Andre the Giant set the world record for number of beers consumed in a single sitting by drinking 119 12oz beers in six hours. 1976. https://www.usatoday.com/story/life/nation-now/2016/07/27/andre-the-giant-drinking-stories-feats-insane/87616884/"
        "That Schlitz was the number one beer in America in the early 1950s and then they started messing with the ingredients to cut costs and the plant was closed less than 30 years later. https://beerconnoisseur.com/articles/how-milwaukees-famous-beer-became-infamous"
        "In 1759 Arthur Guinness, founder of Guinness beer, leased an old unused brewery for £45 per year... for 9,000 YEARS. https://en.wikipedia.org/wiki/Arthur_Guinness"
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
