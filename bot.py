
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def admin_only():
    async def predicate(ctx):
        return (
            ctx.guild is not None
            and ctx.author.guild_permissions.administrator
        )
    return commands.check(predicate)


@bot.event
async def on_ready():
    print(f"AS NUKING TOOL online: {bot.user}")


@bot.command()
@admin_only()
async def channels(ctx):
    names = [c.name for c in ctx.guild.channels]
    await ctx.send("Server channels:\n" + "\n".join(names[:40]))


@bot.command()
@admin_only()
async def roles(ctx):
    names = [r.name for r in ctx.guild.roles]
    await ctx.send("Server roles:\n" + "\n".join(names[:40]))


@bot.command()
@admin_only()
async def ownchannel(ctx, *, name="st4rco-hub"):
    existing = discord.utils.get(
        ctx.guild.text_channels, name=name
    )
    if existing:
        await ctx.send(f"Already exists: {existing.mention}")
        return

    channel = await ctx.guild.create_text_channel(name=name)
    await ctx.send(f"Created: {channel.mention}")


@bot.command()
@admin_only()
async def createrole(ctx, *, name):
    role = await ctx.guild.create_role(name=name)
    await ctx.send(f"Created role: {role.name}")


@bot.command()
async def helpme(ctx):
    await ctx.send(
        "`!channels` - List channels\n"
        "`!roles` - List roles\n"
        "`!ownchannel st4rco-hub` - Create your channel\n"
        "`!createrole Member` - Create a role"
    )


token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("Set the DISCORD_TOKEN secret first.")

bot.run(token)
