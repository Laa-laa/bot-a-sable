import os
import random
import json
import aiohttp
import urllib.parse
import urllib.request
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# Charge les variables d'environnement depuis le fichier .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Fichier de stockage de l'état du jeu (chemin absolu)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_STATE_FILE = os.path.join(SCRIPT_DIR, "wordle_state.json")
SCORE_FILE = os.path.join(SCRIPT_DIR, "scores.json")

# Scores en mémoire
scores = {}


def load_scores():
    """Charge les scores depuis le fichier JSON."""
    global scores
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, 'r', encoding='utf-8') as f:
                scores = json.load(f)
                print(f"[SCORE] Scores chargés: {len(scores)} joueur(s)")
        except Exception as e:
            print(f"[SCORE] Erreur lors du chargement: {e}")
            scores = {}
    else:
        scores = {}


def save_scores():
    """Sauvegarde les scores dans le fichier JSON."""
    try:
        with open(SCORE_FILE, 'w', encoding='utf-8') as f:
            json.dump(scores, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[SCORE] Erreur lors de la sauvegarde: {e}")


def add_score(user_id: str, points: int):
    """Ajoute des points à un joueur et sauvegarde."""
    scores[user_id] = scores.get(user_id, 0) + points
    save_scores()
    return scores[user_id]

WORDLE_WORDS = [
    "abime", "acier", "adieu", "agile", "aigle", "album", "alpin",
    "angle", "antre", "appel", "arbre", "arche", "arene", "argot",
    "armer", "astre", "atome", "avion", "azote", "badge", "bague",
    "banal", "bande", "barge", "baron", "bazar", "biche", "bilan",
    "bison", "bocal", "boite", "bonze", "bosse", "botte", "brave",
    "brise", "brume", "bulle", "cable", "cache", "cadre", "calme",
    "canal", "canne", "carat", "carte", "champ", "chaos", "chaud",
    "chene", "chute", "cidre", "cible", "clame", "clone", "clore",
    "cobra", "coeur", "colis", "colza", "comte", "corde", "corne",
    "corps", "coude", "coupe", "crane", "creux", "crise", "cycle",
    "dague", "dalle", "darne", "daube", "debut", "delta", "dense",
    "depot", "desir", "dette", "digue", "dingo", "dolce", "doyen",
    "drame", "droit", "duvet", "eclat", "ecran", "effet", "egout",
    "eleve", "email", "encre", "enfer", "enjeu", "entre", "envoi",
    "epais", "epice", "epine", "epoux", "essai", "etang", "etape",
    "etole", "etuve", "eveil", "exile", "extra", "fable", "farce",
    "faste", "faune", "fente", "ferme", "fesse", "fiche", "figue",
    "filet", "flair", "fleau", "fleur", "flore", "fonte", "foret",
    "forge", "frime", "frise", "froid", "fugue", "fumet", "fusee",
    "galet", "galon", "gamme", "garde", "gaule", "genie", "genou",
    "geste", "givre", "glace", "gland", "globe", "grace", "grand",
    "griot", "grume", "guide", "guise", "hamac", "harpe", "herse",
    "houle", "huile", "humus", "hyene", "icone", "idole", "image",
    "index", "jambe", "joute", "jupon", "label", "lacet",
    "laine", "lande", "large", "laser", "leche", "lemme", "leste",
    "liane", "liege", "ligne", "limon", "linge", "litre", "livre",
    "lodge", "loupe", "lourd", "lueur", "lutin", "magot", "maire",
    "malin", "malle", "mange", "manne", "masse", "mater", "meche",
    "melee", "melon", "merle", "metal", "mitre", "mixte", "modem",
    "monde", "monts", "morue", "moule", "moyen", "mulet", "nappe",
    "natte", "naval", "niche", "niece", "noeud", "noyer", "nuage",
    "obese", "octet", "ombre", "opale", "opium", "orage", "ordre",
    "orgue", "otage", "ozone", "palme", "panne", "patio", "pause",
    "piano", "piece", "piege", "pince", "piste", "pivot", "pixel",
    "plage", "plaid", "plein", "plomb", "plume", "poeme", "pouce",
    "poule", "prime", "prose", "pulpe", "quart", "queue", "radio",
    "rafle", "ravin", "rayon", "rebut", "recit", "regle", "rejet",
    "renne", "reves", "rhume", "robot", "roche", "roman", "rosee",
    "rouge", "route", "ruche", "ruine", "sable", "sabot", "sauge",
    "serum", "sirop", "sobre", "sonar", "soude", "soupe", "stade",
    "stage", "style", "sucre", "suite", "sujet", "table", "talon",
    "tango", "tapis", "temps", "tenor", "tente", "terme", "titre",
    "toile", "tombe", "tonne", "totem", "tours", "trace", "trame",
    "treve", "trone", "trust", "tueur", "turbo", "tyran", "ultra",
    "union", "usine", "usure", "utile", "valse", "varan", "veine",
    "venin", "verge", "verre", "vertu", "vigie", "vigne", "villa",
    "vitre", "voile", "volet", "wagon", "yacht", "zebre", "zones",
]

# Dictionnaire en mémoire (rechargé au démarrage)
game_state = {}


def load_state():
    """Charge l'état du jeu depuis le fichier JSON."""
    global game_state
    if os.path.exists(GAME_STATE_FILE):
        try:
            with open(GAME_STATE_FILE, 'r', encoding='utf-8') as f:
                game_state = json.load(f)
                print(f"[WORDLE] État chargé: {len(game_state)} joueur(s)")
        except Exception as e:
            print(f"[WORDLE] Erreur lors du chargement: {e}")
            game_state = {}
    else:
        game_state = {}


def save_state():
    """Sauvegarde l'état du jeu dans le fichier JSON."""
    try:
        with open(GAME_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WORDLE] Erreur lors de la sauvegarde: {e}")


LOSS_MESSAGES = [
    "Oh non ! 6 essais, c'est trop pour toi ? Même un enfant de 5 ans trouverait ce mot ! Le mot était : **{word}**",
    "Pauvre amateur ! Tu as échoué après 6 essais... Comment c'est possible ? Le mot était : **{word}**",
    "C'est pathétique ! 6 essais et tu n'as toujours pas trouvé ? Le mot était : **{word}**",
    "Oof, 0 sur 6... T'as besoin de prendre des cours ! Le mot était : **{word}**",
    "Franchement, tu devrais avoir honte. 6 essais pour RIEN ! Le mot était : **{word}**",
    "Catastrophe absolue ! Même mon grand-mère avec les yeux fermés trouverait ! Le mot était : **{word}**",
]


def evaluate_guess(guess: str, target: str) -> str:
    """Évalue un guess et retourne les carrés colorés."""
    green = "🟩"
    orange = "🟧"
    red = "🟥"

    result = [red] * len(target)
    remaining = {}

    # 1) Marquer les lettres bien placées
    for i, (g_char, t_char) in enumerate(zip(guess, target)):
        if g_char == t_char:
            result[i] = green
        else:
            remaining[t_char] = remaining.get(t_char, 0) + 1

    # 2) Marquer les lettres présentes mais mal placées
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
    user_id = str(interaction.user.id)
    total = add_score(user_id, result)
    await interaction.response.send_message(
        f"🎲 Tu as lancé un dé à {faces} faces et tu as obtenu : **{result}**\n"
        f"➕ **+{result} points** | 🏆 Score total : **{total} pts**"
    )


@bot.tree.command(name="coin", description="Lance une pièce (Pile ou Face)")
async def coin(interaction: discord.Interaction):
    result = random.choice(["Pile", "Face"])
    emoji = "🪙"
    user_id = str(interaction.user.id)
    points = 15
    total = add_score(user_id, points)
    await interaction.response.send_message(
        f"{emoji} La pièce est tombée sur : **{result}**\n"
        f"➕ **+{points} points** | 🏆 Score total : **{total} pts**"
    )


WORDS_5 = [w for w in WORDLE_WORDS if len(w) == 5]
wordle_lock = __import__('asyncio').Lock()


def new_word():
    return random.choice(WORDS_5)


def save_game_state():
    try:
        with open(GAME_STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[WORDLE] Erreur sauvegarde: {e}")


@bot.tree.command(name="wordle", description="Tente de trouver le mot du jour")
@app_commands.describe(mot="Ton mot (5 lettres)")
async def wordle(interaction: discord.Interaction, mot: str):
    await interaction.response.defer()

    user_id = str(interaction.user.id)
    guess = mot.strip().lower()

    # Validation en premier, avant tout traitement
    if len(guess) != 5 or not guess.isalpha():
        await interaction.followup.send(
            "Ton mot doit contenir exactement 5 lettres (A-Z) !",
            ephemeral=True,
        )
        return

    # Verrou : un seul traitement à la fois pour éviter toute race condition
    async with wordle_lock:

        # Initialiser le joueur s'il n'existe pas en mémoire
        if user_id not in game_state:
            word = new_word()
            game_state[user_id] = {"word": word, "attempts": 0}
            save_game_state()
            print(f"[WORDLE] Nouveau joueur {user_id}: mot = {word}")

        player = game_state[user_id]
        target = player["word"]

        # Incrémenter les essais
        player["attempts"] += 1
        attempts_left = 6 - player["attempts"]
        save_game_state()

        print(f"[WORDLE] Joueur {user_id}: essai #{player['attempts']} = '{guess}' (cible: '{target}')")

        # Évaluation
        score = evaluate_guess(guess, target)

        # Victoire
        if guess == target:
            attempts_done = player['attempts']
            # Bonus selon le nombre d'essais : 50 pts + jusqu'à 50 pts de bonus
            base_points = 50
            bonus = max(0, (6 - attempts_done) * 10)
            gained = base_points + bonus
            wordle_total = add_score(user_id, gained)
            await interaction.followup.send(
                f"{score}\n✅ **Bravo !** Tu as trouvé le mot **{target.upper()}** en {attempts_done} essai(s) ! 🎉\n"
                f"➕ **+{gained} points** (50 pts + {bonus} pts bonus vitesse) | 🏆 Score total : **{wordle_total} pts**"
            )
            w = new_word()
            game_state[user_id] = {"word": w, "attempts": 0}
            save_game_state()
            print(f"[WORDLE] Joueur {user_id}: victoire ! Nouveau mot = {w}")
            return

        # Défaite
        if attempts_left <= 0:
            loss_message = random.choice(LOSS_MESSAGES).format(word=target.upper())
            await interaction.followup.send(loss_message)
            w = new_word()
            game_state[user_id] = {"word": w, "attempts": 0}
            save_game_state()
            print(f"[WORDLE] Joueur {user_id}: défaite ! Nouveau mot = {w}")
            return

        # Essai normal
        await interaction.followup.send(
            f"{score}\nEssai: **{guess.upper()}** | Essais restants: **{attempts_left}/6**"
        )


@bot.tree.command(name="find", description="Recherche une page Wikipédia et affiche son introduction")
@app_commands.describe(mot="Le mot ou sujet à rechercher sur Wikipédia")
async def find(interaction: discord.Interaction, mot: str):
    await interaction.response.defer()
    user_id = str(interaction.user.id)
    query = mot.strip()

    def fetch_wiki_sync(lang: str, title: str):
        params = urllib.parse.urlencode({
            "action": "query",
            "titles": title,
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
            "format": "json",
            "formatversion": 2,
        })
        url = f"https://{lang}.wikipedia.org/w/api.php?{params}"
        print(f"[FIND] Requête : {url}")
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "DiscordBot/1.0 (https://github.com/bot; contact@example.com) Python/3"
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                pages = data.get("query", {}).get("pages", [])
                if not pages:
                    return None
                page = pages[0]
                if page.get("missing"):
                    return None
                extract = page.get("extract", "").strip()
                if not extract:
                    return None
                title_found = page.get("title", title)
                page_url = f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title_found.replace(' ', '_'))}"
                print(f"[FIND] Trouvé : {title_found}")
                return {"title": title_found, "extract": extract, "url": page_url}
        except Exception as e:
            print(f"[FIND] Erreur : {e}")
            return None

    loop = __import__('asyncio').get_event_loop()
    data = await loop.run_in_executor(None, fetch_wiki_sync, "fr", query)
    lang_used = "fr"
    if data is None or data.get("type") in ("disambiguation", "no-extract"):
        data = await loop.run_in_executor(None, fetch_wiki_sync, "en", query)
        lang_used = "en"

    if data is None or data.get("type") in ("disambiguation", "no-extract"):
        await interaction.followup.send(
            f"❌ Aucune page Wikipédia trouvée pour **{query}**.",
            ephemeral=True
        )
        return

    title = data.get("title", query)
    extract = data.get("extract", "Pas de texte disponible.")
    page_url = data.get("content_urls", {}).get("desktop", {}).get("page", "")
    lang_flag = "🇫🇷" if lang_used == "fr" else "🇬🇧"

    # Tronquer si trop long pour Discord
    if len(extract) > 1000:
        extract = extract[:1000].rsplit(" ", 1)[0] + "…"

    total = add_score(user_id, 1)
    await interaction.followup.send(
        f"{lang_flag} **{title}**\n\n{extract}\n\n"
        f"🔗 {page_url}\n"
        f"➕ **+1 point** | 🏆 Score total : **{total} pts**"
    )


@bot.tree.command(name="score", description="Affiche ton score total")
async def score_cmd(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    total = scores.get(user_id, 0)
    await interaction.response.send_message(
        f"🏆 **Score de {interaction.user.display_name}** : **{total} pts**\n"
        f"Tu peux gagner des points avec :\n"
        f"🪙 `/coin` → +15 pts\n"
        f"🎲 `/roll` → +X pts (selon le résultat du dé)\n"
        f"📝 `/wordle` → +50 pts (+ bonus vitesse) en cas de victoire"
    )


if __name__ == "__main__":
    load_scores()
    load_state()

    if not TOKEN:
        print("Erreur: DISCORD_TOKEN n'est pas défini dans le fichier .env")
    else:
        bot.run(TOKEN)