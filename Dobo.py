# The os module helps us access environment variables
# I.e., our API keys
import os

# For the random splash texts
import random
import re
from sre_parse import Tokenizer

# This module are for loading models from Huggingface
# from transformers import BlenderbotSmallTokenizer, BlenderbotSmallForConditionalGeneration
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration

# The Discord Python API
import discord
from discord.ext import commands, tasks

# Load the tokenizer and model
# model_name = 'facebook/blenderbot_small-90M'
model_name = 'facebook/blenderbot-1B-distill'
# model_name = 'facebook/blenderbot-3B'
tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
model = BlenderbotForConditionalGeneration.from_pretrained(model_name, use_cache=True)
# tokenizer = BlenderbotSmallTokenizer.from_pretrained(model_name)
# model = BlenderbotSmallForConditionalGeneration.from_pretrained(model_name, use_cache=True)

token = 'OTMzNDkzMzMzODY1NjYwNTI2.YeiVag.0dBQFEbfavmHNtZJoEBfVsMguyk'

@tasks.loop(seconds=300.0)
async def my_background_task(client):
    """Will loop every 60 seconds and change the bots presence"""
    line = random.choice(open('splash.txt').readlines())
    await client.change_presence(activity=discord.Game(name=line))

class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()

    def query(self, payload):
        """
        Tokenizes the message content
        """
        data = tokenizer([payload], return_tensors='pt')
        response = model.generate(**data)
        return response

    async def on_ready(self):
        # Print out information when the bot wakes up
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        print('------')

        # Waiting until the bot is ready
        await self.wait_until_ready()

        # Starting the loop
        my_background_task.start(self)

        # Send a request to the model without caring about the response
        # Just so that the model wakes up and starts loading
        self.query('Hello!')

    async def on_message(self, message):
        """
        This function is called whenever the bot sees a message in a channel
        """
        # Ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        # While the bot is waiting on a response from the model
        # Set the its status as typing for user-friendliness
        async with message.channel.typing():
            response = self.query(message.content)
        bot_response = tokenizer.batch_decode(response)
        
        # We may get ill-formed response if the model hasn't fully loaded
        # Or has timed out
        if not bot_response:
            bot_response = 'Hmm... something is not right.'

        bot_response[0] = re.sub('__start__', "", bot_response[0])
        bot_response[0] = re.sub('__end__', "", bot_response[0])

        # Send the model's response to the Discord channel
        await message.channel.send(bot_response[0])

def main():
    client = MyClient('blenderbot_small-90M')
    client.run(token)

if __name__ == '__main__':
    main()
