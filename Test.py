import pexpect
class ChatHandler:
    def __init__(self):
        self.child = pexpect.spawn('python -m parlai interactive --model-file zoo:blenderbot2/blenderbot2_3B/model --search_server ParlAISearchEngine.liyongxin.repl.co', timeout=None)
        self.child.expect('Enter Your Message:')
        self.personality = self.child.before.decode('utf-8', 'ignore').split('[context]')[1]
    def listen(self):
        response = self.child.before
        resp = response.split(b'1m')
        respfinal = resp[1].split(b'\x1b')
        return respfinal[0].decode('utf-8')
    def say(self, message):
        self.child.sendline(message)
        self.child.expect('Enter Your Message:')

import discord
TOKEN = "OTMzNDkzMzMzODY1NjYwNTI2.YeiVag.0dBQFEbfavmHNtZJoEBfVsMguyk"
class Chattr(discord.Client):
    async def on_ready(self):
        self.server_chats = dict()
        for server in self.guilds:
            self.server_chats[server.name] = ChatHandler()
    async def on_message(self, message):
        print(message.content)
        print(message.author.id)
        print(self.user.id)
        if message.content == 'chattrpersona':
            await message.channel.send(chat.personality)
        if message.content == 'chattrforget':
            self.server_chats[message.guild.name].say('[DONE]')
            await message.channel.send('Chat history forgotten.')
        if message.content.startswith("chattr "):
            saying = message.content[7:]
            self.server_chats[message.guild.name].say(saying)
            response = self.server_chats[message.guild.name].listen()
            await message.channel.send(response)
client = Chattr()
client.run('OTMzNDkzMzMzODY1NjYwNTI2.YeiVag.0dBQFEbfavmHNtZJoEBfVsMguyk')
