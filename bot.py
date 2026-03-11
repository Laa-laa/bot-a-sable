import os
import random
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronise les commandes slash avec Discord
        await self.tree.sync()
        print(f"Commandes synchronisées pour {self.user}")

    async def on_ready(self):
        print(f'Connecté en tant que {self.user} (ID: {self.user.id})')
        print('------')

bot = MyBot()

@bot.tree.command(name="roll", description="Lance un dé (par défaut 6 faces)")
@app_commands.describe(faces="Le nombre de faces du dé (défaut: 6)")
async def roll(interaction: discord.Interaction, faces: int = 6):
    if faces <= 1:
        await interaction.response.send_message("Le nombre de faces doit être supérieur à 1 !", ephemeral=True)
        return
    
    result = random.randint(1, faces)
    await interaction.response.send_message(f"🎲 Tu as lancé un dé à {faces} faces et tu as obtenu : **{result}**")

@bot.tree.command(name="coin", description="Lance une pièce (Pile ou Face)")
async def coin(interaction: discord.Interaction):
    result = random.choice(["Pile", "Face"])
    emoji = "🪙"
    await interaction.response.send_message(f"{emoji} La pièce est tombée sur : **{result}**")

if __name__ == "__main__":
    if not TOKEN:
        print("Erreur: DISCORD_TOKEN n'est pas défini dans le fichier .env")
    else:
        bot.run(TOKEN)
