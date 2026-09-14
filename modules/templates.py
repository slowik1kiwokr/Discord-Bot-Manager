# --- SABLONOK a bot integrációhoz ---

VERSION_FILE_TEMPLATE = '''BOT_NAME = "Main Bot"
BOT_VERSION = "1.0.0"
BOT_TOKEN = "ide_ird_a_bot_tokened"
BOT_PREFIX = "/"
'''

BOT_PY_TEMPLATE = '''# --- bot.py — a bot fő fájlja ---
import discord
from discord.ext import commands

from version import BOT_NAME, BOT_VERSION, BOT_TOKEN, BOT_PREFIX
from panel_integrity import BOT_INFO


def get_prefix(bot, message):
    return BOT_PREFIX


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents)


@bot.event
async def on_ready():
    print(f"{BOT_NAME} v{BOT_VERSION} bejelentkezve: {bot.user}")
    try:
        await bot.load_extension("panel_integrity")
        await bot.tree.sync()
        print("[PANEL] Integracio sikeresen betoltve.")
    except Exception as e:
        print(f"[PANEL] Hiba a betolteskor: {e}")


@bot.command(name="teszt", aliases=["test"])
async def teszt(ctx):
    embed = discord.Embed(
        title=BOT_NAME,
        description=f"A bot mukodik! Verzio: {BOT_VERSION}",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(name="parancsok", aliases=["menu"])
async def parancsok(ctx):
    embed = discord.Embed(title="Elérhető parancsok", color=discord.Color.blue())
    embed.add_field(name="teszt", value="Bot tesztelese", inline=False)
    embed.add_field(name="parancsok", value="Ez a menu", inline=False)
    embed.set_footer(text=f"{BOT_NAME} v{BOT_VERSION}")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
'''

PANEL_INTEGRITY_CODE = r'''# --- panel_integrity.py — Panel integracio ---
# Ez a fajl tartalmazza a panel OSSZES funkciojat a bot oldalan.
# Helyezd a bot.py melle, es toltsd be extensionkent:
#     await bot.load_extension("panel_integrity")

# --- UTF-8 kimenet (Windows konzol fix) ---
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import asyncio
import datetime
import json
import os
import uuid

import discord
from discord import app_commands
from discord.ext import commands, tasks

# --- Verzio es info ---
try:
    from version import BOT_NAME, BOT_VERSION
except ImportError:
    BOT_NAME, BOT_VERSION = "Main Bot", "1.0.0"

BOT_INFO = {
    "name": BOT_NAME,
    "version": BOT_VERSION,
}

BOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BOT_DIR, "bot_config.json")
STATS_PATH = os.path.join(BOT_DIR, "bot_stats.json")
CHANNELS_PATH = os.path.join(BOT_DIR, "bot_channels.json")


def _hex_to_color(value):
    """Hex szinkod -> discord.Color."""
    try:
        return discord.Color(int(value.lstrip("#"), 16))
    except (ValueError, AttributeError):
        return discord.Color.blurple()


class PanelIntegrity(commands.Cog):
    """Panel integracio — kapcsolodas, statisztika, tavoli vezerles."""

    def __init__(self, bot):
        self.bot = bot
        self.connected_panel_id = None
        self.connected_source = "Discord"
        self.stats_loop.start()

    def cog_unload(self):
        self.stats_loop.cancel()

    # ==============================================================
    #  Konfiguracio
    # ==============================================================
    def load_config(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return {"panel_id": "#00001", "test_mode": False}

    def panel_directory(self):
        configured = self.load_config().get("panel_dir", "")
        if configured and os.path.isdir(configured):
            return configured
        return BOT_DIR

    # ==============================================================
    #  Panel kommunikacio
    # ==============================================================
    async def request_panel(self, action, user, bot_name="Main Bot", data=None):
        config = self.load_config()
        expected = config.get("panel_id", "#00001")
        if self.connected_panel_id != expected:
            return "Elobb hasznald a /connect parancsot."

        panel_dir = self.panel_directory()
        command_path = os.path.join(panel_dir, "panel_commands.json")
        response_dir = os.path.join(panel_dir, "panel_responses")
        os.makedirs(response_dir, exist_ok=True)

        req_id = uuid.uuid4().hex
        request = {
            "id": req_id,
            "action": action,
            "user": user,
            "source": self.connected_source,
            "bot": bot_name,
            "data": data or {},
            "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }

        try:
            pending = []
            if os.path.exists(command_path):
                with open(command_path, "r", encoding="utf-8") as f:
                    pending = json.load(f)
            pending.append(request)
            tmp = command_path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(pending, f, ensure_ascii=False)
            os.replace(tmp, command_path)
        except (OSError, json.JSONDecodeError) as e:
            return f"A panel nem erheto el: {e}"

        response_path = os.path.join(response_dir, req_id + ".json")
        for _ in range(20):
            await asyncio.sleep(0.5)
            if os.path.exists(response_path):
                try:
                    with open(response_path, "r", encoding="utf-8") as f:
                        resp = json.load(f)
                    os.remove(response_path)
                    if action == "broadcast" and resp.get("action") == "broadcast":
                        return await self.broadcast_to_guilds(resp.get("data", {}))
                    return resp.get("message", "Nincs valasz.")
                except (OSError, json.JSONDecodeError):
                    return "A panel valasza nem olvashato."
        return "A panel 10 masodpercen belul nem valaszolt."

    async def broadcast_to_guilds(self, data):
        """Broadcast kuldese — tamogatja az uzenetet, embedet es idozitest."""
        ch_map = {str(k): str(v) for k, v in data.get("channels", {}).items()}
        payload = data.get("payload", {})
        msg_type = payload.get("type", "message")
        delay = int(data.get("delay_seconds", 0) or 0)

        if delay > 0:
            print(f"[BROADCAST] Utemezve {delay} masodperc mulva...")
            await asyncio.sleep(delay)

        sent, failed = 0, 0
        for guild in self.bot.guilds:
            ch_id = ch_map.get(str(guild.id))
            channel = self.bot.get_channel(int(ch_id)) if ch_id and ch_id.isdigit() else None
            if channel is None:
                channel = next(
                    (c for c in guild.text_channels
                     if c.permissions_for(guild.me).send_messages),
                    None,
                )
            if channel is None:
                failed += 1
                continue
            try:
                if msg_type == "embed":
                    emb = payload.get("embed", {})
                    embed = discord.Embed(
                        title=emb.get("title") or None,
                        description=emb.get("description") or None,
                        color=_hex_to_color(emb.get("color", "#5865F2")),
                    )
                    if emb.get("footer"):
                        embed.set_footer(text=emb["footer"])
                    if emb.get("thumbnail"):
                        embed.set_thumbnail(url=emb["thumbnail"])
                    for field in emb.get("fields", []):
                        embed.add_field(
                            name=field.get("name", "\u200b"),
                            value=field.get("value", "\u200b"),
                            inline=field.get("inline", False),
                        )
                    await channel.send(embed=embed)
                else:
                    content = payload.get("content") or data.get("message", "")
                    if not content:
                        content = "\u200b"
                    await channel.send(content)
                sent += 1
            except (discord.Forbidden, discord.HTTPException) as e:
                print(f"[BROADCAST] Hiba {channel.name}: {e}")
                failed += 1
        return f"Broadcast elkuldve. Sikeres: {sent}, sikertelen: {failed}."

    # ==============================================================
    #  Statisztika + csatornak loop
    # ==============================================================
    @tasks.loop(seconds=2)
    async def stats_loop(self):
        await self.process_panel_broadcasts()
        config = self.load_config()

        # Activity loop
        activities = config.get("activity_loop", [])
        if not activities and config.get("activity_text", ""):
            activities = [{
                "type": config.get("activity_type", "Playing"),
                "text": config.get("activity_text", ""),
            }]
        if config.get("activity_enabled", True) and activities:
            interval = max(60, int(config.get("activity_interval_minutes", 5)) * 60)
            idx = int(datetime.datetime.now().timestamp() // interval) % len(activities)
            act = activities[idx]
            act_text = act.get("text", "")
            act_type = act.get("type", "Playing")
            act_class = {
                "Listening": discord.ActivityType.listening,
                "Watching": discord.ActivityType.watching,
                "Streaming": discord.ActivityType.streaming,
            }.get(act_type, discord.ActivityType.playing)
            if act_text:
                await self.bot.change_presence(
                    activity=discord.Activity(type=act_class, name=act_text)
                )

        # Statisztika mentes
        stats = {
            "panel_id": config.get("panel_id", "#00001"),
            "guilds": len(self.bot.guilds),
            "users": sum(g.member_count or 0 for g in self.bot.guilds),
            "api_ping": round(self.bot.latency * 1000),
            "test_mode_active": config.get("test_mode", False),
            "name": BOT_NAME,
            "version": BOT_VERSION,
            "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        }
        try:
            with open(STATS_PATH, "w", encoding="utf-8") as f:
                json.dump(stats, f, ensure_ascii=False, indent=4)

            servers_dir = os.path.join(BOT_DIR, "data", "servers")
            os.makedirs(servers_dir, exist_ok=True)

            channels_data = []

            for guild in self.bot.guilds:
                bot_member = guild.me

                channels = []
                for ch in guild.text_channels:
                    try:
                        perms = ch.permissions_for(bot_member)
                        channels.append({
                            "id": ch.id,
                            "name": ch.name,
                            "category": ch.category.name if ch.category else "",
                            "position": ch.position,
                            "can_send": bool(perms.send_messages),
                            "can_embed": bool(perms.embed_links),
                            "can_attach": bool(perms.attach_files),
                            "is_nsfw": ch.is_nsfw() if hasattr(ch, "is_nsfw") else False,
                        })
                    except Exception:
                        pass

                server_path = os.path.join(servers_dir, f"{guild.id}.json")
                with open(server_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "guild_id": guild.id,
                        "name": guild.name,
                        "member_count": guild.member_count,
                        "owner": str(guild.owner),
                        "description": guild.description,
                        "created_at": guild.created_at.isoformat(),
                        "icon_url": str(guild.icon.url) if guild.icon else "",
                        "bot_name": BOT_NAME,
                        "version": BOT_VERSION,
                        "channels": channels,
                        "updated_at": datetime.datetime.now().isoformat(timespec="seconds"),
                    }, f, ensure_ascii=False, indent=4)

                channels_data.append({
                    "guild_id": guild.id,
                    "guild_name": guild.name,
                    "channels": channels,
                })

            with open(CHANNELS_PATH, "w", encoding="utf-8") as f:
                json.dump(channels_data, f, ensure_ascii=False, indent=4)

        except OSError as e:
            print(f"[PANEL] Stats mentesi hiba: {e}")

    async def process_panel_broadcasts(self):
        path = os.path.join(self.panel_directory(), "panel_broadcast_requests.json")
        if not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                requests = json.load(f)
            remaining = []
            for req in requests:
                if req.get("bot", BOT_NAME) != BOT_NAME:
                    remaining.append(req)
                    continue
                result = await self.broadcast_to_guilds(req)
                self.connected_source = "Panel"
                print(f"[BROADCAST] {result}")
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(remaining, f, ensure_ascii=False)
            os.replace(tmp, path)
        except (OSError, json.JSONDecodeError):
            return

    @stats_loop.before_loop
    async def before_stats(self):
        await self.bot.wait_until_ready()

    # ==============================================================
    #  Slash parancsok
    # ==============================================================
    @app_commands.command(name="connect", description="Kapcsolodas a panelhez")
    @app_commands.describe(panel_id="A panel azonositoja, pl. #ABC123",
                            device="Telefon vagy PC")
    @app_commands.choices(device=[
        app_commands.Choice(name="Telefon", value="Telefon"),
        app_commands.Choice(name="PC", value="PC"),
    ])
    async def connect(self, interaction: discord.Interaction, panel_id: str,
                       device: app_commands.Choice[str] = None):
        expected = self.load_config().get("panel_id", "#00001")
        if panel_id.strip() != expected:
            await interaction.response.send_message("Hibas panel azonosito.", ephemeral=True)
            return
        self.connected_panel_id = panel_id.strip()
        self.connected_source = device.value if device else "Discord"
        await interaction.response.send_message("Kapcsolodva a panelhez.", ephemeral=True)

    async def _remote(self, interaction, action, bot_name="Main Bot"):
        config = self.load_config()
        allowed = {str(v) for v in config.get("allowed_discord_ids", [])}
        if config.get("test_mode", False) and str(interaction.user.id) not in allowed:
            await interaction.response.send_message(
                "A bot teszt modban van. Csak a tesztelok hasznalhatjak.",
                ephemeral=True,
            )
            return
        if not self.connected_panel_id:
            await interaction.response.send_message(
                "Elobb hasznald a /connect parancsot.", ephemeral=True
            )
            return
        await interaction.response.defer()
        result = await self.request_panel(action, str(interaction.user), bot_name)
        await interaction.followup.send(result[:1900])

    @app_commands.command(name="vezerles", description="Panel bot vezerlese")
    @app_commands.choices(muvelet=[
        app_commands.Choice(name="Inditas", value="start"),
        app_commands.Choice(name="Leallitas", value="stop"),
        app_commands.Choice(name="Ujrainditas", value="restart"),
        app_commands.Choice(name="Allapot", value="status"),
        app_commands.Choice(name="Naplo", value="log"),
    ])
    async def vezerles(self, interaction: discord.Interaction,
                        muvelet: app_commands.Choice[str], bot_neve: str = "Main Bot"):
        await self._remote(interaction, muvelet.value, bot_neve)

    @app_commands.command(name="info", description="Panel informacio")
    async def info(self, interaction: discord.Interaction):
        await self._remote(interaction, "info")

    @app_commands.command(name="status", description="Panel allapot")
    async def status(self, interaction: discord.Interaction):
        await self._remote(interaction, "status")

    @app_commands.command(name="stressz", description="Eroforras ellenorzes")
    async def stressz(self, interaction: discord.Interaction):
        await self._remote(interaction, "stressz")

    @app_commands.command(name="log", description="Panel naplo")
    async def log(self, interaction: discord.Interaction):
        await self._remote(interaction, "log")

    @app_commands.command(name="start", description="Bot inditasa")
    async def start(self, interaction: discord.Interaction):
        await self._remote(interaction, "start")

    @app_commands.command(name="stop", description="Bot leallitasa")
    async def stop(self, interaction: discord.Interaction):
        await self._remote(interaction, "stop")

    @app_commands.command(name="restart", description="Bot ujrainditasa")
    async def restart(self, interaction: discord.Interaction):
        await self._remote(interaction, "restart")

    @app_commands.command(name="kilepes", description="A bot kilep egy szerverrol")
    @app_commands.describe(guild_id="A Discord szerver azonositoja")
    async def kilepes(self, interaction: discord.Interaction, guild_id: str):
        if not self.connected_panel_id:
            await interaction.response.send_message(
                "Elobb hasznald a /connect parancsot.", ephemeral=True
            )
            return
        try:
            guild = self.bot.get_guild(int(guild_id))
        except ValueError:
            guild = None
        if guild is None:
            await interaction.response.send_message(
                "Nem talalhato ilyen szerver.", ephemeral=True
            )
            return
        await guild.leave()
        await interaction.response.send_message(f"A bot kilepett innen: {guild.name}")

    @app_commands.command(name="broadcast", description="Uzenet az osszes szerverre")
    @app_commands.describe(message="A globalis uzenet")
    async def broadcast(self, interaction: discord.Interaction, message: str):
        config = self.load_config()
        allowed = {str(v) for v in config.get("allowed_discord_ids", [])}
        if config.get("test_mode", False) and str(interaction.user.id) not in allowed:
            await interaction.response.send_message(
                "Csak a tesztelok hasznalhatjak.", ephemeral=True
            )
            return
        if not self.connected_panel_id:
            await interaction.response.send_message(
                "Elobb hasznald a /connect parancsot.", ephemeral=True
            )
            return
        await interaction.response.defer(ephemeral=True)
        result = await self.request_panel(
            "broadcast", str(interaction.user), BOT_NAME, {"message": message}
        )
        await interaction.followup.send(result[:1900], ephemeral=True)

    # ==============================================================
    #  Commander parancsok betoltese
    # ==============================================================
    def _load_commander_commands(self):
        path = os.path.join(BOT_DIR, "commander_commands.json")
        if not os.path.exists(path):
            print("[PANEL] Nincs commander_commands.json - nincs egyedi parancs.")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                commands_list = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[PANEL] Commander fajl hiba: {e}")
            return

        print(f"[PANEL] Commander parancsok betoltese ({len(commands_list)} db)...")

        for entry in commands_list:
            if not entry.get("enabled", True):
                continue

            name = entry.get("name", "").strip().lower()
            if not name or not name.replace("_", "").isalnum():
                continue

            description = entry.get("description", "Egyedi parancs")

            def make_callback(cmd_entry, cmd_name):
                async def callback(interaction: discord.Interaction):
                    try:
                        if cmd_entry.get("type") == "embed":
                            emb = cmd_entry.get("embed", {})
                            embed = discord.Embed(
                                title=emb.get("title") or None,
                                description=emb.get("description") or None,
                                color=_hex_to_color(emb.get("color", "#5865F2")),
                            )
                            if emb.get("footer"):
                                embed.set_footer(text=emb["footer"])
                            if emb.get("thumbnail"):
                                embed.set_thumbnail(url=emb["thumbnail"])
                            for field in emb.get("fields", []):
                                embed.add_field(
                                    name=field.get("name", "\u200b"),
                                    value=field.get("value", "\u200b"),
                                    inline=field.get("inline", False),
                                )
                            await interaction.response.send_message(
                                embed=embed,
                                ephemeral=cmd_entry.get("ephemeral", False),
                            )
                        else:
                            content = cmd_entry.get("content", "") or "\u200b"
                            await interaction.response.send_message(
                                content,
                                ephemeral=cmd_entry.get("ephemeral", False),
                            )
                    except Exception as e:
                        print(f"[PANEL] Commander /{cmd_name} hiba: {e}")
                return callback

            try:
                cmd = app_commands.Command(
                    name=name,
                    description=description,
                    callback=make_callback(entry, name),
                )
                self.bot.tree.add_command(cmd)
                print(f"[PANEL] OK Commander parancs betoltve: /{name}")
            except Exception as e:
                print(f"[PANEL] HIBA Commander parancs (/{name}): {e}")


async def _load_auto_extensions(bot):
    """Automatikusan betolti a bot_extensions.txt-ben listazott extension-oket."""
    ext_file = os.path.join(BOT_DIR, "bot_extensions.txt")
    if not os.path.exists(ext_file):
        return
    print("[PANEL] Auto-extension-ok betoltese...")
    try:
        with open(ext_file, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if not name or name.startswith("#"):
                    continue
                try:
                    await bot.load_extension(name)
                    print(f"[PANEL] OK Extension betoltve: {name}")
                except Exception as e:
                    print(f"[PANEL] HIBA Extension ({name}): {e}")
    except Exception as e:
        print(f"[PANEL] Auto-extension hiba: {e}")


async def setup(bot):
    cog = PanelIntegrity(bot)
    cog._load_commander_commands()
    await bot.add_cog(cog)
    await _load_auto_extensions(bot)
'''