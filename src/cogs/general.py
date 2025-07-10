import sys
import discord
from discord.ext import commands


class General(commands.Cog):
    """
    The class that contains the general commands of the bot.

    :param client: The bot client.
    :type client: discord.AutoShardedBot

    :ivar client: The bot client.
    :vartype client: discord.AutoShardedBot
    """

    def __init__(self, client: discord.AutoShardedBot) -> None:
        self.client = client
        self.versions = {
            "機器人": "1.0.0",
            "Python": ".".join(
                [
                    str(sys.version_info.major),
                    str(sys.version_info.minor),
                    str(sys.version_info.micro),
                ]
            ),
            "Py-cord": discord.__version__,
        }


    @discord.slash_command(
        name="invite",
        description="邀請機器人至你的伺服器。",
    )
    async def invite(self, ctx: discord.ApplicationContext) -> None:
        """
        The invite command.

        :param ctx: The context of the command.
        :type ctx: discord.ApplicationContext
        """
        await ctx.defer()
        embed = discord.Embed(
            title="邀請機器人",
            description="點擊下方的按鈕來邀請機器人至你的伺服器。",
            color=discord.Color.brand_green(),
        )
        view = discord.ui.View(
            discord.ui.Button(
                label="邀請連結",
                url=f"https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=67584&scope=bot%20applications.commands"
            )
        )
        await ctx.respond(embed=embed, view=view)

    @discord.slash_command(
        name="info",
        description="顯示機器人的資訊。",
    )
    @discord.guild_only()
    async def info(self, ctx: discord.ApplicationContext) -> None:
        """
        The info command.

        :param ctx: The context of the command.
        :type ctx: discord.ApplicationContext
        """
        await ctx.defer()

        ver = "\n".join([f"{k}: **{v}**" for k, v in self.versions.items()])
        users = []
        channels = 0
        for i in self.client.guilds:
            users.extend(iter(i.members))
            channels += len(i.channels)

        embed = discord.Embed(
            title="機器人資訊",
            description="一個富含創意易於使用的錢包機器人，管理員可以透過指令查詢與管理使用者的餘額。",
            color=discord.Color.brand_green(),
        )
        embed.add_field(name="📒 版本", value=ver, inline=False)
        embed.add_field(
            name="📊 數據",
            value=f"正在服務 **{len(self.client.guilds)}** 個伺服器，共 **{channels}** 個頻道。",
            inline=False,
        )
        embed.add_field(
            name="📈 狀態",
            value=f"目前伺服器所在分片: 分片 **{ctx.guild.shard_id}**\n分片延遲: **{round(self.client.latency*1000, 2)}**ms",
            inline=False,
        )

        await ctx.respond(embed=embed)

    @discord.slash_command(
        name="help",
        description="顯示機器人的指令列表。",
    )
    async def help(self, ctx: discord.ApplicationContext) -> None:
        """
        The help command.

        :param ctx: The context of the command.
        :type ctx: discord.ApplicationContext
        """
        await ctx.defer()

        embed = discord.Embed(
            title="幫助訊息",
            description="一個富含創意易於使用的錢包機器人。",
            color=discord.Color.brand_green(),
        )
        embed.add_field(
            name="💰 錢包",
            value=f"""
</balance:{self.client.get_command('balance').id}> - 查詢使用者的餘額。
</list:{self.client.get_command('list').id}> - 查詢伺服器所有使用者的餘額。
            """,
            inline=False,
        )
        embed.add_field(
            name="🔧 管理員設定",
            value=f"""
</set-name:{self.client.get_command('set-name').id}> - 設定伺服器貨幣的名稱。
</set-admin:{self.client.get_command('set-admin').id}> - 設定伺服器的管理員身分組。
            """,
            inline=False,
        )
        embed.add_field(
            name="💡 雜項",
            value=f"""
</info:{self.client.get_command('info').id}> - 顯示機器人的資訊。
</invite:{self.client.get_command('invite').id}> - 邀請機器人至你的伺服器。
</help:{self.client.get_command('help').id}> - 顯示機器人的指令列表。
            """,
            inline=False,
        )
        embed.set_footer(text="如果在使用上有任何問題，歡迎加入支援伺服器請求協助。")
        embed.set_thumbnail(url=self.client.user.display_avatar.url)

        view = discord.ui.View(
            discord.ui.Button(
                label="邀請連結",
                url=f"https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=67584&scope=bot%20applications.commands"
            ),
            discord.ui.Button(
                label="支援伺服器",
                url="https://discord.com/invite/ouo-community-970310299603312701"
            )
        )

        await ctx.respond(embed=embed, view=view)



def setup(client: discord.AutoShardedBot) -> None:
    """
    The setup function for the cog.

    :param client: The bot client.
    :type client: discord.AutoShardedBot
    """
    client.add_cog(General(client))
