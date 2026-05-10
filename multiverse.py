from discord.ext import commands
import discord
import asyncio
import re

token = "Enter your token here"


bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
TEMP_BLACKLIST_MINUTES = 30
spam_cache = {}
temp_blacklist = {}
perma_blacklist = set()
LINK_REGEX = re.compile( r"(https?:\/\/|www\.|discord\.gg)",re.IGNORECASE)
@bot.event
async def on_ready():
    print(f"{bot.user} is ready")
    try:
        synced = await bot.tree.sync()
        for i in synced:
            print(i)
        print("These are active commands!")
    except Exception as e:
        print(e)

@bot.tree.command(name="setup_multiverse", description="Interlinking servers")
async def setup_multiverse(interaction: discord.Interaction):

    if not interaction.user.guild_permissions.manage_channels:
        return await interaction.response.send_message(
            "You need Manage Channels permission.",
            ephemeral=True
        )

    if not interaction.guild.me.guild_permissions.manage_channels:
        return await interaction.response.send_message(
            "I don't have permission to create channels.",
            ephemeral=True
        )

    if not interaction.user.guild_permissions.manage_webhooks:
        return await interaction.response.send_message(
            "You need Manage Webhooks permission.",
            ephemeral=True
        )

    if not interaction.guild.me.guild_permissions.manage_webhooks:
        return await interaction.response.send_message(
            "I don't have permission to manage webhooks.",
            ephemeral=True
        )

    try:
        existing = discord.utils.get(
            interaction.guild.text_channels,
            name="multiverse"
        )

        if existing:
            return await interaction.response.send_message(
                f"{existing.mention} already exists.",
                ephemeral=True
            )

        channel = await interaction.guild.create_text_channel(
            name="multiverse",
            slowmode_delay=5
        )

        webhook = await channel.create_webhook(name="Multiverse")

        await interaction.response.send_message(
            f"Created {channel.mention}\n"
            f"Webhook: `{webhook.name}`"
        )

    except discord.Forbidden:
        await interaction.response.send_message(
            "Bot lacks required permissions.",
            ephemeral=True
        )

@bot.event
async def on_message(message):

    if message.author.bot:
        return
    user_id = message.author.id
    current_time = asyncio.get_event_loop().time()

    # ================= PERMA BLACKLIST ================= #

    if user_id in perma_blacklist:
        try:
            await message.delete()
        except:
            pass
        return
# ====================== TEMP BLACKLIST =================== #
    if user_id in temp_blacklist:
        expiry = temp_blacklist[user_id]
        if current_time<expiry:
            try:
                await message.delete()
            except:
                pass
            return
        else:
            temp_blacklist.pop(user_id,None)

# ======================== REPITITION SPAM ====================== # 
    if user_id not in spam_cache:
        spam_cache[user_id] = []
    spam_cache[user_id].append({
        "content":message.content.strip().lower(),
        "time":current_time
    })
    spam_cache[user_id]=[msg for msg in spam_cache[user_id] if current_time - msg["time"] <= 15]
    same_messages = [msg for msg in spam_cache[user_id] if msg["content"] == message.content.strip().lower()]
    if len(same_messages)>= 3:
        expiry = (
            asyncio.get_event_loop().time() + (TEMP_BLACKLIST_MINUTES*60)
        )
        temp_blacklist[user_id] = expiry
        try:
            await message.delete()
        except:
            pass
        spam_cache[user_id]=[]
        return await message.channel.send(f"{message.author.mention} temporarily blacklisted for spam",delete_after=5)
    if message.channel.name != "multiverse":
        await bot.process_commands(message)
        return
    # ======================= LINK BLOCK ========================== #
    if LINK_REGEX.search(message.content):
        try:
            await message.delete()
        except:
            pass
        return await message.channel.send(f"{message.author.mention} links are not allowed.",delete_after=5)
    
    #username=getattr(message.author,"display_name",message.author.name)
    for guild in bot.guilds:
        for ch in guild.text_channels:

            if ch.name == "multiverse" and ch.id != message.channel.id:

                try:
                    webhooks = await ch.webhooks()
                    webhook = discord.utils.get(webhooks, name="Multiverse")

                    if webhook is None:
                        webhook = await ch.create_webhook(name="Multiverse")

                    await webhook.send(
                        content=message.content or "",
                        username=message.author.display_name,
                        avatar_url= message.author.display_avatar.url
                    )

            
                    for att in message.attachments:
                        await webhook.send(
                            att.url,
                            username=f"{message.author.display_name}",
                            avatar_url=message.author.display_avatar.url
                        )
                except Exception as e:
                    print(f"Error: {e}")

            
    await bot.process_commands(message)
# =========================== Permanent Blacklist ============================= #
@bot.tree.command(name="blacklist",description="Perma blaclist")
async def blacklist(interaction:discord.Interaction,user_id:str):
    if not interaction.user.id == 407913114818969611:
        return await interaction.response.send_message(f"{interaction.user.id} You're not the guy",ephemeral=True)
    try:
        user_id= int(user_id)
        perma_blacklist.add(user_id)
        await interaction.response.send_message(f"{user_id} Perma Blacklisted.",ephemeral=True)
    except:
        await interaction.response.send_message(f"Invalid user id {user_id}",ephemeral=True)
@bot.tree.command(name="unblacklist",description="remove from blacklist")
async def unblacklist(interaction:discord.Interaction,user_id:str):
    if not interaction.user.id == 407913114818969611:
        return await interaction.response.send_message(f"{interaction.user.id} You're not the guy")
    try:
        user_id = int(user_id)
        perma_blacklist.discard(user_id)
        temp_blacklist.pop(user_id,None)
        await interaction.response.send_message(f"User {user_id} unblacklisted",ephemeral=True)
    except:
        await interaction.response.send_message(f"Invalid user id {user_id}",ephemeral=True)
    
bot.run(token)
