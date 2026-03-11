# Bot Discord RPG 🐇

Un bot Discord RPG simple en français, avec des **easter eggs liés aux lapins**.

## Fonctionnalités

- Création de personnage avec `/start`
- Profil joueur avec `/profil`
- Exploration et combats via `/explore`
- Repos pour récupérer des PV via `/repos`
- Inventaire avec `/inventaire`
- Quête aléatoire avec `/quete`
- Événements cachés « lapins » (objets, rencontres, bonus)

## Prérequis

- Node.js 18+
- Un bot Discord créé sur le portail développeur

## Installation

1. Installer les dépendances :

```bash
npm install
```

2. Copier `.env.example` vers `.env` et remplir les valeurs.

3. Inviter le bot avec les scopes :

- `bot`
- `applications.commands`

4. Lancer le bot :

```bash
npm start
```

## Variables d'environnement

- `DISCORD_TOKEN` : token du bot
- `DISCORD_CLIENT_ID` : ID de l'application
- `DISCORD_GUILD_ID` : (optionnel) ID de serveur pour enregistrer les commandes plus vite en développement

## Notes

- Les données joueurs sont sauvegardées automatiquement dans `data/players.json`.
- Si `DISCORD_GUILD_ID` est renseigné, les commandes slash sont enregistrées sur ce serveur ; sinon elles sont globales (propagation plus lente).
