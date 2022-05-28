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
		name='kick',
		description='Kick a user out of the server.',
		options = [
			Option(
				name="user",
				description="The user you want to kick",
				type=OptionType.user,
				required=True
			),
			Option(
				name='reason',
				description="The reason you kicked the user.",
				type=OptionType.string,
				required = False
			)
		]
	)

	

	@commands.has_permissions(kick_members=True)
	async def kick(self, interaction: ApplicationCommandInteraction, user: disnake.User, reason: str = "No reason provided."):
		member = await interaction.guild.get_or_fetch_member(user.id)
		
		if member.guild_permissions.administrator:
			await interaction.send(embed=EZEmbed('Error!', ERROR, 'User is an admin!'))
		else:
			try:
				Embed = EZEmbed('User Kicked!', SUCCESS, f'**{member}** was kicked by **{interaction.author}**')
				Embed.add_field(
					name = 'Reason: ',
					value = reason
				)
				await interaction.send(embed=Embed)

				try:
					Embed.description = f'You were kicked by **{interaction.author}** in **{interaction.guild}**'
					await member.send(embed=Embed)
				except:
					pass
				#await member.kick(reason=reason)

			except:
				Embed = EZEmbed('Error!', ERROR, f'Failed to kick.')
				await interaction.send(embed=Embed)

def setup(bot):
	bot.add_cog(Moderation(bot))