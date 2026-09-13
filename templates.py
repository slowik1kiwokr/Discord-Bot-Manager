VERSION_FILE_TEMPLATE = '''BOT_NAME = "Main Bot"
BOT_VERSION = "1.0.0"
BOT_TOKEN = "ide_ird_a_bot_tokened"
'''

INFO_FILE_TEMPLATE = '''from version import BOT_NAME, BOT_VERSION

BOT_INFO = {
    "name": BOT_NAME,
    "version": BOT_VERSION,
}
'''

BOT_VEZERLO_CODE = r'''import asyncio
import datetime
import json
import os
import uuid

import discord
from discord import app_commands
from discord.ext import commands, tasks

BOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BOT_DIR, "bot_config.json")
STATS_PATH = os.path.join(BOT_DIR, "bot_stats.json")
try:
    from version import BOT_NAME, BOT_VERSION
except ImportError:
    BOT_NAME, BOT_VERSION = "Main Bot", "1.0.0"

class BotVezerlo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.connected_panel_id = None
        self.connected_source = "Discord"
        self.stats_loop.start()

    def load_config(self):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as config_file:
                return json.load(config_file)
        except (OSError, json.JSONDecodeError):
            return {"panel_id": "#00001", "test_mode": False}

    def panel_directory(self):
        configured_path = self.load_config().get("panel_dir", "")
        if configured_path and os.path.isdir(configured_path):
            return configured_path
        return os.path.dirname(os.path.abspath(__file__))

    async def request_panel(self, action, user, bot_name="Main Bot", data=None):
        config = self.load_config()
        expected_id = config.get("panel_id", "#00001")
        if self.connected_panel_id != expected_id:
            return "Elobb hasznald a /connect parancsot."

        panel_dir = self.panel_directory()
        command_path = os.path.join(panel_dir, "panel_commands.json")
        response_dir = os.path.join(panel_dir, "panel_responses")
        os.makedirs(response_dir, exist_ok=True)
        request_id = uuid.uuid4().hex
        request = {
            "id": request_id,
            "action": action,
            "user": user,
            "source": self.connected_source,
            "bot": bot_name,
            "data": data or {},
            "created_at": datetime.datetime.now().isoformat(timespec="seconds")
        }
        try:
            pending = []
            if os.path.exists(command_path):
                with open(command_path, "r", encoding="utf-8") as command_file:
                    pending = json.load(command_file)
            pending.append(request)
            temporary_path = command_path + ".tmp"
            with open(temporary_path, "w", encoding="utf-8") as command_file:
                json.dump(pending, command_file, ensure_ascii=False)
            os.replace(temporary_path, command_path)
        except (OSError, json.JSONDecodeError) as error:
            return f"A panel nem erheto el: {error}"

        response_path = os.path.join(response_dir, request_id + ".json")
        for _ in range(20):
            await asyncio.sleep(0.5)
            if os.path.exists(response_path):
                try:
                    with open(response_path, "r", encoding="utf-8") as response_file:
                        response = json.load(response_file)
                    os.remove(response_path)
                    if action == "broadcast" and response.get("action") == "broadcast":
                        return await self.broadcast_to_guilds(response.get("data", {}))
                    return response.get("message", "Nincs valasz.")
                except (OSError, json.JSONDecodeError):
                    return "A panel valasza nem olvashato."
        return "A panel 10 masodpercen belul nem valaszolt."

    async def broadcast_to_guilds(self, data):
        message = str(data.get("message", "")).strip()
        channel_map = {str(key): str(value) for key, value in data.get("channels", {}).items()}
        if not message:
            return "A broadcast uzenete ures."
        sent = 0
        failed = 0
        for guild in self.bot.guilds:
            channel_id = channel_map.get(str(guild.id))
            channel = self.bot.get_channel(int(channel_id)) if channel_id and channel_id.isdigit() else None
            if channel is None:
                channel = next((candidate for candidate in guild.text_channels if candidate.permissions_for(guild.me).send_messages), None)
            if channel is None:
                failed += 1
                continue
            try:
                await channel.send(message)
                sent += 1
            except (discord.Forbidden, discord.HTTPException):
                failed += 1
        return f"Broadcast elkuldve. Sikeres: {sent}, sikertelen: {failed}."

    @tasks.loop(seconds=2)
    async def stats_loop(self):
        await self.process_panel_broadcasts()
        config = self.load_config()
        activities = config.get("activity_loop", [])
        if not activities and config.get("activity_text", ""):
            activities = [{"type": config.get("activity_type", "Playing"), "text": config.get("activity_text", "")}]
        if config.get("activity_enabled", True) and activities:
            interval_seconds = max(60, int(config.get("activity_interval_minutes", 5)) * 60)
            activity = activities[int(datetime.datetime.now().timestamp() // interval_seconds) % len(activities)]
            activity_text = activity.get("text", "")
            activity_type = activity.get("type", "Playing")
            activity_class = {
                "Listening": discord.ActivityType.listening,
                "Watching": discord.ActivityType.watching,
                "Streaming": discord.ActivityType.streaming,
            }.get(activity_type, discord.ActivityType.playing)
            if activity_text:
                await self.bot.change_presence(activity=discord.Activity(type=activity_class, name=activity_text))
        stats = {
            "panel_id": config.get("panel_id", "#00001"),
            "guilds": len(self.bot.guilds),
            "users": sum(g.member_count or 0 for g in self.bot.guilds),
            "api_ping": round(self.bot.latency * 1000),
            "test_mode_active": config.get("test_mode", False),
            "name": BOT_NAME,
            "version": BOT_VERSION,
            "updated_at": datetime.datetime.now().isoformat(timespec="seconds")
        }
        try:
            with open(STATS_PATH, "w", encoding="utf-8") as stats_file:
                json.dump(stats, stats_file, ensure_ascii=False, indent=4)
            servers_dir = os.path.join(BOT_DIR, "data", "servers")
            os.makedirs(servers_dir, exist_ok=True)
            for guild in self.bot.guilds:
                with open(os.path.join(servers_dir, f"{guild.id}.json"), "w", encoding="utf-8") as server_file:
                    json.dump({
                        "guild_id": guild.id,
                        "name": guild.name,
                        "member_count": guild.member_count,
                        "owner": str(guild.owner),
                        "description": guild.description,
                        "created_at": guild.created_at.isoformat(),
                        "bot_name": BOT_NAME,
                        "version": BOT_VERSION,
                        "updated_at": datetime.datetime.now().isoformat(timespec="seconds")
                    }, server_file, ensure_ascii=False, indent=4)
        except OSError:
            pass

    async def process_panel_broadcasts(self):
        request_path = os.path.join(self.panel_directory(), "panel_broadcast_requests.json")
        if not os.path.exists(request_path):
            return
        try:
            with open(request_path, "r", encoding="utf-8") as request_file:
                requests = json.load(request_file)
            remaining = []
            for request in requests:
                if request.get("bot", BOT_NAME) != BOT_NAME:
                    remaining.append(request)
                    continue
                result = await self.broadcast_to_guilds(request)
                self.connected_source = "Panel"
                print("[BROADCAST]", result)
            temporary_path = request_path + ".tmp"
            with open(temporary_path, "w", encoding="utf-8") as request_file:
                json.dump(remaining, request_file, ensure_ascii=False)
            os.replace(temporary_path, request_path)
        except (OSError, json.JSONDecodeError):
            return

    @stats_loop.before_loop
    async def before_stats(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="connect", description="Kapcsolodas a panelhez")
    @app_commands.describe(panel_id="A panel azonositoja, peldaul #12345", device="Telefon vagy PC")
    @app_commands.choices(device=[
        app_commands.Choice(name="Telefon", value="Telefon"),
        app_commands.Choice(name="PC", value="PC")
    ])
    async def connect(self, interaction: discord.Interaction, panel_id: str, device: app_commands.Choice[str] = None):
        if panel_id.strip() != self.load_config().get("panel_id", "#00001"):
            await interaction.response.send_message("Hibas panelazonosito.", ephemeral=True)
            return
        self.connected_panel_id = panel_id.strip()
        self.connected_source = device.value if device else "Discord"
        await interaction.response.send_message("Kapcsolodva a panelhez.", ephemeral=True)

    async def remote_command(self, interaction, action, bot_name="Main Bot"):
        config = self.load_config()
        allowed_ids = {str(value) for value in config.get("allowed_discord_ids", [])}
        if config.get("test_mode", False) and str(interaction.user.id) not in allowed_ids:
            await interaction.response.send_message("A bot teszt módban van. Jelenleg csak a tesztelők használhatják.", ephemeral=True)
            return
        if not self.connected_panel_id:
            await interaction.response.send_message("Elobb hasznald a /connect parancsot.", ephemeral=True)
            return
        await interaction.response.defer()
        result = await self.request_panel(action, str(interaction.user), bot_name)
        await interaction.followup.send(result[:1900])

    @app_commands.command(name="broadcast", description="Uzenet kuldese az osszes csatlakoztatott szerverre")
    @app_commands.describe(message="A globalis uzenet szovege", bot_neve="A panelben levo bot neve")
    async def broadcast(self, interaction: discord.Interaction, message: str, bot_neve: str = "Main Bot"):
        config = self.load_config()
        allowed_ids = {str(value) for value in config.get("allowed_discord_ids", [])}
        if config.get("test_mode", False) and str(interaction.user.id) not in allowed_ids:
            await interaction.response.send_message("A bot teszt modban van. Jelenleg csak a tesztelok hasznalhatjak.", ephemeral=True)
            return
        if not self.connected_panel_id:
            await interaction.response.send_message("Elobb hasznald a /connect parancsot.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True)
        result = await self.request_panel("broadcast", str(interaction.user), bot_neve, {"message": message})
        await interaction.followup.send(result[:1900], ephemeral=True)

    @app_commands.command(name="vezerles", description="Panelen lévő bot kezelése")
    @app_commands.describe(muvelet="Művelet", bot_neve="A panelben lévő bot neve")
    @app_commands.choices(muvelet=[
        app_commands.Choice(name="Indítás", value="start"),
        app_commands.Choice(name="Leállítás", value="stop"),
        app_commands.Choice(name="Újraindítás", value="restart"),
        app_commands.Choice(name="Állapot", value="status"),
        app_commands.Choice(name="Napló", value="log")
    ])
    async def vezerles(self, interaction: discord.Interaction, muvelet: app_commands.Choice[str], bot_neve: str = "Main Bot"):
        await self.remote_command(interaction, muvelet.value, bot_neve)

    @app_commands.command(name="info", description="Panel informacio")
    async def info(self, interaction: discord.Interaction):
        await self.remote_command(interaction, "info")

    @app_commands.command(name="status", description="Panel allapot")
    async def status(self, interaction: discord.Interaction):
        await self.remote_command(interaction, "status")

    @app_commands.command(name="stressz", description="Erőforras ellenorzes")
    async def stressz(self, interaction: discord.Interaction):
        await self.remote_command(interaction, "stressz")

    @app_commands.command(name="log", description="Panel naplo")
    async def log(self, interaction: discord.Interaction):
        await self.remote_command(interaction, "log")

    @app_commands.command(name="start", description="Bot inditasa")
    async def start(self, interaction: discord.Interaction):
        await self.remote_command(interaction, "start")

    @app_commands.command(name="stop", description="Bot leallitasa")
    async def stop(self, interaction: discord.Interaction):
        await self.remote_command(interaction, "stop")

    @app_commands.command(name="restart", description="Bot ujrainditasa")
    async def restart(self, interaction: discord.Interaction):
        await self.remote_command(interaction, "restart")

    @app_commands.command(name="kilepes", description="A bot kilep egy Discord szerverrol")
    @app_commands.describe(guild_id="A Discord szerver azonositoja")
    async def kilepes(self, interaction: discord.Interaction, guild_id: str):
        if not self.connected_panel_id:
            await interaction.response.send_message("Elobb hasznald a /connect parancsot.", ephemeral=True)
            return
        try:
            guild = self.bot.get_guild(int(guild_id))
        except ValueError:
            guild = None
        if guild is None:
            await interaction.response.send_message("Nem talalhato ilyen szerver.", ephemeral=True)
            return
        await guild.leave()
        await interaction.response.send_message(f"A bot kilepett innen: {guild.name}")

async def setup(bot):
    await bot.add_cog(BotVezerlo(bot))'''   # ← a hosszú kód a panel.pyw-ből
PANEL_EXTENSION_CODE = BOT_VEZERLO_CODE