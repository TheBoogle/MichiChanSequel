from sre_constants import SUCCESS
import disnake
from disnake import ApplicationCommandInteraction, Embed, Option, OptionType
from disnake.ext import commands

import random
import math

SUCCESS, ERROR = 1,2

def generateXP():
	return random.randrange(75,125)
	
def calculateLevel(xp):
	return int(math.sqrt(xp) / 2)

def calculateXp(level):
	return int((level ** 2) * 4)

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



class Levels(commands.Cog, name='levels'):
	def __init__(self, bot):
		self.bot = bot

		@self.bot.event
		async def on_message(ctx):
			mydb = self.bot.Database
			
			if ctx.author.bot == False and len(ctx.content) > 1:
				xp = generateXP()
				cursor = mydb.cursor()
				cursor.execute("SELECT user_xp FROM users WHERE client_id = "+str(ctx.author.id))
				result = cursor.fetchall()
				if len(result) == 0:
					cursor.execute("INSERT INTO users VALUES(" + str(ctx.author.id) + "," + str(xp) + ')')
				else:
					originalXP = result[0][0]

					OriginalLevel = calculateLevel(originalXP)

					currentXP = result[0][0] + xp
					
					newLevel = calculateLevel(currentXP)

					# if newLevel > OriginalLevel and newLevel >= 500:
					# 	await ctx.author.send(f"You just leveled up to level {newLevel}!")

					if currentXP >= calculateXp(102) and ctx.guild.id == 883924611530625034:
						
						role = ctx.guild.get_role(914578267917389824)
						
						member = ctx.author
						roles = [role for role in member.roles]
						i=0
						found=False
						while i < len(roles):
							currentrole=roles[i]

							if role.id == currentrole.id:
								found=True
								
							i=i+1
						
						
						if not found:
							role = ctx.guild.get_role(914578267917389824)
							await ctx.author.add_roles(role)
							await ctx.channel.send(f"{member.mention} You have unlocked the Media Access role, you can now send images in the media channel.")

					if currentXP >= calculateXp(100) and ctx.guild.id == 460932049394728990:
						
						role = ctx.guild.get_role(460944551130169346)
						
						member = ctx.author
						roles = [role for role in member.roles]
						i=0
						found=False
						while i < len(roles):
							currentrole=roles[i]

							if role.id == currentrole.id:
								found=True
								
							i=i+1
						
						
						if not found:
							role = ctx.guild.get_role(460944551130169346)
							await ctx.author.add_roles(role)
							await ctx.channel.send(f"Congragulations {member.mention} on hitting level 100! Enjoy the Advanced AGM members role")

					if currentXP >= calculateXp(200) and ctx.guild.id == 460932049394728990:
						
						role = ctx.guild.get_role(787042501780701225)
						
						member = ctx.author
						roles = [role for role in member.roles]
						i=0
						found=False
						while i < len(roles):
							currentrole=roles[i]

							if role.id == currentrole.id:
								found=True
								
							i=i+1
						
						
						if not found:
							role = ctx.guild.get_role(787042501780701225)
							await ctx.author.add_roles(role)
							await ctx.channel.send(f"Congragulations {member.mention} on hitting level 200! Enjoy the Mega-Advanced AGM members role")

					cursor.execute("UPDATE users SET user_xp = "+ str(currentXP)+" WHERE client_id = " +str(ctx.author.id))
				mydb.commit()

	@commands.slash_command(
		name='rank',
		description='Get a users rank',
		options = [
			Option(
				name="user",
				description="The user you want view the rank of",
				type=OptionType.user,
				required=False
			)
		]
	)
	
	async def rank(self, interaction: ApplicationCommandInteraction, user: disnake.User=None):
		mydb = self.bot.Database
		if user == None:
			user = interaction.author
		try:
			cursor = mydb.cursor()
			cursor.execute("SELECT user_xp FROM users WHERE client_id = "+str(user.id))
			result = cursor.fetchall()
			xp=result[0][0]
			embed = disnake.Embed(title=user.name+"#"+user.discriminator, color=user.color)
			level_number = calculateLevel(int(result[0][0]))
			embed.add_field(name="LVL", value = str(level_number))
			totalxp=xp
			cursor.execute('SET @row_number=0')
			cursor.execute("SELECT (@row_number:=@row_number + 1) AS num, client_id, user_xp FROM users ORDER BY user_xp DESC")
			result3 = cursor.fetchall()
			i=0
			found=False
			while i < len(result3):

				if result3[i][1] == user.id:
					
					embed.add_field(name="GLOBAL RANK", value="Rank #"+str(result3[i][0])+" / "+str(len(result3)))
					found=True
					break
				i=i+1
			embed.add_field(name="XP", value = str(xp-calculateXp(level_number)) +"/"+str(calculateXp(level_number+1)-calculateXp(level_number)))
			embed.add_field(name="Total XP", value = str(totalxp))
			await interaction.send(embed=embed)
		except:
			embed=EZEmbed('Error!',ERROR,'That user is not in the database.')

			await interaction.send(embed=embed)
		
	@commands.slash_command(
		name='top',
		description='Gets the leaderboard of user ranks',
		options = []
	)

	async def top(self, interaction: ApplicationCommandInteraction):
		await interaction.send('`Loading leaderboard...`')
		lines = 10
		start = 0
		mydb = self.bot.Database
		cursor = mydb.cursor()
		cursor.execute(f"SELECT user_xp from users ORDER BY user_xp DESC LIMIT {lines}")
		result = cursor.fetchall()
		cursor.execute(f"SELECT client_id from users ORDER BY user_xp DESC LIMIT {lines}")
		result2 = cursor.fetchall()
		embed = disnake.Embed(title="Global Leaderboard",color=0xFFFF00)
		if lines == None:
			lines = len(result)
			if lines > 10:
				lines = 10
		
		lines = lines + start

		i=start
		if i < 0: 
			i=0
		runs=1+start
		if lines > len(result):
			lines = len(result)

		

		while i < lines:
			member = await self.bot.getch_user(result2[i][0])
			# member = ctx.guild.get_member(result2[i][0])

			if member == None:
				pass
			else:
				embed.add_field(name="@"+str(member)+" RANK: #"+str(runs), inline=False, value="**Level**: "+str(calculateLevel(result[i][0]))+" **Total XP**: "+str(result[i][0]))
				runs=runs+1
			i=i+1
			

		cursor.execute("SET @row_number = 0")
		cursor.execute("SELECT (@row_number:=@row_number + 1) AS num, client_id, user_xp FROM users ORDER BY user_xp DESC")
		result3 = cursor.fetchall()
		i=0
		found=False
		while i < len(result3):
			if result3[i][1] == interaction.author.id:
				embed.set_footer(text="@"+interaction.author.name+"#"+interaction.author.discriminator+" is rank #"+str(result3[i][0])+" / "+str(len(result3)))
				found=True
				break
			i=i+1
		await interaction.delete_original_message()
		await interaction.send(embed=embed)


def setup(bot):
	bot.add_cog(Levels(bot))