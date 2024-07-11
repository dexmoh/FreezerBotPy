import discord
import bot
import whitelist
import console
import datetime
import time


# *** COMMANDS ***

# Chilly's version of the classic 'ping' command. :)
# For comedic effect, this command isn't documented anywhere.
@bot.bot.command(name='bitch')
async def _bitch(ctx):
    await ctx.send('https://media.discordapp.net/attachments/622200209015046220/831832692835221554/bitch.gif')


# *** PRIVILEGED COMMANDS ***

# Shut down the bot (you'll have to manually turn it back on).
@bot.bot.command(name='shutdown')
async def _shutdown(ctx):
    async with ctx.channel.typing():
        time.sleep(0.8)

        # Check if the user has access to this command.
        if ctx.author.id in whitelist.user_whitelist:
            console.log(f'User {ctx.author.name} (ID: {ctx.author.id}) invoked the shutdown command.')
            await ctx.send('Shutting down... :(')
            await ctx.send('https://cdn.discordapp.com/attachments/805603157484503046/1260199089686056971/yes-power.gif')
            await ctx.bot.close()
        else:
            await ctx.send('https://tenor.com/view/lotr-lord-of-the-rings-theoden-king-of-rohan-you-have-no-power-here-gif-4952489')


# Toggle experimental features off and on.
@bot.bot.command(name='toggle_exp')
async def _toggle_experimental(ctx):
    if ctx.author.id in whitelist.user_whitelist:
        bot.experimental = not bot.experimental
        
        embed = discord.Embed(
            color=bot.color
        )
        
        if bot.experimental:
            console.log(f'User {ctx.author.name} (ID: {ctx.author.id}) enabled experimental features.')
            embed.description = 'Experimental features are now **enabled**.'
        else:
            console.log(f'User {ctx.author.name} (ID: {ctx.author.id}) disabled experimental features.')
            embed.description = 'Experimental features are now **disabled**.'

        embed.set_footer(text=f'Requested by {ctx.author.name}.', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
