import discord

client = discord.Client()

words = ["explosion", "detonation", "bomb", "liquid engine", "rocket engine", "combustion", "explode"]

missile = """The missile knows where it is at all times. It knows this because it knows where it isn't. By subtracting where it is from where it isn't, or where it isn't from where it is (whichever is greater), it obtains a difference, or deviation. The guidance subsystem uses deviations to generate corrective commands to drive the missile from a position where it is to a position where it isn't, and arriving at a position where it wasn't, it now is. Consequently, the position where it is, is now the position that it wasn't, and it follows that the position that it was, is now the position that it isn't.
In the event that the position that it is in is not the position that it wasn't, the system has acquired a variation, the variation being the difference between where the missile is, and where it wasn't. If variation is considered to be a significant factor, it too may be corrected by the GEA. However, the missile must also know where it was.
The missile guidance computer scenario works as follows. Because a variation has modified some of the information the missile has obtained, it is not sure just where it is. However, it is sure where it isn't, within reason, and it knows where it was. It now subtracts where it should be from where it wasn't, or vice-versa, and by differentiating this from the algebraic sum of where it shouldn't be, and where it was, it is able to obtain the deviation and its variation, which is called error."""

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user and message.channel.name is not "bpsfm-control":
        pass

    elif message.content.lower() == "mork missile":
        await message.channel.send(missile)

    elif message.content.lower().startswith("mork tell me about "):
        await message.channel.send(missile.replace("missile", message.content[19:]))

    elif message.content.lower().startswith("mork") and len(message.content) > 5:
        await message.channel.send(message.content[5:])

    elif any(substring in message.content.lower() for substring in words):
        await message.channel.send("your friendly local three letter agency is watching")

with open("token.txt", 'r') as f:
    token = f.readlines()[0]
client.run(token)
