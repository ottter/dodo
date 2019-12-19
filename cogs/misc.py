from discord.ext import commands
from random import choice


class MiscCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='8ball', pass_context=True)
    async def eight_ball(self, context):
        possible_responses = [
            'It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it',
            'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
            'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
            'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
        await context.send(f"🎱 {choice(possible_responses)}, {context.message.author.mention} 🎱")


def setup(bot):
    bot.add_cog(MiscCommands(bot))