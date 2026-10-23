
a
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
    await ctx.send("**Server channels:**\n" + "\n".join(names[:40]))

@bot.command()
@admin_only()
async def makechannel(ctx, *, name: str):
    channel = await ctx.guild.create_text_channel(name[:90])
    await ctx.send(f"Created channel: {channel.mention}")

@bot.command()
@admin_only()
async def makerole(ctx, *, name: str):
    role = await ctx.guild.create_role(name=name[:100])
    await ctx.send(f"Created role: {role.name}")

@bot.command()
@admin_only()
async def helpme(ctx):
    await ctx.send(
        "**AS NUKING TOOL commands**\n"
        "`!channels` — list channels\n"
        "`!makechannel name` — create a channel\n"
        "`!makerole name` — create a role\n"
        "`!helpme` — show commands"
    )

token = os.getenv("DISCORD_TOKEN")
if not token:
    raise RuntimeError("Set the DISCORD_TOKEN environment secret.")

bot.run(token)
