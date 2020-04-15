import random

import discord
import gpt_2_simple as gpt2
from discord.ext import commands

import decbot
import decbot.audio as audio
import decbot.config as config
import music
from decbot.bot.error import NoVoice, BadVoice

sess = gpt2.start_tf_sess()
gpt2.load_gpt2(sess)

offtopic = ["off-topic", "l8-night-vibe-check", "dontworrybhealthy",
            "bpsfm-control"]

words = ["explosion", "detonation", "bomb", "liquid engine", "rocket engine",
         "combustion", "explode"]

missile = """The missile knows where it is at all times. It knows this because it knows where it isn't. By subtracting where it is from where it isn't, or where it isn't from where it is (whichever is greater), it obtains a difference, or deviation. The guidance subsystem uses deviations to generate corrective commands to drive the missile from a position where it is to a position where it isn't, and arriving at a position where it wasn't, it now is. Consequently, the position where it is, is now the position that it wasn't, and it follows that the position that it was, is now the position that it isn't.
In the event that the position that it is in is not the position that it wasn't, the system has acquired a variation, the variation being the difference between where the missile is, and where it wasn't. If variation is considered to be a significant factor, it too may be corrected by the GEA. However, the missile must also know where it was.
The missile guidance computer scenario works as follows. Because a variation has modified some of the information the missile has obtained, it is not sure just where it is. However, it is sure where it isn't, within reason, and it knows where it was. It now subtracts where it should be from where it wasn't, or vice-versa, and by differentiating this from the algebraic sum of where it shouldn't be, and where it was, it is able to obtain the deviation and its variation, which is called error."""


class Mork(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.voice = None
        self.mixer = audio.Mixer()
        self.music = music.Music()

    def is_joined(self, member):
        if not member.voice:
            raise NoVoice('"{}" is not in a voice channel.'.format(member.nick))

        return self.voice and self.voice.channel.id == member.voice.channel.id

    async def join(self, member):
        # Joining the already joined channel is a NOP.
        if self.is_joined(member):
            return

        channel = member.voice.channel
        try:
            if self.voice.is_playing():
                raise BadVoice('Bot is active in "{}".'.format(channel.name))

            # If the bot is waiting in a valid voice channel, the voice client
            # can be moved to the new channel rather than connecting anew.
            await self.voice.move_to(channel)
        except AttributeError:
            # The voice client must be `None` or invalid; create a new one.
            self.voice = await channel.connect()

    async def invoke(self, text):
        req = audio.Request(text)
        audio.tts.convert(req)

        self.mixer.enqueue(req)
        req.cleanup()

        if not self.voice.is_playing():
            self.voice.play(self.mixer)

    @commands.Cog.listener()
    async def on_ready(self):
        self.send_message = self.bot.get_cog('Text').send_message
        if discord.opus.is_loaded():
            return

        path = config.get('opus')
        if path:
            discord.opus.load_opus(path)

        if not discord.opus.is_loaded():
            raise RuntimeError('Could not load libopus.')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            if "autorouter" in message.content.lower():
                await message.channel.send(
                    "never trust the autorouter, you are far better than the one good autorouter that's half a million dollars")
            if any(substring in message.content.lower() for substring in words):
                await message.channel.send(
                    "your friendly local three letter agency is watching")

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.nick}')
        self._last_member = member

    @commands.command()
    async def missile(self, ctx, *, text=None):
        """Mork will tell you about the missile or something else"""
        if text:
            await ctx.channel.send(missile.replace("missile", text))
        else:
            await ctx.channel.send(missile)

    @commands.command()
    async def ask(self, ctx, *, text=None):
        """Mork will answer your questions"""
        length = random.randint(5, 100)
        if text:
            data = gpt2.generate(sess, length=length, prefix=text,
                                 return_as_list=True)[0]
        else:
            data = gpt2.generate(sess, length=length, return_as_list=True)[0]
        await ctx.channel.send(data)
        if ctx.author.voice:
            await self.join(ctx.author)
            await self.invoke(data)
            print("something")

    @commands.command()
    async def F(self, ctx):
        """F"""
        if ctx.author.voice:
            await self.join(ctx.author)
            await self.invoke("""[pr<600,18>][pr<200,18>][pr<1800,23>_>pr<600,18>][pr<300,23>][pr<1800,27>]
[pr<600,18>][pr<300,23>][pr<1200,27>][pr<600,18>][pr<300,23>][pr<1200,27>][pr<600,18>][pr<300,23>][pr<1800,27>]
[pr<600,23>][pr<300,27>][pr<1800,30>][pr<900,27>][pr<900,23>][pr<1800,18>]
[pr<600,18>][pr<200,18>][pr<1800,23>]""")

    @commands.group()
    async def play(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid command passed...')

    @play.command()
    async def random(self, ctx, *, category=None):
        """Plays a random song. Category is optional, can be christmas, country, gospel, rock"""
        await self.join(ctx.author)
        song = self.music.random(category.upper())
        await self.invoke(song)
        await ctx.send(f"Now playing: {song.name}")

    @play.command()
    async def song(self, ctx, *, song):
        """Plays a song. Song list at """
        print(f"Playing: {song}")
        await self.join(ctx.author)
        await self.invoke(self.music.play(song))

    @play.command()
    async def stop(self, ctx):
        """Stops playing"""
        self.voice.stop()

    @play.command()
    async def list(self, ctx):
        """Lists all songs"""
        await ctx.send(
            "https://gist.github.com/nmk456/a4c5b1aac419f4fd3f84491923473f1c")


with open("token.txt", 'r') as f:
    token = f.readlines()[0]

client = commands.Bot(command_prefix="mork ")
client.add_cog(decbot.bot.Voice(client))
client.add_cog(decbot.bot.Text(client))
client.add_cog(decbot.bot.Util(client))
client.add_cog(Mork(client))
client.run(token)
