from os import getenv

from twitchio.ext import commands

from coc_tools.jobs.responses import greet
from coc_tools import db


class Bot(commands.Bot):
    def __init__(self):
        self.cnxn = db.create_connection()
        # self.session = self.get_last_session()
        super().__init__(
            token=getenv("TWITCH_TOKEN"),
            prefix="?",
            initial_channels=[getenv("TWITCH_CHANNEL")],
        )

    def get_last_session(self):
        prev_sesh = db.last_session(self.cnxn)
        return prev_sesh["name"]

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        print(message.timestamp, end=" - ")
        print(message.author.name, end=":   ")
        print(message.content)

        await self.handle_commands(message)

    @commands.command(aliases=["h"])
    async def help(self, ctx: commands.Context):
        """
        Help command to list all commands
        :param ctx: Twitch context
        :return: None
        """
        message = [
            f"/me Hello, @{ctx.author.name}!",
            "?h[elp] => display all commands",
            "?hello|hi => Be greeted by the bot",
        ]

        for m in message:
            await ctx.send(m)

    @commands.command(aliases=["hi"])
    async def hello(self, ctx: commands.Context):
        """
        Hello command to say hi to user
        :param ctx: Twitch context
        :return: None
        """
        greeting = greet(ctx.author.name)
        message = greeting.get("message")
        await ctx.send(message)

    @commands.command(aliases=["sesh"])
    async def session(self, ctx: commands.Context):
        message = f"current session name: {self.session}"
        await ctx.send(message)


bot = Bot()
bot.run()
