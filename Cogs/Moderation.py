from sre_constants import SUCCESS
import disnake
from disnake import ApplicationCommandInteraction, Embed, Option, OptionType
from disnake.ext import commands

SUCCESS, ERROR = 1,2

warning1 = 715331218186436679
warning2 = 715331294136893470
warning3 = 715331322385793137
logchannelId = 801880622187544576

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
				description="The user you want to view the warns of",
				type=OptionType.user,
				required=True
			)
		]
	)

	@commands.has_permissions(manage_messages=True)
	async def warns(self, interaction: ApplicationCommandInteraction, user: disnake.User): 
		mydb = self.bot.Database
		if not mydb.is_connected():
			mydb.reconnect(attempts=3, delay=0)
		cursor = mydb.cursor()
		cursor.execute(f"SELECT * FROM warnings WHERE UserID={user.id}")
		result = cursor.fetchall()
		mydb.commit()
		embed = disnake.Embed(title=f"Warnings for {user}")
		
		if len(result) == 0:
			embed.description = 'This user has no warnings.'
		else:
			for x in result:
				try:
					b = await self.bot.getch_user(int(x[1]))
					embed.add_field(name=f'Warning `ID:{x[3]}`', value=f'Reason: `{x[2]}` | Warned by: {b}`({x[1]})`',inline=False)
				except:
					embed.add_field(name=f'Warning `ID:{x[3]}`', value=f'Reason: `{x[2]}` | Warned by: `({x[1]})`',inline=False)

		await interaction.send(embed=embed)
		

	@commands.slash_command(
		name='warn',
		description='Warn a user',
		options = [
			Option(
				name="member",
				description="The user you want to warn",
				type=OptionType.user,
				required=True
			),
			Option(
				name="reason",
				description="The reason why you're warning this person",
				type=OptionType.string,
				required=False
			)
		]
	)

	@commands.has_permissions(manage_messages=True)
	async def warn(self, interaction: ApplicationCommandInteraction, member: disnake.User, reason: str = 'No reason provided.'):
		mydb = self.bot.Database
		if not mydb.is_connected():
			mydb.reconnect(attempts=3, delay=0)
		
		if member:
			logchannel = self.bot.get_channel(logchannelId)
			if member.bot == True:
				await interaction.send("You can't warn a bot!")
				return
			if interaction.author == member:
				await interaction.send("You can't warn yourself!")
				return

			
			cursor = mydb.cursor()
			cursor.execute(f"INSERT INTO warnings (UserId, ModID, Reason) VALUES({member.id}, {interaction.author.id}, '{reason}')")
			cursor.execute("SELECT LAST_INSERT_ID();")
			result = cursor.fetchall()
			result = result[0][0]

			embed = disnake.Embed(title = 'User Was Warned!')
			embed.description = f"{interaction.author}({interaction.author.id}) warned {member.mention}({member.id})! `Warning ID: {result}`"

			await logchannel.send(embed=embed)
			await interaction.send(embed=embed)

			cursor.execute(f"SELECT * FROM warnings WHERE UserID={member.id}")
			result = cursor.fetchall()
			mydb.commit()

			try:
				await member.remove_roles(interaction.guild.get_role(warning1))
			except:
				pass
			try:
				await member.remove_roles(interaction.guild.get_role(warning2))
			except:
				pass
			try:
				await member.remove_roles(interaction.guild.get_role(warning3))
			except:
				pass

			if len(result) == 1:
				await member.add_roles(interaction.guild.get_role(warning1))
			elif len(result) == 2:
				await member.add_roles(interaction.guild.get_role(warning1))
				await member.add_roles(interaction.guild.get_role(warning2))
			elif len(result) == 3:
				await member.add_roles(interaction.guild.get_role(warning1))
				await member.add_roles(interaction.guild.get_role(warning2))
				await member.add_roles(interaction.guild.get_role(warning3))
			elif len(result) > 3:
				await interaction.channel.send(f"{member.mention} was banned for >3 warnings!")
				await interaction.guild.ban(member, reason=">3 Warnings")

	@commands.slash_command(
		name='delwarn',
		description='Delete a warning',
		options = [
			Option(
				name="warningid",
				description='The warning ID',
				type=OptionType.integer,
				required=True
			)
		]
	)

	@commands.has_permissions(manage_roles=True)
	async def delwarn(self, interaction: ApplicationCommandInteraction, warningid:int=None):
		mydb = self.bot.Database
		if not mydb.is_connected():
			mydb.reconnect(attempts=3, delay=0)
		logchannel = self.bot.get_channel(logchannelId)
		cursor = mydb.cursor()
		cursor.execute(f"DELETE FROM warnings WHERE warningID={warningid}")
		mydb.commit()

		await interaction.send(f"Deleted warning with ID `{warningid}`")
		embed = disnake.Embed(title = 'Warning Deleted')
		embed.description = f"{interaction.author.mention}({interaction.author.id} deleted warning with ID `{warningid}`"

		await logchannel.send(embed=embed)


def setup(bot):
	bot.add_cog(Moderation(bot))