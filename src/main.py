import tracemalloc

import decouple
import discord

from src.utils.views import MoneyManageView


class Bot(discord.AutoShardedBot):
    """
    The main class of the bot.
    """

    def __init__(self) -> None:
        super().__init__(
            intents=discord.Intents.default(),
            activity=discord.Game(name="錢錢💰")
        )
        self._client_ready = False
        self.load_extension("src.cogs", recursive=True)

    async def on_shard_connect(self, shard_id: int) -> None:
        """
        The event that is triggered when a shard connected.

        :param shard_id: The shard ID.
        :type shard_id: int
        """
        print(f"Shard {shard_id} connected.")

    async def on_shard_ready(self, shard_id: int) -> None:
        """
        The event that is triggered when a shard is ready.

        :param shard_id: The shard ID.
        :type shard_id: int
        """
        print(f"Shard {shard_id} ready.")

    async def on_shard_resumed(self, shard_id: int) -> None:
        """
        The event that is triggered when a shard resumed.

        :param shard_id: The shard ID.
        :type shard_id: int
        """
        print(f"Shard {shard_id} resumed.")

    async def on_shard_disconnect(self, shard_id: int) -> None:
        """
        The event that is triggered when a shard disconnected.

        :param shard_id: The shard ID.
        :type shard_id: int
        """
        print(f"Shard {shard_id} disconnected.")

    async def on_ready(self) -> None:
        """
        The event that is triggered when the bot is ready.
        """
        if self._client_ready:
            return

        self.add_view(MoneyManageView())

        print("-------------------------")
        print(f"Logged in as: {self.user.name}#{self.user.discriminator} ({self.user.id})")
        print(f"Shards Count: {self.shard_count}")
        print(f"Memory Usage: {tracemalloc.get_traced_memory()[0] / 1024 ** 2:.2f} MB")
        print(f" API Latency: {self.latency * 1000:.2f} ms")
        print(f" Guild Count: {len(self.guilds)}")
        print("-------------------------")
        self._client_ready = True

    async def on_message(self, message: discord.Message) -> None:
        """
        The event that is triggered when a message is sent.

        :param message: The message that is sent.
        :type message: discord.Message
        """
        if (
            message.mentions and self.user in message.mentions
            and message.channel.permissions_for(message.guild.me).send_messages
        ):
            embed = discord.Embed(
                title="感謝選用錢叡",
                description=f"""
                錢叡是一個富含創意易於使用的錢包機器人。
                他可以幫助你管理伺服器的經濟。
                你可以使用 </help:{self.get_command('help').id}> 來查看指令列表。
                """,
                color=discord.Color.brand_green()
            )
            embed.set_footer(text="如果在使用上有任何問題，歡迎加入支援伺服器請求協助。")
            embed.set_thumbnail(url=self.user.display_avatar.url)
            view = discord.ui.View(
                discord.ui.Button(
                    label="邀請連結",
                    url=f"https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=67584&scope=bot%20applications.commands"
                ),
                discord.ui.Button(
                    label="支援伺服器",
                    url="https://discord.com/invite/ouo-community-970310299603312701"
                )
            )
            await message.reply(embed=embed, view=view)

    def run(self) -> None:
        super().run(decouple.config("token"))
