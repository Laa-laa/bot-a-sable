# Sablette Bot

Bot Discord simple permettant de jouer, obtenir des informations rapides et utiliser des commandes utiles directement dans un serveur Discord.

## L'équipe
- Lélia KOZAN — Product Owner
- Clément DARRIBEAU — Scrum Master
- Baptiste MANCEL— Developer
- Nicolas DAUNAC — Developer

## La vision produit
En tant que membre d’un serveur Discord, ce projet permet de jouer et récupérer rapidement des informations utiles directement dans Discord, sans quitter la conversation.

## Product Backlog

| ID | User Story | MoSCoW | Statut |
|---|---|---|---|
| US-01 | En tant que membre du serveur, je veux vérifier que le bot est en ligne afin de savoir qu’il fonctionne. | Must | ✅ livré |
| US-02 | En tant que membre du serveur, je veux lancer un dé à 6 faces afin de jouer rapidement avec mes amis. | Must | ✅ livré |
| US-03 | En tant que membre du serveur, je veux jouer au wordle du jour. | Must | ✅ livré |
| US-04 | En tant que membre du serveur, je veux obtenir une information rapide depuis Internet afin d’éviter de quitter Discord. | Must | ⏳ en cours |
| US-05 | En tant qu’utilisateur, je veux voir un message d’erreur propre si la commande échoue afin de comprendre ce qu’il se passe. | Should | ⏳ en cours |
| US-06 | En tant qu’administrateur du projet, je veux une documentation d’installation afin que le projet soit relançable facilement. | Should | ⏳ en cours |
| US-07 | En tant que membre du serveur, je veux une commande `/help` afin de connaître les commandes disponibles. | Must | ⏳ en cours |
| US-08 | En tant qu’équipe projet, je veux conserver les statistiques des joueurs afin de rendre le jeu plus riche.En tant que membre du serveur, je veux suivre les statistiques des joueurs. | Could | ⏳ en cours |

## Ce qui doit être livré (MVP)
- Commande `/ping`
- Commande `/roll`
- Commande `/fact`
- Documentation d’installation
- Bot lançable localement

## Lancer le projet en local


## Ce qui a été reporté et pourquoi
- US-07 `/help` : reportée par manque de temps
- US-08 commande fun supplémentaire : hors scope du MVP
- Persistance des scores : trop complexe pour le temps imparti

## Nos décisions techniques
- Stack choisie : Node.js + discord.js
- Nous avons choisi un stockage simple sans base de données afin de livrer un MVP rapidement
- Nous avons priorisé les slash commands simples pour faciliter la démo

## Comment on a utilisé l’IA
- L’IA a été utilisée pour générer la structure du bot, les commandes et corriger les erreurs
- Les prompts les plus efficaces étaient ceux qui précisaient la stack, le fichier concerné et l’User Story exacte
- L’IA a parfois proposé une architecture trop complexe, que nous avons simplifiée pour rester dans le temps imparti

## Rétrospective rapide
### Ce qui a bien marché
- Bonne répartition des tâches entre backlog, code et revue
- L’IA a permis d’aller vite sur les commandes simples

### Ce qu’on ferait différemment
- Écrire les prompts encore plus précisément dès le début
- Réduire le scope plus tôt

### Ce qu’on garderait
- Le découpage en petites User Stories
- Les branches par fonctionnalité
- La validation rapide par le Product Owner
