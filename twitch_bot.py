from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token='',
            prefix='?',
            initial_channels=[""]
        )

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        if message.echo:
            return

        print(message.author.name)
        print(message.timestamp)
        print(message.content)

        await self.handle_commands(message)

    @commands.command(aliases=['h'])
    async def help(self, ctx: commands.Context):
        """Help command to list all commands"""
        message = [
            f'/me Hello, @{ctx.author.name}!',
            "?h[elp] => display all commands"
        ]

        for m in message:
            await ctx.send(m)


bot = Bot()
bot.run()
