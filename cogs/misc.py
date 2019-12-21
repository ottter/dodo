from discord.ext import commands
from random import choice, randint



class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name='8ball', pass_context=True)
    async def eight_ball(self, context):
        """Ask the magic 8 ball any question"""
        possible_responses = [
            'It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely', 'You may rely on it',
            'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes', 'Reply hazy try again',
            'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
            'Don\'t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
        await context.send(f"🎱 {choice(possible_responses)}, {context.message.author.mention} 🎱")

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(name='roll', aliases=['dice'], pass_context=True)
    async def dice_roll(self, context):
        """Use RNG to roll NdN dice
            .roll  ==== RNG 1-100 result
            .roll 2d6 = RNG 2 6-sided dice rolls"""
        user_id = context.message.author.id
        user_input = str(context.message.content)
        dice = user_input.split(' ', 1)

        try:
            rolls, sides = map(int, dice[1].split('d'))
            result = ', '.join(str(randint(1, sides)) for r in range(rolls))
            await context.send(f'🎲 <@{user_id}> rolled {rolls} d{sides} dice and the results are: 🎲 \n ' + result)

        except IndexError:    # More elegant ways? sure. Easier ways? no.
            result = str(randint(1, 100))
            await context.send(f'🎲 <@{user_id}> rolled 1-100 and got: {result}🎲')

        except Exception as err:
            print(err)
            await context.send('Format has to be in NdN! Example: 4d6')


def setup(bot):
    bot.add_cog(Misc(bot))