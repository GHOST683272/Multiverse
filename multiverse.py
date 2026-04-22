from discord.ext import commands
import discord


token = "Enter your bot token here"


bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

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

    if message.channel.name != "multiverse":
        await bot.process_commands(message)
        return
    
    username=getattr(message.author,"display_name",message.author.name)
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

bot.run(token)
