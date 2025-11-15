import interactions
import os

# ----------------------------------------------------
# BOT SETUP
# ----------------------------------------------------
TOKEN = os.getenv("DISCORD_TOKEN")  # or replace with string directly

bot = interactions.Client(
    token=TOKEN,
    intents=interactions.Intents.ALL,
)


# ----------------------------------------------------
# /create-group COMMAND
# ----------------------------------------------------
@interactions.slash_command(
    name="create-group",
    description="Create a temporary private channel with a specific user."
)
@interactions.AutoDefer()
@interactions.option(
    name="member",
    description="Member to invite",
    type=interactions.OptionType.USER,
    required=True
)
async def create_group(ctx: interactions.SlashContext, member: interactions.Member):

    guild = ctx.guild

    # Create a private text channel
    channel = await guild.create_channel(
        name=f"private-{member.id}",
        type=interactions.ChannelType.GUILD_TEXT,
        permission_overwrites=[
            # Deny everyone
            interactions.Overwrite(
                id=guild.id,
                type=0,  # role
                deny=interactions.Permissions.VIEW_CHANNEL
            ),
            # Allow inviter temporarily
            interactions.Overwrite(
                id=ctx.author.id,
                type=1,  # member
                allow=interactions.Permissions.VIEW_CHANNEL
            ),
            # Allow target member
            interactions.Overwrite(
                id=member.id,
                type=1,  # member
                allow=interactions.Permissions.VIEW_CHANNEL
            )
        ]
    )

    await channel.send(f"{member.mention}, you have been added to this private channel.")

    # Remove inviter access
    await channel.modify_permission(
        ctx.author.id,
        type=1,
        deny=interactions.Permissions.VIEW_CHANNEL
    )

    await ctx.send(f"Private group created: <#{channel.id}>")


# ----------------------------------------------------
# START BOT
# ----------------------------------------------------
bot.start()
