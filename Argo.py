import discord
from discord.ext import commands, tasks
from transformers import AutoModelForCausalLM, AutoTokenizer, BigBirdForQuestionAnswering, BigBirdTokenizer
import torch

token = ''
client = commands.Bot(command_prefix='>')
channel = client.get_channel()
# GPT MODEL
#tokenizer = AutoTokenizer.from_pretrained("Poly-Pixel/shrek-medium-full")
#model = AutoModelForCausalLM.from_pretrained("Poly-Pixel/shrek-medium-full")

# BIGBIRD MODEL
tokenizer = BigBirdTokenizer.from_pretrained("vasudevgupta/bigbird-roberta-natural-questions")
# BIGBIRD MODEL by default its in `block_sparse` mode with num_random_blocks=3, block_size=64
model = BigBirdForQuestionAnswering.from_pretrained("vasudevgupta/bigbird-roberta-natural-questions")

@tasks.loop(seconds=300.0)
async def my_background_task():
    """Will loop every 60 seconds and change the bots presence"""
    await client.change_presence(activity=discord.Game(name='About to 360 no scope outta here'))

@client.event
async def on_ready():
	print(f'Logged in as {client.user} (ID: {client.user.id})')
	print('------')
	# Waiting until the bot is ready
	await client.wait_until_ready()
	# Starting the loop
	my_background_task.start()

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	#step = 1
	# GPT MODEL encode the new user input, add the eos_token and return a tensor in Pytorch
	#new_user_input_ids = tokenizer.encode(message.content + tokenizer.eos_token, return_tensors='pt')

	# GPT MODEL append the new user input tokens to the chat history
	#bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

	# GPT MODEL generated a response while limiting the total chat history to 1000 tokens
	#chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

	# GPT MODEL pretty print last ouput tokens from bot
	#response = "{}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True))
	print(message.content)
	# BIGBIRD MODEL
	encoded_input = tokenizer(message.content, return_tensors='pt')
	response = model(**encoded_input)

	await message.channel.send(response)
	return

client.run(token)