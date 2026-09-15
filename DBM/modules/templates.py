"""
Bot fájl sablonok — nyelvfüggő.
A panel a jelenlegi nyelvnek megfelelő sablont adja vissza.
"""

from modules.languages import LANGUAGES


# =====================================================================
#  VERSION.PY — nyelvfüggetlen (csak változók)
# =====================================================================
VERSION_FILE_TEMPLATE = '''BOT_NAME = "Main Bot"
BOT_VERSION = "1.0.0"
BOT_TOKEN = "ide_ird_a_bot_tokened"
BOT_PREFIX = "/"
'''

VERSION_FILE_TEMPLATE_EN = '''BOT_NAME = "Main Bot"
BOT_VERSION = "1.0.0"
BOT_TOKEN = "put_your_bot_token_here"
BOT_PREFIX = "/"
'''


# =====================================================================
#  BOT.PY SABLON
# =====================================================================
BOT_PY_TEMPLATE_HU = '''# --- bot.py — a bot fő fájlja ---
import discord
from discord.ext import commands

from version import BOT_NAME, BOT_VERSION, BOT_TOKEN, BOT_PREFIX
from panel_integrity import BOT_INFO


def get_prefix(bot, message):
    """A bot parancs-prefixét adja vissza."""
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
        print("[PANEL] Integráció sikeresen betöltve.")
    except Exception as e:
        print(f"[PANEL] Hiba a betöltéskor: {e}")


@bot.command(name="teszt", aliases=["test"])
async def teszt(ctx):
    """Egyszerű teszt parancs."""
    embed = discord.Embed(
        title=BOT_NAME,
        description=f"✅ A bot működik! Verzió: {BOT_VERSION}",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(name="parancsok", aliases=["menu"])
async def parancsok(ctx):
    """Elérhető parancsok listája."""
    embed = discord.Embed(title="🤖 Elérhető parancsok", color=discord.Color.blue())
    embed.add_field(name="teszt", value="Bot tesztelése", inline=False)
    embed.add_field(name="parancsok", value="Ez a menü", inline=False)
    embed.set_footer(text=f"{BOT_NAME} v{BOT_VERSION}")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
'''

BOT_PY_TEMPLATE_EN = '''# --- bot.py — the bot's main file ---
import discord
from discord.ext import commands

from version import BOT_NAME, BOT_VERSION, BOT_TOKEN, BOT_PREFIX
from panel_integrity import BOT_INFO


def get_prefix(bot, message):
    """Returns the bot's command prefix."""
    return BOT_PREFIX


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=get_prefix, intents=intents)


@bot.event
async def on_ready():
    print(f"{BOT_NAME} v{BOT_VERSION} logged in: {bot.user}")
    try:
        await bot.load_extension("panel_integrity")
        await bot.tree.sync()
        print("[PANEL] Integration loaded successfully.")
    except Exception as e:
        print(f"[PANEL] Loading error: {e}")


@bot.command(name="test")
async def test(ctx):
    """Simple test command."""
    embed = discord.Embed(
        title=BOT_NAME,
        description=f"✅ The bot works! Version: {BOT_VERSION}",
        color=discord.Color.green(),
    )
    await ctx.send(embed=embed)


@bot.command(name="commands", aliases=["menu"])
async def commands_cmd(ctx):
    """List of available commands."""
    embed = discord.Embed(title="🤖 Available commands", color=discord.Color.blue())
    embed.add_field(name="test", value="Test the bot", inline=False)
    embed.add_field(name="commands", value="This menu", inline=False)
    embed.set_footer(text=f"{BOT_NAME} v{BOT_VERSION}")
    await ctx.send(embed=embed)


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
'''


# =====================================================================
#  PANEL_INTEGRITY.PY — nyelvfüggetlen (a bot kódja nem nyelvfüggő)
# =====================================================================
PANEL_INTEGRITY_CODE = r'''# --- panel_integrity.py — Panel integration ---
# All panel-side functions for the bot.

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
    try:
        return discord.Color(int(value.lstrip("#"), 16))
    except (ValueError, AttributeError):
        return discord.Color.blurple()


class PanelIntegrity(commands.Cog):
    """Panel integration — connection, stats, remote control."""

    def __init__(self, bot):
        self.bot = bot
        self.connected_panel_id = None
        self.connected_source = "Discord"
        self.stats_loop.start()

    def cog_unload(self):
        self.stats_loop.cancel()

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

    async def request_panel(self, action, user, bot_name="Main Bot", data=None):
        config = self.load_config()
        expected = config.get("panel_id", "#00001")
        if self.connected_panel_id != expected:
            return "Use /connect first."

        panel_dir = self.panel_directory()
        command_path = os.path.join(panel_dir, "panel_commands.json")
        response_dir = os.path.join(panel_dir, "panel_responses")
        os.makedirs(response_dir, exist_ok=True)

        req_id = uuid.uuid4().hex
        request = {
            "id": req_id, "action": action, "user": user,
            "source": self.connected_source, "bot": bot_name,
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
            return f"Panel unavailable: {e}"

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
                    return resp.get("message", "No response.")
                except (OSError, json.JSONDecodeError):
                    return "Panel response unreadable."
        return "Panel did not respond within 10 seconds."

    async def broadcast_to_guilds(self, data):
        ch_map = {str(k): str(v) for k, v in data.get("channels", {}).items()}
        payload = data.get("payload", {})
        msg_type = payload.get("type", "message")
        delay = int(data.get("delay_seconds", 0) or 0)
        if delay > 0:
            await asyncio.sleep(delay)
        sent, failed = 0, 0
        for guild in self.bot.guilds:
            ch_id = ch_map.get(str(guild.id))
            channel = self.bot.get_channel(int(ch_id)) if ch_id and ch_id.isdigit() else None
            if channel is None:
                channel = next((c for c in guild.text_channels
                                 if c.permissions_for(guild.me).send_messages), None)
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
                    await channel.send(embed=embed)
                else:
                    content = payload.get("content") or data.get("message", "")
                    await channel.send(content or "\u200b")
                sent += 1
            except (discord.Forbidden, discord.HTTPException):
                failed += 1
        return f"Broadcast sent. Success: {sent}, failed: {failed}."

    @tasks.loop(seconds=2)
    async def stats_loop(self):
        await self.process_panel_broadcasts()
        config = self.load_config()
        activities = config.get("activity_loop", [])
        if not activities and config.get("activity_text", ""):
            activities = [{"type": config.get("activity_type", "Playing"),
                           "text": config.get("activity_text", "")}]
        if config.get("activity_enabled", True) and activities:
            interval = max(60, int(config.get("activity_interval_minutes", 5)) * 60)
            idx = int(datetime.datetime.now().timestamp() // interval) % len(activities)
            act = activities[idx]
            act_text = act.get("text", "")
            if act_text:
                act_class = {
                    "Listening": discord.ActivityType.listening,
                    "Watching": discord.ActivityType.watching,
                    "Streaming": discord.ActivityType.streaming,
                }.get(act.get("type", "Playing"), discord.ActivityType.playing)
                await self.bot.change_presence(
                    activity=discord.Activity(type=act_class, name=act_text))
        stats = {
            "panel_id": config.get("panel_id", "#00001"),
            "guilds": len(self.bot.guilds),
            "users": sum(g.member_count or 0 for g in self.bot.guilds),
            "api_ping": round(self.bot.latency * 1000),
            "test_mode_active": config.get("test_mode", False),
            "name": BOT_NAME, "version": BOT_VERSION,
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
                            "id": ch.id, "name": ch.name,
                            "category": ch.category.name if ch.category else "",
                            "position": ch.position,
                            "can_send": bool(perms.send_messages),
                            "can_embed": bool(perms.embed_links),
                            "can_attach": bool(perms.attach_files),
                            "is_nsfw": ch.is_nsfw() if hasattr(ch, "is_nsfw") else False,
                        })
                    except Exception:
                        pass
                with open(os.path.join(servers_dir, f"{guild.id}.json"),
                          "w", encoding="utf-8") as f:
                    json.dump({
                        "guild_id": guild.id, "name": guild.name,
                        "member_count": guild.member_count,
                        "owner": str(guild.owner),
                        "description": guild.description,
                        "created_at": guild.created_at.isoformat(),
                        "icon_url": str(guild.icon.url) if guild.icon else "",
                        "bot_name": BOT_NAME, "version": BOT_VERSION,
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
            print(f"[PANEL] Stats save error: {e}")

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

    @app_commands.command(name="connect", description="Connect to the panel")
    @app_commands.describe(panel_id="Panel ID (e.g. #ABC123)",
                            device="Phone or PC")
    @app_commands.choices(device=[
        app_commands.Choice(name="Phone", value="Phone"),
        app_commands.Choice(name="PC", value="PC"),
    ])
    async def connect(self, interaction: discord.Interaction, panel_id: str,
                       device: app_commands.Choice[str] = None):
        expected = self.load_config().get("panel_id", "#00001")
        if panel_id.strip() != expected:
            await interaction.response.send_message("❌ Invalid panel ID.", ephemeral=True)
            return
        self.connected_panel_id = panel_id.strip()
        self.connected_source = device.value if device else "Discord"
        await interaction.response.send_message("✅ Connected to panel.", ephemeral=True)

    async def _remote(self, interaction, action, bot_name="Main Bot"):
        config = self.load_config()
        allowed = {str(v) for v in config.get("allowed_discord_ids", [])}
        if config.get("test_mode", False) and str(interaction.user.id) not in allowed:
            await interaction.response.send_message(
                "🧪 Bot is in test mode. Only testers can use it.", ephemeral=True)
            return
        if not self.connected_panel_id:
            await interaction.response.send_message("Use /connect first.", ephemeral=True)
            return
        await interaction.response.defer()
        result = await self.request_panel(action, str(interaction.user), bot_name)
        await interaction.followup.send(result[:1900])

    @app_commands.command(name="manage", description="Manage panel bot")
    @app_commands.choices(action=[
        app_commands.Choice(name="Start", value="start"),
        app_commands.Choice(name="Stop", value="stop"),
        app_commands.Choice(name="Restart", value="restart"),
        app_commands.Choice(name="Status", value="status"),
        app_commands.Choice(name="Log", value="log"),
    ])
    async def manage(self, interaction: discord.Interaction,
                      action: app_commands.Choice[str], bot_name: str = "Main Bot"):
        await self._remote(interaction, action.value, bot_name)

    @app_commands.command(name="info", description="Panel information")
    async def info(self, interaction: discord.Interaction):
        await self._remote(interaction, "info")

    @app_commands.command(name="status", description="Panel status")
    async def status(self, interaction: discord.Interaction):
        await self._remote(interaction, "status")

    @app_commands.command(name="stress", description="Resource check")
    async def stress(self, interaction: discord.Interaction):
        await self._remote(interaction, "stressz")

    @app_commands.command(name="log", description="Panel log")
    async def log(self, interaction: discord.Interaction):
        await self._remote(interaction, "log")

    @app_commands.command(name="start", description="Start the bot")
    async def start(self, interaction: discord.Interaction):
        await self._remote(interaction, "start")

    @app_commands.command(name="stop", description="Stop the bot")
    async def stop(self, interaction: discord.Interaction):
        await self._remote(interaction, "stop")

    @app_commands.command(name="restart", description="Restart the bot")
    async def restart(self, interaction: discord.Interaction):
        await self._remote(interaction, "restart")

    @app_commands.command(name="leave", description="Bot leaves a server")
    @app_commands.describe(guild_id="Discord server ID")
    async def leave(self, interaction: discord.Interaction, guild_id: str):
        if not self.connected_panel_id:
            await interaction.response.send_message("Use /connect first.", ephemeral=True)
            return
        try:
            guild = self.bot.get_guild(int(guild_id))
        except ValueError:
            guild = None
        if guild is None:
            await interaction.response.send_message("Server not found.", ephemeral=True)
            return
        await guild.leave()
        await interaction.response.send_message(f"Bot left: {guild.name}")

    @app_commands.command(name="broadcast", description="Message all servers")
    @app_commands.describe(message="The global message")
    async def broadcast(self, interaction: discord.Interaction, message: str):
        config = self.load_config()
        allowed = {str(v) for v in config.get("allowed_discord_ids", [])}
        if config.get("test_mode", False) and str(interaction.user.id) not in allowed:
            await interaction.response.send_message(
                "Only testers can use it.", ephemeral=True)
            return
        if not self.connected_panel_id:
            await interaction.response.send_message("Use /connect first.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        result = await self.request_panel(
            "broadcast", str(interaction.user), BOT_NAME, {"message": message})
        await interaction.followup.send(result[:1900], ephemeral=True)

    def _load_commander_commands(self):
        path = os.path.join(BOT_DIR, "commander_commands.json")
        if not os.path.exists(path):
            print("[PANEL] No commander_commands.json — no custom commands.")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                commands_list = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"[PANEL] Commander file error: {e}")
            return
        print(f"[PANEL] Loading commander commands ({len(commands_list)})...")
        for entry in commands_list:
            if not entry.get("enabled", True):
                continue
            name = entry.get("name", "").strip().lower()
            if not name or not name.replace("_", "").isalnum():
                continue
            description = entry.get("description", "Custom command")

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
                            await interaction.response.send_message(
                                embed=embed,
                                ephemeral=cmd_entry.get("ephemeral", False))
                        else:
                            content = cmd_entry.get("content", "") or "\u200b"
                            await interaction.response.send_message(
                                content,
                                ephemeral=cmd_entry.get("ephemeral", False))
                    except Exception as e:
                        print(f"[PANEL] Commander /{cmd_name} error: {e}")
                return callback

            try:
                cmd = app_commands.Command(name=name, description=description,
                                             callback=make_callback(entry, name))
                self.bot.tree.add_command(cmd)
                print(f"[PANEL] OK Commander command: /{name}")
            except Exception as e:
                print(f"[PANEL] ERROR Commander ({name}): {e}")


async def _load_auto_extensions(bot):
    ext_file = os.path.join(BOT_DIR, "bot_extensions.txt")
    if not os.path.exists(ext_file):
        return
    print("[PANEL] Loading auto-extensions...")
    try:
        with open(ext_file, "r", encoding="utf-8") as f:
            for line in f:
                name = line.strip()
                if not name or name.startswith("#"):
                    continue
                try:
                    await bot.load_extension(name)
                    print(f"[PANEL] OK Extension: {name}")
                except Exception as e:
                    print(f"[PANEL] ERROR Extension ({name}): {e}")
    except Exception as e:
        print(f"[PANEL] Auto-extension error: {e}")


async def setup(bot):
    cog = PanelIntegrity(bot)
    cog._load_commander_commands()
    await bot.add_cog(cog)
    await _load_auto_extensions(bot)
'''


# =====================================================================
#  Nyelv-alapú választó
# =====================================================================
def get_version_template(lang="English"):
    if lang == "Magyar":
        return VERSION_FILE_TEMPLATE
    return VERSION_FILE_TEMPLATE_EN


def get_bot_py_template(lang="English"):
    if lang == "Magyar":
        return BOT_PY_TEMPLATE_HU
    return BOT_PY_TEMPLATE_EN


def get_panel_integrity_code(lang="English"):
    # A bot kódja nyelvfüggetlen (angol a Python szintaxis)
    return PANEL_INTEGRITY_CODE


# === RÉGI NEVEK (visszafelé kompatibilitás) ===
VERSION_FILE_TEMPLATE = VERSION_FILE_TEMPLATE_HU if "HU" in globals() else VERSION_FILE_TEMPLATE
BOT_PY_TEMPLATE = BOT_PY_TEMPLATE_HU
INFO_FILE_TEMPLATE = ""  # már nem használt