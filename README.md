# spelling_shamer_discord_bot

This is a simple Discord bot that reads recent messages, and if
it finds a typo, replies with the misspelled word in
obnoxious **I M P A C T** font. 

This was just a fun project to practice some python and API skills.
The bot searches a few english and slang dictionaries for words to ignore,
in addition to using the pyspellchecker module. It will also ignore
words less than 5 characters long, words that are all-caps, and words
that have punctuation other than at the end. This is in an attempt
to reduce the number of false-triggers.  

This is a great tutorial for getting started with a discord bot:
https://realpython.com/how-to-make-a-discord-bot-python/  

You will need to make a .env file in the same directory as this
file with this information:  
DISCORD_TOKEN="YOUR_DISCORD_TOKEN"  

Once you've set up the application on discord's website and created
the .env, all you need to do is add the bot to a server and run this file:
python main.py. Refer to the tutorial with questions.  

Written by Mike Reilly
Contact mreilly92@gmail.com with questions
