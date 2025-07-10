import discord
from discord.interactions import Interaction

from src.utils.storage import Storage


class AddModal(discord.ui.Modal):
    """
    The modal class for the add button.
    """

    def __init__(self, user_id: int) -> None:
        super().__init__(title="增加餘額")
        self.user_id = user_id
        self.add_item(
            discord.ui.InputText(
                label="數量",
                placeholder="請輸入要增加的數量",
            )
        )

    async def callback(self, interaction: Interaction) -> None:
        """
        The callback function for the modal.

        :param interaction: The interaction that the callback is triggered from.
        :type interaction: Interaction
        """
        await interaction.response.defer()

        ans = interaction.data["components"][0]["components"][0]["value"]
        if not ans.isdigit():
            return await interaction.followup.send("請輸入大於0的整數。", ephemeral=True)

        data = await Storage.get_guild_data(interaction.guild.id)
        data["users"][str(self.user_id)] = new = data["users"].get(str(self.user_id), 0) + int(ans)
        await Storage.set_guild_data(interaction.guild.id, data)

        name = data['name']
        await interaction.followup.send(
            f"已為 <@{self.user_id}> 增加了 {ans} {name}。他們現在擁有 {new} {name}。",
            ephemeral=True
        )


class SubModal(discord.ui.Modal):
    """
    The modal class for the sub button.
    """

    def __init__(self, user_id: int) -> None:
        super().__init__(title="減少餘額")
        self.user_id = user_id
        self.add_item(
            discord.ui.InputText(
                label="數量",
                placeholder="請輸入要減少的數量",
            )
        )

    async def callback(self, interaction: Interaction) -> None:
        """
        The callback function for the modal.

        :param interaction: The interaction that the callback is triggered from.
        :type interaction: Interaction
        """
        await interaction.response.defer()

        ans = interaction.data["components"][0]["components"][0]["value"]
        if not ans.isdigit():
            return await interaction.followup.send("請輸入大於0的整數。", ephemeral=True)

        data = await Storage.get_guild_data(interaction.guild.id)
        data["users"][str(self.user_id)] = new = data["users"].get(str(self.user_id), 0) - int(ans)
        await Storage.set_guild_data(interaction.guild.id, data)

        name = data['name']
        await interaction.followup.send(
            f"已從 <@{self.user_id}> 減少了 {ans} {name}。他們現在擁有 {new} {name}。",
            ephemeral=True
        )


class MoneyManageView(discord.ui.View):
    """
    The view class for the money command.
    """

    def __init__(self) -> None:
        super().__init__(timeout=None)

    async def on_check_failure(self, interaction: Interaction) -> None:
        """
        The event that is triggered when the check fails.

        :param interaction: The interaction that the check failed.
        :type interaction: Interaction
        """
        await interaction.response.send_message("你沒有權限使用這個按鈕。", ephemeral=True)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """
        The interaction check function for the view.

        :param interaction: The interaction to check.
        :type interaction: discord.Interaction
        :return: Whether the interaction is allowed.
        :rtype: bool
        """
        data = await Storage.get_guild_data(interaction.guild.id)
        return (
            discord.utils.find(lambda r: r.id == data["admin"], interaction.user.roles) is not None
            if data["admin"]
            else interaction.user.guild_permissions.administrator
        )

    @discord.ui.button(
        label="增加餘額",
        custom_id="add",
        style=discord.ButtonStyle.green,
    )
    async def add(self, _: discord.ui.Button, interaction: discord.Interaction) -> None:
        """
        The add button.

        :param _: The button that was clicked.
        :type _: discord.ui.Button
        :param interaction: The interaction of the button.
        :type interaction: discord.Interaction
        """
        ori = interaction.message
        user_id = int(ori.embeds[0].footer.text.removeprefix("使用者ID: "))
        await interaction.response.send_modal(AddModal(user_id))

    @discord.ui.button(
        label="減少餘額",
        custom_id="sub",
        style=discord.ButtonStyle.green,
    )
    async def sub(self, _: discord.ui.Button, interaction: discord.Interaction) -> None:
        """
        The sub button.

        :param _: The button that was clicked.
        :type _: discord.ui.Button
        :param interaction: The interaction of the button.
        :type interaction: discord.Interaction
        """
        ori = interaction.message
        user_id = int(ori.embeds[0].footer.text.removeprefix("使用者ID: "))
        await interaction.response.send_modal(SubModal(user_id))
