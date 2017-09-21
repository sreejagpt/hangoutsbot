import asyncio
from random import shuffle

import plugins


def _initialise(bot):
    plugins.register_user_command(["toastfact"])


def toastfact(bot, event):
    """
    /bot toastfact
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

    bot.send_message(event.conv, answers[0])
