import discord
from discord.ext import commands, pages

from src.utils.storage import Storage
from src.utils.views import MoneyManageView


class Economic(commands.Cog):
    """
    The class that contains the economic commands of the bot.

    :param client: The bot client.
    :type client: discord.AutoShardedBot

    :ivar client: The bot client.
    :vartype client: discord.AutoShardedBot
    """

    def __init__(self, client: discord.AutoShardedBot) -> None:
        self.client = client
        self.PLACEMENT_EMOJI = {1: "🥇", 2: "🥈", 3: "🥉"}

    @discord.slash_command(
        name="balance",
        description="顯示與管理使用者的餘額。",
    )
    @discord.option(
        name="user",
        description="要顯示的使用者。",
    )
    @discord.guild_only()
    async def balance(self, ctx: discord.ApplicationContext, user: discord.Member = None) -> None:
        """
        The balance command.

        :param ctx: The context of the command.
        :type ctx: discord.ApplicationContext
        :param user: The user to show the balance of.
        :type user: discord.Member
        """
        await ctx.defer()

        if user is None:
            user = ctx.author

        data = await Storage.get_guild_data(ctx.guild.id)
        data["users"].get(str(user.id), 0)

        embed = discord.Embed(
            title="查詢餘額",
            description=f"{user.mention} 擁有 {data['users'].get(str(user.id), 0)} {data['name']}。",
            color=discord.Color.brand_green(),
        ).set_footer(text=f"使用者ID: {user.id}")

        await ctx.respond(embed=embed, view=MoneyManageView())

    @discord.slash_command(
        name="set-name",
        description="設定伺服器的貨幣名稱。",
    )
    @discord.option(
        name="name",
        description="要設定的貨幣名稱。",
    )
    @discord.guild_only()
    @discord.default_permissions(administrator=True)
    async def set_name(self, ctx: discord.ApplicationContext, name: str) -> None:
        """
        The set-name command.

        :param ctx: The context of the command.
        :type ctx: discord.ApplicationContext
        :param name: The name of the money.
        :type name: str
        """
        await ctx.defer(ephemeral=True)

        data = await Storage.get_guild_data(ctx.guild.id)
        data["name"] = name
        await Storage.set_guild_data(ctx.guild.id, data)

        await ctx.respond(f"已將貨幣名稱設置為 {name}。")

    @discord.slash_command(
        name="set-admin",
        description="設定管理員身分組。",
    )
    @discord.option(
        name="role",
        description="要設定的管理員身分組。",
    )
    @discord.guild_only()
    @discord.default_permissions(administrator=True)
    async def set_admin(self, ctx: discord.ApplicationContext, role: discord.Role) -> None:
        """
        The set-admin command.

        :param ctx: The context of the command.
        :type ctx: discord.ApplicationContext
        :param role: The role to set.
        :type role: discord.Role
        """
        await ctx.defer(ephemeral=True)

        data = await Storage.get_guild_data(ctx.guild.id)
        data["admin"] = role.id
        await Storage.set_guild_data(ctx.guild.id, data)

        await ctx.respond(f"已將管理員身分組設置為 {role.mention}。擁有該身分組的使用者可以使用餘額管理按鈕。")

    @discord.slash_command(
        name="list",
        description="列出這個伺服器所有使用者的餘額。",
    )
    @discord.guild_only()
    async def list(self, ctx: discord.ApplicationContext) -> None:
        """
        The list command.

        :param ctx: The context of the command.
        :type ctx: discord.ApplicationContext
        """
        await ctx.defer(ephemeral=True)

        data = await Storage.get_guild_data(ctx.guild.id)
        users = {int(k): v for k, v in data["users"].items() if v != 0}

        if not users:
            return await ctx.respond(f"這個伺服器沒有任何使用者擁有{data['name']}。")

        embed = discord.Embed(
            title="使用者餘額列表",
            description=f"這個伺服器共有 {len(users)} 名使用者擁有{data['name']}。",
            color=discord.Color.brand_green(),
        )

        pgs = []
        sorted_users = sorted(users.items(), key=lambda item: item[1], reverse=True)
        for i, l in enumerate(discord.utils.as_chunks(sorted_users, 10)):
            eb = embed.copy()
            for j, c in enumerate(l, 1):
                place = i * 10 + j
                user = await self.client.get_or_fetch_user(c[0])
                eb.add_field(
                    name=f"{self.PLACEMENT_EMOJI.get(place, place)} - {user.name}#{user.discriminator}",
                    value=f"餘額：{c[1]} {data['name']}",
                    inline=False,
                )
            pgs.append(eb)
        if len(pgs) == 1:
            return await ctx.respond(embed=pgs[0])
        paginator = pages.Paginator(pages=pgs)
        await paginator.respond(ctx.interaction, ephemeral=True)


def setup(client: discord.AutoShardedBot) -> None:
    """
    The setup function for the cog.

    :param client: The bot client.
    :type client: discord.AutoShardedBot
    """
    client.add_cog(Economic(client))
