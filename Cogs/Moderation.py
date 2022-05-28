from sre_constants import SUCCESS
import disnake
from disnake import ApplicationCommandInteraction, Embed, Option, OptionType
from disnake.ext import commands

SUCCESS, ERROR = 1,2

def EZEmbed(Title: str, Color: int, Reason: str):
	Colors = {
		SUCCESS: 0x32a852,
		ERROR: 0xE02B2B
	}
	return disnake.Embed(
		title=Title,
		description=Reason,
		color=Colors[Color]
	)



class Moderation(commands.Cog, name='moderation'):
	def __init__(self, bot):
		self.bot = bot

	@commands.slash_command(
		name='warns',
		description='View the warnings of a user',
		options = [
			Option(
				name="user",
				description="The user you want to the warns of",
				type=OptionType.user,
				required=True
			)
		]
	)
	
	@commands.has_permissions(manage_messages=True)
	async def warns(self, interaction: ApplicationCommandInteraction, user: disnake.User):
		await interaction.send('test')
		
	

def setup(bot):
	bot.add_cog(Moderation(bot))