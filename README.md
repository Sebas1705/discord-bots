# Overlord

Bot de Discord "god bot" para un único servidor personal: py-cord, todas las capacidades activadas (moderación, bienvenida/roles, música, comandos custom, administración) sobre una base común de logging, manejo de errores y configuración persistente por servidor.

## Requisitos

- Python 3.11+
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

## Despliegue

Dos caminos, según cuánta fricción de cuenta/tarjeta estés dispuesto a aceptar a cambio de confiabilidad.

### Opción A — Oracle Cloud Free Tier (recomendada: $0/mes de por vida, VPS real)

El bot corre en un contenedor Docker con reinicio automático, así que el mantenimiento se reduce a `git pull` + rebuild cuando cambia algo.

### 1. Levantar el servidor (una sola vez)

1. Creá una cuenta en [Oracle Cloud](https://www.oracle.com/cloud/free/) (pide tarjeta para verificar identidad, pero el shape "Always Free" nunca cobra).
2. Creá una instancia **Always Free**: shape `VM.Standard.A1.Flex` (ARM, hasta 4 OCPU/24GB) si hay disponibilidad en tu región, o `VM.Standard.E2.1.Micro` (x86, 1 OCPU/1GB) como respaldo — cualquiera de las dos alcanza de sobra para este bot. Imagen: Ubuntu 22.04+.
3. Abrí el puerto de salida (el bot solo hace conexiones salientes hacia Discord, no necesitás abrir puertos entrantes).
4. Conectate por SSH e instalá Docker:

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER   # cerrá sesión y volvé a entrar para que aplique
```

### 2. Desplegar el bot

```bash
git clone https://github.com/Sebas1705/discord-bots.git
cd discord-bots
cp .env.example .env
nano .env                       # completar DISCORD_TOKEN
docker compose up -d --build
```

### 3. Mantenimiento

```bash
docker compose logs -f          # ver logs en vivo
docker compose restart          # reiniciar sin perder configuración (data/ persiste)
git pull && docker compose up -d --build   # actualizar a la última versión
```

`restart: unless-stopped` en `docker-compose.yml` hace que el bot vuelva solo si se cae el proceso o se reinicia la VM — no hace falta un cron ni supervisor aparte. Los tests corren automáticamente en cada push (`.github/workflows/test.yml`, gratis en GitHub Actions), así que un `git pull` en el servidor solo trae código que ya pasó CI.

### Opción B — Replit + UptimeRobot ($0, sin tarjeta ni cuenta de nube)

**Trade-offs, en serio, antes de elegir esto:** Replit puede dormir el repl igual pese al ping (lo restringen cada tanto en el free tier), los recursos son bajos (podés notarlo con `music` bajo carga), y no es un uso oficialmente pensado para procesos 24/7 — es la comunidad de bots hobby la que lo adoptó así. Si en algún momento te cansás de que se caiga, la migración a Docker/Oracle (arriba) es directa porque es el mismo código.

1. Entrá a [replit.com](https://replit.com), creá cuenta (solo email, sin tarjeta) e importá este repo (`Create Repl` → `Import from GitHub` → `Sebas1705/discord-bots`). Replit detecta `.replit` y `replit.nix` automáticamente (instala Python y `ffmpeg`).
2. En la pestaña **Secrets** (no uses `.env` acá) agregá `DISCORD_TOKEN` y opcionalmente `BOT_PREFIX`.
3. Apretá **Run**. La primera vez instala dependencias (`pip install -e .`) y levanta el bot junto con un mini servidor HTTP (`keep_alive.py`) en el puerto que Replit expone públicamente — así es como un pinger externo lo mantiene despierto.
4. Copiá la URL que te da el panel de Replit (algo como `https://discord-bots.tuusuario.repl.co`).
5. Creá una cuenta gratis en [UptimeRobot](https://uptimerobot.com) (sin tarjeta) y agregá un monitor **HTTP(s)** apuntando a esa URL, con intervalo de 5 minutos. Eso evita que Replit duerma el repl por inactividad.

`keep_alive.py` solo se activa cuando detecta la variable `REPL_ID` (que Replit define solo) — en Docker/Oracle no hace nada, así que el mismo repo sirve para ambos caminos sin tocar código.
