# Overlord

Bot de Discord "god bot" para un único servidor personal: py-cord, todas las capacidades activadas (moderación, bienvenida/roles, música, comandos custom, administración) sobre una base común de logging, manejo de errores y configuración persistente por servidor.

## Requisitos

- Python 3.13+
- [ffmpeg](https://ffmpeg.org/) instalado y en el `PATH` (para el cog de música)
- Una aplicación + bot en el [Discord Developer Portal](https://discord.com/developers/applications), con los intents **Message Content** y **Server Members** activados

## Setup

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows (Git Bash: source .venv/Scripts/activate)
pip install -e .[dev]
cp .env.example .env       # completar DISCORD_TOKEN
overlord
pytest
```

## Invitar al bot

Generá el link de invitación en el Developer Portal con los scopes `bot` + `applications.commands` y estos permisos: Send Messages, Manage Messages, Kick Members, Ban Members, Manage Roles, Connect, Speak.

## Arquitectura

Todo lo que hay bajo `src/overlord/cogs/` se descubre y carga automáticamente al arrancar (`main.py`) — un cog nuevo no necesita ningún cableado adicional.

- `config.py` — lo mínimo que debe venir del entorno (token, prefix)
- `storage.py` — store JSON por servidor (`data/guild_settings.json`, gitignored); el mecanismo que usa el resto de los cogs para recordar configuración
- `logging_setup.py` — logging de consola
- `errors.py` — manejador global de errores de slash commands

## Cogs (todo activo — servidor único, pocos miembros, sin necesidad de feature-flags)

- `settings` — `/settings welcome_channel|auto_role|mod_log|show`
- `admin` — solo para el owner: `/sync`, `/reload`, `/shutdown`
- `moderation` — `/kick`, `/ban`, `/purge`, logueado opcionalmente en un canal de mod-log
- `welcome` — mensaje de bienvenida + auto-rol, configurado vía `/settings`
- `custom_commands` — `/addcommand`, `/removecommand`, `/say`: comandos de texto definidos en runtime
- `music` — reproducción en canal de voz vía yt-dlp (requiere `ffmpeg`)
- `utility` — `/ping`, `/uptime`

## Tests

```bash
pytest
```
