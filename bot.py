import os
import random
from datetime import datetime, timezone
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

WORDLE_WORDS = [
    "avion",
    "plage",
    "table",
    "fleur",
    "piano",
    "sable",
    "route",
    "nuage",
    "fruit",
    "bison",
    "crane",
    "glace",
    "livre",
    "monts",
    "perle",
]


def get_daily_word() -> str:
    # Utilise la date UTC pour avoir le meme mot du jour pour tout le monde.
    day_index = datetime.now(timezone.utc).date().toordinal()
    return WORDLE_WORDS[day_index % len(WORDLE_WORDS)]


def evaluate_guess(guess: str, target: str) -> str:
    green = "🟩"
    orange = "🟧"
    red = "🟥"

    result = [red] * len(target)
    remaining = {}

    # 1) Lettres bien placees
    for i, (g_char, t_char) in enumerate(zip(guess, target)):
        if g_char == t_char:
            result[i] = green
        else:
            remaining[t_char] = remaining.get(t_char, 0) + 1

    # 2) Lettres presentes mais mal placees
    for i, g_char in enumerate(guess):
        if result[i] == green:
            continue
        if remaining.get(g_char, 0) > 0:
            result[i] = orange
            remaining[g_char] -= 1

    return "".join(result)

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


@bot.tree.command(name="wordle", description="Tente de trouver le mot du jour")
@app_commands.describe(mot="Ton mot (5 lettres)")
async def wordle(interaction: discord.Interaction, mot: str):
    guess = mot.strip().lower()
    target = get_daily_word()

    if len(guess) != len(target) or not guess.isalpha():
        await interaction.response.send_message(
            f"Ton mot doit contenir exactement {len(target)} lettres (A-Z).",
            ephemeral=True,
        )
        return

    score = evaluate_guess(guess, target)
    if guess == target:
        await interaction.response.send_message(
            f"{score}\nBravo ! Tu as trouvé le mot du jour : **{target.upper()}**"
        )
        return

    await interaction.response.send_message(
        f"{score}\nEssai: **{guess.upper()}**"
    )

if __name__ == "__main__":
    if not TOKEN:
        print("Erreur: DISCORD_TOKEN n'est pas défini dans le fichier .env")
    else:
        bot.run(TOKEN)
