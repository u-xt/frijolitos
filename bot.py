import discord
from discord.ext import commands
import random
import re

intents = discord.Intents.default()
intents.message_content = True  # Necessary to access message content
intents.members = True  # Necessary for managing roles and members

bot = commands.Bot(command_prefix='!', intents=intents)

# Target channel
TARGET_CHANNEL_ID = 1278425513731297302
# IDs of the channels to monitor
SOURCE_CHANNEL_IDS = {
    1278426567906693170,
    1278426609224913017,
    1278426586588254239,
    1278426609921163328,
    1278426724249636926,
    1278426610554638419
}

# Accumulated data
user_ids = set()  # Using a set to avoid duplicates
wallet_total_accumulated = 0  # Total accumulated from wallets

# Role ID to assign
ROLE_ID = 1231137098145333250
# Role ID that allows executing commands to change channel names
AUTHORIZED_ROLE_ID = 1233279479535767552

# Channel IDs for "vouche" and "mark"
VOUCHE_CHANNEL_ID = 1231351470809415761
MARK_CHANNEL_ID = 1247340155929366569

# Voice channel ID to rename
VOICE_CHANNEL_ID = 1279491827208028181

def generate_random_value(min_value, max_value):
    """Generates a random value within the given range."""
    return random.randint(min_value, max_value)

# Function to process messages
def process_message(message):
    global user_ids, wallet_total_accumulated
    
    # Extract the User ID
    user_id_match = re.search(r'Username/UserID:\s*([0-9]+)', message)
    if user_id_match:
        user_ids.add(user_id_match.group(1))
    
    # Search for wallet values in the message
    wallet_match = re.search(r'Wallet\s*-\s*\$(\d+[\d,]*)', message)
    if wallet_match:
        wallet_amount = int(wallet_match.group(1).replace(',', ''))
        wallet_total_accumulated += wallet_amount

# Event when a message is received
@bot.event
async def on_message(message):
    if message.channel.id in SOURCE_CHANNEL_IDS:
        process_message(message.content)
    await bot.process_commands(message)

# Command to send the summary
@bot.command(name='AT')
async def send_summary(ctx):
    # Generate random values for the summary
    wallet_total = generate_random_value(1000000, 10000000)
    profit_total = generate_random_value(500000, 5000000)
    atms_total = generate_random_value(1000, 10000)
    
    # Convert the set of User IDs to a list and join them into a string
    user_ids_str = "\n".join(user_ids) if user_ids else "N/A"
    
    embed = discord.Embed(
        title="AutoFarm",
        description=f"**| Wallet: ${wallet_total:,} | Profit: ${profit_total:,} | Passed: 00:00:00\n\nATMs:\n| ATMs - {atms_total}\n\nIDs\n{user_ids_str}\n\n**",
        color=0xFF5733  # Example color
    )
    embed.set_author(name="Xt")
    
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        await target_channel.send(embed=embed)
    else:
        await ctx.send("Could not find the target channel.")

# Command to calculate the total wallets with discount
@bot.command(name='DHC')
async def send_discounted_wallet_total(ctx):
    global wallet_total_accumulated
    
    # Apply a 15% discount
    discounted_total = wallet_total_accumulated * 0.85
    
    embed = discord.Embed(
        title="DHC available",
        description=f"**Accumulated DHC:\n\n${discounted_total:,.2f}**",
        color=0xFF5733  # Example color
    )
    embed.set_author(name="Xt")
    
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        await target_channel.send(embed=embed)
    else:
        await ctx.send("Could not find the target channel.")

# Command to assign a role
@bot.command(name='buyer')
async def assign_role(ctx, member: discord.Member = None, *, user_name=None):
    if not member and user_name:
        # Search for the member by name
        for m in ctx.guild.members:
            if user_name.lower() in m.display_name.lower() or user_name.lower() in str(m).lower():
                member = m
                break
    
    if not member:
        await ctx.send("The mentioned or specified user was not found.")
        return
    
    role = discord.utils.get(ctx.guild.roles, id=ROLE_ID)
    if role:
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(
                f"Thank you for purchasing, {member.mention} :D\n"
                f"Remember to leave your vouche in <#{VOUCHE_CHANNEL_ID}> and your mark in <#{MARK_CHANNEL_ID}>."
            )
        else:
            await ctx.send(f"{member.mention} already has the role.")
    else:
        await ctx.send("Could not find the role.")

# Commands for links
@bot.command(name='1MR')
async def link_1mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/791857328/1MDHC")

@bot.command(name='2MR')
async def link_2mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/791611269/2MDHC")

@bot.command(name='3MR')
async def link_3mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/791622139/3MDHC")

@bot.command(name='4MR')
async def link_4mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/791430982/4MDHC")

@bot.command(name='5MR')
async def link_5mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/811855304/5MDHC")

@bot.command(name='6MR')
async def link_6mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/812078260/6MDHC")

@bot.command(name='7MR')
async def link_7mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/812092148/7MDHC")

@bot.command(name='8MR')
async def link_8mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/811692668/8MDHC")

@bot.command(name='9MR')
async def link_9mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/812048196/9MDHC")

@bot.command(name='10MR')
async def link_10mr(ctx):
    await ctx.send("https://www.roblox.com/es/game-pass/811665691/10MDHC")

# Commands to change the voice channel name
@bot.command(name='ATF')
@commands.has_permissions(administrator=True)  # Only administrators can use this command
async def set_status_farming(ctx):
    if not any(role.id == AUTHORIZED_ROLE_ID for role in ctx.author.roles):
        await ctx.send("You do not have permission to use this command.")
        return

    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        await voice_channel.edit(name="status-Farming🖥️")
        await ctx.send("Voice channel name changed to 'status-Farming🖥️'.")
    else:
        await ctx.send("Could not find the voice channel.")

@bot.command(name='sON')
@commands.has_permissions(administrator=True)  # Only administrators can use this command
async def set_status_online(ctx):
    if not any(role.id == AUTHORIZED_ROLE_ID for role in ctx.author.roles):
        await ctx.send("You do not have permission to use this command.")
        return

    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        await voice_channel.edit(name="status-🟢")
        await ctx.send("Voice channel name changed to 'status-🟢'.")
    else:
        await ctx.send("Could not find the voice channel.")

@bot.command(name='sOF')
@commands.has_permissions(administrator=True)  # Only administrators can use this command
async def set_status_offline(ctx):
    if not any(role.id == AUTHORIZED_ROLE_ID for role in ctx.author.roles):
        await ctx.send("You do not have permission to use this command.")
        return

    voice_channel = bot.get_channel(VOICE_CHANNEL_ID)
    if voice_channel:
        await voice_channel.edit(name="status-🔴")
        await ctx.send("Voice channel name changed to 'status-🔴'.")
    else:
        await ctx.send("Could not find the voice channel.")

# Command to display help information
@bot.command(name='helps')
async def help_command(ctx):
    embed = discord.Embed(
        title="Help Command",
        description="List of available commands:",
        color=0x00FF00
    )
    embed.add_field(name="!AT", value="Sends a summary with random values.", inline=False)
    embed.add_field(name="!DHC", value="Calculates the total wallets with a 15% discount.", inline=False)
    embed.add_field(name="!buyer", value="Assigns a role to a user.", inline=False)
    embed.add_field(name="!1MR", value="Sends the link for 1MDHC.", inline=False)
    embed.add_field(name="!2MR", value="Sends the link for 2MDHC.", inline=False)
    embed.add_field(name="!3MR", value="Sends the link for 3MDHC.", inline=False)
    embed.add_field(name="!4MR", value="Sends the link for 4MDHC.", inline=False)
    embed.add_field(name="!5MR", value="Sends the link for 5MDHC.", inline=False)
    embed.add_field(name="!6MR", value="Sends the link for 6MDHC.", inline=False)
    embed.add_field(name="!7MR", value="Sends the link for 7MDHC.", inline=False)
    embed.add_field(name="!8MR", value="Sends the link for 8MDHC.", inline=False)
    embed.add_field(name="!9MR", value="Sends the link for 9MDHC.", inline=False)
    embed.add_field(name="!10MR", value="Sends the link for 10MDHC.", inline=False)
    embed.add_field(name="!ATF", value="Changes the voice channel name to 'status-Farming🖥️'.", inline=False)
    embed.add_field(name="!sON", value="Changes the voice channel name to 'status-🟢'.", inline=False)
    embed.add_field(name="!sOF", value="Changes the voice channel name to 'status-🔴'.", inline=False)
    embed.add_field(name="!help", value="Displays this help message.", inline=False)

    await ctx.send(embed=embed)

# Start the bot
bot.run('MTI3OTMwMjQ2NjQ0NTM4MTYzMg.G2gp1y.YbFdNK7PvOnhg7mV3s9PmwWX_ibB7gCslqalIA')
