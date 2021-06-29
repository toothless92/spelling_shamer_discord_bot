'''
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
'''

import csv
import os

import discord
from dotenv import load_dotenv
from spellchecker import SpellChecker

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
lwr_case = "abcdefghijklmnopqrstuvwxyz"
upr_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

spell = SpellChecker()

# stack help on words: https://stackoverflow.com/questions/4456446/dictionary-text-file

def create_dict(file, dir=None):	
	'''
	Loads a text file based on the input file and directory strings.
	Returns a set (not a dictionary) in the variable helpfully 
	labeled "dict".
	'''
	# Check for directory input
	if dir is not None:
		# Create filename
		file = os.path.join(dir, file)
	# Create filename
	print("Importing " + file + "...")
	# Create dictionary set
	dict = set([])
	dict = set(line.split(" ")[0].lower() for line in \
		       open(file, 'rt', encoding="utf8")).union(dict)
	print("Dictionary import complete.")
	print("")
	return dict


# oxford.txt is an english dictionary from sujithps https://raw.githubusercontent.com/sujithps/Dictionary/master/Oxford%20English%20Dictionary.txt
ox = create_dict("oxford.txt","words")
# huge.txt is an english dictionary from San Jose http://www.math.sjsu.edu/~foster/dictionary.txt
huge = create_dict("huge.txt","words")
# the slang files are from Matt Bierner's github repo https://github.com/mattbierner/urban-dictionary-word-list
for ltr in upr_case:
	file = ltr + ".data"
	slang = set([])
	slang = slang.union(create_dict(file,"slang"))


def edits1(word):
	'''
	I ended up not using this function, but I thought it was a cool
	implementation, so I am keeping it in case I decide to use it later.
	This function returns a list of all the words that are essentially
	one typo away from the input word.
	https://norvig.com/spell-correct.html
	'''
    # "All edits that are one edit away from `word`."
	letters    = 'abcdefghijklmnopqrstuvwxyz'
	splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
	deletes    = [L + R[1:]               for L, R in splits if R]
	transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
	replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
	inserts    = [L + c + R               for L, R in splits for c in letters]
	return set(deletes + transposes + replaces + inserts)


def rm_trailing_punc(word):
	'''
	Remvoes trailing punctuation
	'''
	# Loop, checking last letter of word for punctuation
	while True:
		if word[-1] in punc:
			# remove last character
			word = word[:-1]
		else:
			# no ending punctuation, return
			return(word)


def is_all_letters(word):
	for c in word:
		if (c not in lwr_case) and (c not in upr_case):
			return False
	return True


def check_dict(word, dict):
	if word in dict:
		return True
	else:
		return False


def process_msg(msg):
	'''
	This function takes a message input and forms a
	**R E P L Y** if a typo is found.
	'''
	# Split sentence into words
	words = msg.split(" ")
	# Loop through every word in sentence
	for word in words:
		print("Examining: " + word)
		# Strip off any trailing punctuation from the word
		word = rm_trailing_punc(word)
		skip_word = False

		# Skip uppercase words.  Too many abbreviations to account for
		if word.isupper(): skip_word = True

		# make word lowercase for simplicity.  All dictionaries are imported as lowercase.
		word = word.lower()
		# Skip the word if it is not just letters
		if not is_all_letters(word): skip_word = True
		# The two english dictionary lookups are definitely redundant, and probably redundant to the
		# spell checker, but I'm going to keep them in for good luck
		if check_dict(word, ox): skip_word = True
		if check_dict(word, huge): skip_word = True
		# Slang dictionary lookup
		if check_dict(word, slang): skip_word = True
		# Check for known word with spell checker
		# This is necessary because the dictionaries are missing
		# things like plurals
		if spell.known([word]) != set(): skip_word = True
		# Skip the word if it is 4 or fewer characters long. There are too
		# many short phrases / sounds to account for
		if len(word) < 5: skip_word = True
		if skip_word:
			print ("\"" + word + "/"" is not a typo.")
			print ("")
			continue
		# Create **R E P L Y**
		response = "**"
		response = response + word[0].upper()
		for c in word[1:]:
			response = response + " " + c.upper()
		response = response + "**"
		print(word + " is not a word!")
		print("")
		return response
	return None


def main():
	client = discord.Client()

	# Function for when bot is connected and ready (one-time, on startup)
	@client.event
	async def on_ready():

		# This prints the name of all servers the bot is currently connected to
		if client.guilds:
			for guild in client.guilds:
				print(
					f'{client.user} is connected to the following guild:\n'
					f'{guild.name}(id: {guild.id})'
				)
	
	# Function for when a new message is recieved
	@client.event
	async def on_message(message):
		if False:
			# This is just here to force the message properties pop up in
			# Visual studio. I am not sorry.
			message = discord.Message()

		# Get message string from message object
		msg = message.content

		# Don't reply to yourself
		if message.author == client.user:
			return

		# Crunch the message and get a reply if a typo is found
		response = process_msg(msg)
		if response is None:
			return
		else:
			await message.channel.send(response)

	print("bot is started.")
	client.run(TOKEN)


if __name__ == "__main__":
	main()