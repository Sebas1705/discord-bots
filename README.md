# discord-bots

Bot de Discord personal (Python + [py-cord](https://docs.pycord.dev/)) con moderación, comandos de utilidad, bienvenida/roles y música.

## Requisitos

- Python 3.11+
- [ffmpeg](https://ffmpeg.org/) instalado y en el `PATH` (necesario para el cog de música)
- Una aplicación + bot creados en el [Discord Developer Portal](https://discord.com/developers/applications), con los intents **Message Content** y **Server Members** activados

## Setup

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows (Git Bash: source .venv/Scripts/activate)
pip install -r requirements.txt
cp .env.example .env       # completar DISCORD_TOKEN
python -m src.bot.main
```

## Invitar al bot

Generá el link de invitación en el Developer Portal con los scopes `bot` + `applications.commands` y, como mínimo, estos permisos: Send Messages, Manage Messages, Kick Members, Ban Members, Manage Roles, Connect, Speak.

## Estructura

```
src/bot/
  main.py         # entrypoint, carga los cogs
  config.py       # settings desde variables de entorno
  cogs/
    moderation.py # kick, ban, purge
    welcome.py    # mensaje de bienvenida + auto-rol
    music.py      # play/skip/stop en canal de voz (yt-dlp + ffmpeg)
    utility.py    # ping, info, comandos custom
```

## Tests

```bash
pytest
```
