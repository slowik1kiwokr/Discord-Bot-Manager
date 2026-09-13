import webbrowser

import customtkinter as ctk

from modules.languages import LANGUAGES


# =====================================================================
#  TUTORIAL TARTALOM — kétnyelvű
#  A panel aktuális nyelvét követi (self.current_language)
# =====================================================================
TUTORIAL_CONTENT = {
    "Magyar": [
        {
            "id": "getting_started",
            "title": "🚀 Első lépések",
            "content": """# 🚀 Első lépések

## Mi ez a panel?
A Discord Bot Manager egy több botot kezelő vezérlőpult.
Egyszerre több botot indíthatsz, állíthatsz le, figyelhetsz
és szabályozhatsz egyetlen felületről.

## Első indítás
1. Indítsd el a panel.pyw-t dupla kattintással
2. Megjelenik a Splash képernyő — várj 3 másodpercet
3. Ha jelszót állítottál be, be kell írnod
4. Megnyílik a főablak

## Alap felépítés
A panel három részre oszlik:

Bal oldal — Vezérlő menü
  - Control: Bot indítás/leállítás/újraindítás
  - Bulk Control: Összes bot egyszerre
  - Tools: GitHub, Integráció, Tutorial
  - Statistics: Beállítások, Statisztikák, Backup

Középső rész — Élő naplók
  - A futó botok üzenetei valós időben
  - Szűrők: ALL / ERRORS / SUCCESS / EVENTS
  - Keresés a naplókban

Jobb oldal — Pro metrikák
  - Bot neve, verziója, uptime
  - RAM, CPU, hőmérséklet
  - Szerverek, felhasználók, hibák

## Első bot hozzáadása
1. Kattints a + gombra a fülek mellett (bal felül)
2. Adj neki nevet (pl. ZeneBot)
3. Kattints a Tallózás gombra
4. Válaszd ki a botod fő .py fájlját (pl. bot.py)
5. Kattints a Mentés gombra
6. Kész! Most már tudod indítani.
""",
        },
        {
            "id": "bot_management",
            "title": "🤖 Bot kezelés",
            "content": """# 🤖 Bot kezelés

## Bot indítása
1. Válaszd ki a botot a fülek közül (bal felül)
2. Kattints a Start Bot gombra
3. A bal oldali státusz zöldre vált (ONLINE)
4. Az Élő naplók elkezdenek görögni

## Bot leállítása
1. Kattints a Stop gombra
2. A bot folyamat leáll, a státusz piros lesz (OFFLINE)

## Újraindítás
1. Kattints a Restart gombra
2. A panel leállítja, majd 1,5 másodperc múlva újraindítja

## Több bot kezelése
Fülek
  - Minden bot külön fülön jelenik meg
  - Kattints rájuk a váltáshoz

Jobb klikk egy fülre
  - Átnevezés
  - Törlés (csak ha nem az első bot)

Új bot hozzáadása
  - Kattints a + gombra a fülek mellett

## Tömeges vezérlés (Bulk Control)
A bal oldali menüben:
  - Start All — összes bot indítása
  - Restart All — összes bot újraindítása
  - Stop All — összes bot leállítása

## Automatikus újraindítás
A bot beállításainál (fő panel, középső rész):
  - Auto-indítás — a panel indulásakor automatikusan elindul
  - Auto Restart — időzített újraindítás (nap/óra/perc)
  - Midnight Restart — éjfélkor újraindul

## Crash védelem
Ha a bot összeomlik, a panel:
  1. Naplózza a hibát (ERROR szint)
  2. Ha be van kapcsolva, újraindítja (Crash Watchdog)
  3. A Settings ablakban állítható a várakozási idő
""",
        },
        {
            "id": "settings",
            "title": "⚙️ Beállítások",
            "content": """# ⚙️ Beállítások

## Settings ablak megnyitása
Bal oldali menü -> Settings

## Panel Settings fül

Panel azonosító
  - Egyedi azonosító, amivel a bot kapcsolódik
  - Használd a Copy /connect command gombot a Discordban

Panel jelszó
  - Üresen hagyva: nincs védelem
  - Kitöltve: a panel induláskor kéri a jelszót

Nyelv
  - English / Magyar

Kicsinyítés tálcára
  - Ha be van kapcsolva, X-re a tálcára kerül
  - Jobb klikk a tálcaikonra -> megnyitás

Discord Rich Presence
  - Discord profilodon megjelenik, hogy a panelt használod

Napló mentési szint
  - Mindent mentse
  - Csak hibák
  - Csak események
  - Sikeres interakciók

Hiba hang
  - Válassz hangot a legördülőből
  - A Teszt hang gombbal meghallgathatod

Automatikus biztonsági mentés
  - Be/ki kapcsolható
  - Panel indulásakor azonnal
  - Időzített (pl. 24 óránként)

## Bot Settings fül

Maximum RAM használat
  - Ha a bot túllépi, a panel figyelmeztet
  - Opcionálisan automatikusan leállítja

Teszt mód
  - Csak a megadott Discord ID-k használhatják a botot

Tesztelők Discord ID-i
  - Vesszővel elválasztva
  - Pl.: 123456789012345678, 987654321098765432

Auto-Restart on Crash
  - Ha a bot összeomlik, automatikusan újraindul
  - Állítsd be a várakozási időt másodpercben
""",
        },
        {
            "id": "commander",
            "title": "⚡ Commander (Parancsok)",
            "content": """# ⚡ Commander — Dinamikus parancsok

## Mi ez?
A Commanderrel kód írása nélkül hozhatsz létre Discord
parancsokat. Sima szöveges üzenet vagy szép embed formában.

## Használat
1. Bal oldali menü -> Commander
2. Kattints az Új parancs gombra
3. Válassz sablont a legördülőből
4. Töltsd ki a mezőket
5. Mentés

## Elérhető sablonok

Szöveges üzenetek
  - Egyszerű szöveges üzenet
  - Üdvözlő szöveges üzenet

Embed üzenetek
  - Egyszerű embed (kék)
  - Színes értesítő embed (narancs)
  - Hiba embed (piros)
  - Siker embed (zöld)
  - Segítség embed (több mezővel)

## Parancs beállításai

Név
  - Per jel nélkül (pl. parancs1 -> /parancs1)
  - Csak betű, szám, alulvonás

Leírás
  - Megjelenik a Discord / menüben

Típus
  - Üzenet: sima szöveg
  - Embed: színes, formázott üzenet

Embed szín
  - Hex kód (pl. #5865F2)
  - Gyors gombok: Blurple, Zöld, Piros, Narancs, Kék, Lila, Sárga

Ephemeral
  - Csak a hívónak látszik (nem látszik másoknak)

Engedélyezve
  - Kikapcsolva: a bot nem tölti be

## Commander.py a botba
1. Kattints a Commander.py a botba gombra
2. A panel legenerálja a bot mappájába
3. A bot bot.py-jában legyen benne:
   await bot.load_extension("Commander")
4. Indítsd újra a botot

## Discord parancsok frissítése
A Discord 1 óránként frissíti a slash parancsokat.
Ha azonnal akarod:
  - Fejlesztői szerveren: /commander_reload
  - Vagy indítsd újra a botot
""",
        },
        {
            "id": "plugins",
            "title": "🧩 Pluginok",
            "content": """# 🧩 Pluginok — Panel bővítése

## Mi ez?
A pluginok Python fájlok, amik a panelbe épülnek be,
és új funkciókat adnak hozzá. Nem kell a fő kódot módosítani.

## Plugin ablak
Bal oldali menü -> Plugins

Bal oldal — a meglévő pluginok listája
Jobb oldal — a kiválasztott plugin kódja

## Új plugin létrehozása
1. Kattints az Új plugin gombra
2. Adj neki fájlnevet (pl. sajat_plugin.py)
3. Válassz sablont
4. Létrehozás

## Elérhető sablonok

Ures plugin
  - Csak a váz, semmit nem csinál

Esemény loggoló
  - 10 másodpercenként naplóbejegyzést ír

Egyedi gomb a sidebar-hoz
  - Új gomb a bal oldali menüben

Egyedi ablak megnyitó gomb
  - Új ablak, amit gombbal nyitsz meg

Üdvözlő üzenet a naplóban
  - Csak egy egyszerű üzenet

Bot állapot figyelő
  - Figyeli, ha egy bot leáll vagy elindul

Hangjelzés hibánál
  - Extra Beep, ha ERROR van a naplóban

Egyszerű számológép ablak
  - Működő számológép

Téma váltó gombok
  - Sötét / Zöld téma gyorsváltó

Discord webhook értesítés
  - Hibák továbbítása webhookra

## Plugin szerkesztése
1. Válaszd ki a bal oldali listából
2. Szerkeszd a jobb oldali szerkesztőben
3. Mentés — szintaktikai ellenőrzéssel

## Plugin törlése
1. Válaszd ki
2. Törlés

## Plugin újratöltése
Ha módosítottál egy plugint, az Újratöltés gombbal
azonnal életbe lép (nem kell újraindítani a panelt).

## Plugin struktúra
Minden pluginben kell egy setup_panel(panel) függvény.
A panel paraméter a fő panel példány, amit használhatsz.
""",
        },
        {
            "id": "backup",
            "title": "💾 Biztonsági mentés",
            "content": """# 💾 Biztonsági mentés

## Mi ez?
A panel ZIP fájlba menti:
  - Az összes bot beállítását (bots.json)
  - A panel beállításait (settings.json)
  - A botok adatait (data/, .db, .json)

## Backup ablak
Bal oldali menü -> Backups

## Új mentés készítése
1. Kattints az Új mentés gombra
2. A panel ZIP-et készít a backups/ mappába
3. Formátum: bot_backup_2025-01-20_14-30-00.zip

## Visszaállítás
1. Válaszd ki a mentést a listából
2. Kijelölt visszaállítása gomb
3. Megerősítés után a fájlok felülíródnak
4. Indítsd újra a panelt

## Automatikus mentés
A Settings ablakban állítható:

Automatikus biztonsági mentés
  - Be/ki kapcsolható

Mentés panelindításkor
  - Induláskor azonnal készít egyet

Időzített mentés gyakorisága
  - Órában (pl. 24 = naponta)
  - 0 = kikapcsolva

## Mit tartalmaz a mentés?
  - bots.json — botok beállításai
  - settings.json — panel beállítások
  - bots/<bot_nev>/ — minden bot adata
  - .db, .sqlite — adatbázisok
  - data/ mappa — szerver adatok
""",
        },
        {
            "id": "github_update",
            "title": "🚀 Frissítések",
            "content": """# 🚀 Automatikus frissítés

## Hogyan működik?
A panel 60 percenként ellenőrzi a GitHubon, van-e új verzió.
Ha igen, felugró ablakban jelzi.

## Frissítés ablak

Fejléc
  - Jelenlegi verzió -> Új verzió

Changelog
  - A fejlesztő által írt változások listája

3 gomb:
  - Frissítés letöltése — letölti és telepíti
  - Később — bezárja, 1 óra múlva újra jelzi
  - Kihagyás — nem jelzi, amíg újra nem indítod

## Letöltés folyamata
1. ZIP letöltése a GitHub-ról
2. Kicsomagolás
3. Futó botok leállítása
4. Fájlok frissítése (védett fájlok kihagyásával)
5. Verziószám frissítése

## Védett fájlok
Ezek soha nem íródnak felül:
  - bots.json — botjaid beállításai
  - settings.json — panel beállítások
  - backups/ — mentések
  - plugins/ — pluginjaid
  - logs/ — naplók
  - Saját ikonok

## Újraindítás
A letöltés után a panel kérdezi:
  - Újraindítás most — bezárja és újraindítja
  - Kilépés — bezárja, te indítod újra

## Manuális ellenőrzés
Bal oldali menü -> GitHub Frissítés
Mindig megmutatja, van-e új verzió (akár van, akár nincs).
""",
        },
        {
            "id": "statistics",
            "title": "📊 Statisztikák",
            "content": """# 📊 Statisztikák

## Pro metrikák (jobb oldal)
A főablak jobb oldalán látható:

Bot információk
  - Bot neve, verziója
  - Uptime (munkamenet) — mióta fut
  - Heti uptime — összesített futási idő
  - Ping válaszidők (API / Msg)
  - Összes parancs

PC erőforrások
  - RAM használat
  - CPU használat
  - PC hőmérséklet (ha elérhető)
  - Szerverek (guilds) száma
  - Elért felhasználók
  - Hibák számlálója

## Teljesítmény grafikon
Kattints a Teljesítmény grafikon gombra:

Időtáv választó
  - Utolsó 10 perc
  - Utolsó 1 óra
  - Utolsó 24 óra

Grafikonok
  - RAM használat (kék vonal)
  - CPU használat (zöld vonal)

Export
  - PNG mentése gombbal elmented a képet

## Globális statisztika
Bal oldali menü -> Global Statistics

Áttekintés fül
  - Az összes bot állapota
  - Parancsszám, hibák

Parancs statisztika fül
  - Napi parancsok
  - Legnépszerűbb parancsok (Top 10)

## Naplók szűrése
A középső részen:

Szűrő gombok
  - ALL — összes napló
  - ERRORS — csak hibák (piros)
  - SUCCESS — csak sikerek (zöld)
  - EVENTS — csak események (lila)

Keresés
  - Írj be szöveget a keresőbe
  - Azonnal szűri a naplókat

Automatikus görgetés
  - Pipáld be — mindig a legfrissebb sorra ugrik

Törlés
  - A Törlés gombbal kiüríted a naplót
""",
        },
        {
            "id": "integration",
            "title": "📌 Bot integráció",
            "content": """# 📌 Bot integráció

## Mi ez?
A panel és a botod együttműködnek. A bot egy kiegészítő
kódot kap, ami a panel parancsait fogadja.

## Integrációs ablak
Bal oldali menü -> Alapok / Integráció

## 3 fül

1. bot.py sablon
  - Kész bot.py kód, amit másolhatsz
  - Tartalmazza a Panel extension betöltést
  - Parancsok: /teszt, /parancsok

2. Panel.py kód
  - A Panel.py extension kódja
  - Ez teszi lehetővé a /connect parancsot
  - A bot statisztikáit a panelnek küldi

3. Tutorial
  - Lépésről lépésre útmutató
  - Függőségek telepítése gombbal

## Bot összekötése a panellel

1. lépés: Bot fájl kiválasztása
  - A fő panelen tallózd be a bot .py fájlját

2. lépés: Panel.py mentése
  - Kattints a Panel.py összekötése gombra
  - A panel létrehozza a bot mappájában

3. lépés: bot.py módosítása
  - Nyisd meg a bot.py-t
  - Az on_ready() függvénybe írd:
    await bot.load_extension("Panel")

4. lépés: Bot újraindítás
  - A panelen indítsd újra a botot

5. lépés: /connect parancs
  - A panelen kattints a Copy /connect command gombra
  - Discordban írd be a másolt parancsot
  - Pl.: /connect panel_id:#ABC123 device:PC

6. lépés: Kész!
  - A bot most már a panelről vezérelhető
  - Discordból is: /start, /stop, /restart, /broadcast

## Elérhető Discord parancsok

Vezérlés (panelről)
  - /connect — kapcsolódás a panelhez
  - /start — bot indítása
  - /stop — bot leállítása
  - /restart — bot újraindítása
  - /status — bot állapota
  - /info — panel információ
  - /log — utolsó naplóbejegyzések
  - /stressz — rendszer-erőforrás ellenőrzés

Üzenetküldés
  - /broadcast — üzenet az összes szerverre

Kilépés
  - /kilepes — bot kilép egy szerverből

## Panel azonosító
Minden panelnek van egy egyedi azonosítója:
  - Formátum: #XXXXXXXX
  - A bal oldali menüben látható
  - Ezzel tud a bot kapcsolódni

## Bot verzió és token
A bot mappájában lévő version.py:
  - BOT_NAME — bot neve
  - BOT_VERSION — verziószám
  - BOT_TOKEN — Discord token

FIGYELEM: A tokent tartsd titokban!
""",
        },
        {
            "id": "shortcuts",
            "title": "⌨️ Gyorsgombok",
            "content": """# ⌨️ Gyorsgombok és tippek

## Billentyűparancsok

Fő ablak
  - Ctrl + N — Új bot hozzáadása
  - Ctrl + R — Kiválasztott bot újraindítása
  - Ctrl + S — Beállítások mentése
  - F5 — Statisztikák frissítése

Naplók
  - Ctrl + F — Keresés a naplókban
  - Ctrl + L — Naplók törlése

Fülek
  - Ctrl + Tab — Következő bot
  - Ctrl + Shift + Tab — Előző bot

## Tippek

Több bot kezelése
  - Használj beszédes neveket (pl. ZeneBot, ModBot)
  - Csoportosítsd a fülek sorrendjét (balról jobbra fontosság)

Gyorsabb munka
  - Állítsd be az Auto-indítás-t a gyakran használt botoknál
  - Használd a Bulk Control gombokat, ha mind induljon
  - Kapcsold be az automatikus backup-ot (napi)

Hibakeresés
  - Ha a bot leáll, nézd meg a naplót ERROR szűrővel
  - A stressz parancs megmutatja az aktuális CPU/RAM-ot
  - Használd a Crash Watchdog-ot (Settings -> Bot Settings)

Biztonság
  - Készíts backup-ot minden nagyobb változtatás előtt
  - Tartsd a panel jelszót, ha publikus gépen használod
  - A Discord tokent soha ne oszd meg

Testreszabás
  - Settings -> Discord téma (4 beépített)
  - Settings -> Hiba hang (saját választás)
  - Pluginokkal tovább bővíthető

## Hibaelhárítás

A bot nem indul
  - Ellenőrizd, hogy a .py fájl létezik
  - Nézd meg a naplókat (ERROR szűrő)
  - Próbáld manuálisan: py bot.py a bot mappájában

A panel nem érzékeli a botot
  - Ellenőrizd, hogy a /connect parancsot használtad
  - Nézd meg, hogy a panel ID egyezik
  - Bot újraindítás segíthet

A Commander parancsok nem jelennek meg
  - Discord 1 óránként frissíti a slash parancsokat
  - Vagy: /commander_reload fejlesztői szerveren
  - Vagy: bot újraindítás

Nem jelenik meg a hőmérséklet
  - A Windows gyakran nem adja ki WMI-n
  - Telepítsd a LibreHardwareMonitor-t
  - Vagy hagyd figyelmen kívül (CPU % mutatja a terhelést)
""",
        },
    ],
    "English": [
        {
            "id": "getting_started",
            "title": "🚀 Getting Started",
            "content": """# 🚀 Getting Started

## What is this panel?
Discord Bot Manager is a control panel for managing multiple bots.
You can start, stop, monitor and manage several bots at once
from a single interface.

## First launch
1. Launch panel.pyw with a double-click
2. The Splash screen appears — wait 3 seconds
3. If you set a password, enter it
4. The main window opens

## Basic layout
The panel is divided into three parts:

Left side — Control menu
  - Control: Start/Stop/Restart bot
  - Bulk Control: All bots at once
  - Tools: GitHub, Integration, Tutorial
  - Statistics: Settings, Statistics, Backups

Middle part — Live logs
  - Running bots' messages in real time
  - Filters: ALL / ERRORS / SUCCESS / EVENTS
  - Search in logs

Right side — Pro metrics
  - Bot name, version, uptime
  - RAM, CPU, temperature
  - Servers, users, errors

## Adding your first bot
1. Click the + button next to the tabs (top left)
2. Give it a name (e.g. MusicBot)
3. Click the Browse button
4. Select your bot's main .py file (e.g. bot.py)
5. Click Save
6. Done! You can now start it.
""",
        },
        {
            "id": "bot_management",
            "title": "🤖 Bot Management",
            "content": """# 🤖 Bot Management

## Starting a bot
1. Select the bot from the tabs (top left)
2. Click the Start Bot button
3. The left status turns green (ONLINE)
4. Live logs start scrolling

## Stopping a bot
1. Click the Stop button
2. The bot process stops, status turns red (OFFLINE)

## Restarting
1. Click the Restart button
2. The panel stops it, then restarts after 1.5 seconds

## Managing multiple bots
Tabs
  - Each bot appears on a separate tab
  - Click them to switch

Right-click on a tab
  - Rename
  - Delete (only if not the first bot)

Adding a new bot
  - Click the + button next to the tabs

## Bulk Control
In the left menu:
  - Start All — start all bots
  - Restart All — restart all bots
  - Stop All — stop all bots

## Automatic restart
In the bot settings (main panel, middle section):
  - Auto-start — starts automatically when panel launches
  - Auto Restart — scheduled restart (day/hour/minute)
  - Midnight Restart — restarts at midnight

## Crash protection
If the bot crashes, the panel:
  1. Logs the error (ERROR level)
  2. If enabled, restarts it (Crash Watchdog)
  3. The wait time is configurable in Settings
""",
        },
        {
            "id": "settings",
            "title": "⚙️ Settings",
            "content": """# ⚙️ Settings

## Opening the Settings window
Left menu -> Settings

## Panel Settings tab

Panel ID
  - Unique identifier the bot connects with
  - Use the Copy /connect command button in Discord

Panel password
  - Empty: no protection
  - Filled: the panel asks for the password on launch

Language
  - English / Magyar

Minimize to tray
  - If enabled, X sends it to the system tray
  - Right-click the tray icon -> open

Discord Rich Presence
  - Shows on your Discord profile that you use the panel

Log save level
  - Save everything
  - Only errors
  - Only events
  - Successful interactions

Error sound
  - Choose a sound from the dropdown
  - Use the Test sound button to preview

Automatic backup
  - On/off toggle
  - On panel startup
  - Scheduled (e.g. every 24 hours)

## Bot Settings tab

Maximum RAM usage
  - If the bot exceeds it, the panel warns
  - Optionally auto-terminates

Test mode
  - Only specified Discord IDs can use the bot

Tester Discord IDs
  - Comma-separated
  - E.g.: 123456789012345678, 987654321098765432

Auto-Restart on Crash
  - If the bot crashes, it restarts automatically
  - Set the wait time in seconds
""",
        },
        {
            "id": "commander",
            "title": "⚡ Commander (Commands)",
            "content": """# ⚡ Commander — Dynamic commands

## What is it?
Commander lets you create Discord commands without writing
any code. As plain text messages or beautiful embeds.

## Usage
1. Left menu -> Commander
2. Click the New command button
3. Choose a template from the dropdown
4. Fill in the fields
5. Save

## Available templates

Text messages
  - Simple text message
  - Welcome text message

Embed messages
  - Simple embed (blue)
  - Colorful notification embed (orange)
  - Error embed (red)
  - Success embed (green)
  - Help embed (multiple fields)

## Command settings

Name
  - Without slash (e.g. command1 -> /command1)
  - Letters, numbers, underscore only

Description
  - Appears in the Discord / menu

Type
  - Message: plain text
  - Embed: colored, formatted message

Embed color
  - Hex code (e.g. #5865F2)
  - Quick buttons: Blurple, Green, Red, Orange, Blue, Purple, Yellow

Ephemeral
  - Only visible to the caller (hidden from others)

Enabled
  - Disabled: the bot doesn't load it

## Commander.py to the bot
1. Click the Commander.py to bot button
2. The panel generates it in the bot folder
3. In the bot's bot.py, add:
   await bot.load_extension("Commander")
4. Restart the bot

## Refreshing Discord commands
Discord refreshes slash commands every hour.
To refresh immediately:
  - On a dev server: /commander_reload
  - Or restart the bot
""",
        },
        {
            "id": "plugins",
            "title": "🧩 Plugins",
            "content": """# 🧩 Plugins — Extending the panel

## What is it?
Plugins are Python files that hook into the panel and add
new features. No need to modify the core code.

## Plugin window
Left menu -> Plugins

Left side — list of existing plugins
Right side — code of the selected plugin

## Creating a new plugin
1. Click the New plugin button
2. Give it a filename (e.g. my_plugin.py)
3. Choose a template
4. Create

## Available templates

Empty plugin
  - Just the skeleton, does nothing

Event logger
  - Writes a log entry every 10 seconds

Custom button on sidebar
  - Adds a new button to the left menu

Custom window button
  - A new window opened by a button

Welcome message in log
  - Just a simple message

Bot status watcher
  - Watches when a bot stops or starts

Sound alert on error
  - Extra beep on ERROR in log

Simple calculator window
  - Working calculator

Theme switcher buttons
  - Dark / Green theme quick switch

Discord webhook notification
  - Forwards errors to webhook

## Editing a plugin
1. Select it from the left list
2. Edit it in the right editor
3. Save — with syntax check

## Deleting a plugin
1. Select it
2. Delete

## Reloading plugins
If you modified a plugin, the Reload button applies
changes immediately (no need to restart the panel).

## Plugin structure
Every plugin must have a setup_panel(panel) function.
The panel parameter is the main panel instance you can use.
""",
        },
        {
            "id": "backup",
            "title": "💾 Backups",
            "content": """# 💾 Backups

## What is it?
The panel saves into a ZIP file:
  - All bot settings (bots.json)
  - Panel settings (settings.json)
  - Bot data (data/, .db, .json)

## Backup window
Left menu -> Backups

## Creating a new backup
1. Click the New backup button
2. The panel creates a ZIP in the backups/ folder
3. Format: bot_backup_2025-01-20_14-30-00.zip

## Restore
1. Select the backup from the list
2. Restore selected button
3. After confirmation, files are overwritten
4. Restart the panel

## Automatic backup
Configurable in Settings:

Automatic backup
  - On/off toggle

Backup on panel startup
  - Creates one immediately on launch

Scheduled backup interval
  - In hours (e.g. 24 = daily)
  - 0 = disabled

## What does the backup contain?
  - bots.json — bot settings
  - settings.json — panel settings
  - bots/<bot_name>/ — each bot's data
  - .db, .sqlite — databases
  - data/ folder — server data
""",
        },
        {
            "id": "github_update",
            "title": "🚀 Updates",
            "content": """# 🚀 Automatic update

## How it works
The panel checks GitHub every 60 minutes for a new version.
If found, it shows a popup window.

## Update window

Header
  - Current version -> New version

Changelog
  - List of changes written by the developer

3 buttons:
  - Download update — downloads and installs
  - Later — closes, re-checks after 1 hour
  - Skip — won't show until you restart

## Download process
1. Download ZIP from GitHub
2. Extract
3. Stop running bots
4. Update files (protected files are skipped)
5. Update version number

## Protected files
These are never overwritten:
  - bots.json — your bot settings
  - settings.json — panel settings
  - backups/ — backups
  - plugins/ — your plugins
  - logs/ — logs
  - Custom icons

## Restart
After download, the panel asks:
  - Restart now — closes and restarts
  - Exit — closes, you restart manually

## Manual check
Left menu -> GitHub Update
Always shows whether there's a new version (or not).
""",
        },
        {
            "id": "statistics",
            "title": "📊 Statistics",
            "content": """# 📊 Statistics

## Pro metrics (right side)
Visible on the right side of the main window:

Bot information
  - Bot name, version
  - Uptime (session) — how long it's been running
  - Weekly uptime — total running time
  - Ping response times (API / Msg)
  - Total commands

PC resources
  - RAM usage
  - CPU usage
  - PC temperature (if available)
  - Server (guild) count
  - Users reached
  - Error counter

## Performance chart
Click the Performance chart button:

Time range selector
  - Last 10 minutes
  - Last 1 hour
  - Last 24 hours

Charts
  - RAM usage (blue line)
  - CPU usage (green line)

Export
  - Save PNG button to save the image

## Global statistics
Left menu -> Global Statistics

Overview tab
  - Status of all bots
  - Command count, errors

Command statistics tab
  - Daily commands
  - Most popular commands (Top 10)

## Log filtering
In the middle part:

Filter buttons
  - ALL — all logs
  - ERRORS — errors only (red)
  - SUCCESS — successes only (green)
  - EVENTS — events only (purple)

Search
  - Type text in the search box
  - Filters logs instantly

Auto-scroll
  - Check it — always jumps to the newest line

Clear
  - The Clear button empties the log
""",
        },
        {
            "id": "integration",
            "title": "📌 Bot Integration",
            "content": """# 📌 Bot Integration

## What is it?
The panel and your bot work together. The bot gets an
additional code that receives the panel's commands.

## Integration window
Left menu -> Basics / Integration

## 3 tabs

1. bot.py template
  - Ready-made bot.py code you can copy
  - Contains the Panel extension loading
  - Commands: /test, /commands

2. Panel.py code
  - The Panel.py extension code
  - Enables the /connect command
  - Sends bot statistics to the panel

3. Tutorial
  - Step-by-step guide
  - Install dependencies button

## Connecting your bot to the panel

Step 1: Select bot file
  - Browse your bot's .py file in the main panel

Step 2: Save Panel.py
  - Click the Connect Panel.py button
  - The panel creates it in the bot folder

Step 3: Modify bot.py
  - Open bot.py
  - In the on_ready() function add:
    await bot.load_extension("Panel")

Step 4: Restart bot
  - Restart the bot from the panel

Step 5: /connect command
  - Click Copy /connect command on the panel
  - Paste it in Discord
  - E.g.: /connect panel_id:#ABC123 device:PC

Step 6: Done!
  - The bot is now controllable from the panel
  - Also from Discord: /start, /stop, /restart, /broadcast

## Available Discord commands

Control (from panel)
  - /connect — connect to panel
  - /start — start bot
  - /stop — stop bot
  - /restart — restart bot
  - /status — bot status
  - /info — panel info
  - /log — recent log entries
  - /stress — system resource check

Messaging
  - /broadcast — message to all servers

Leave
  - /kilepes — bot leaves a server

## Panel ID
Every panel has a unique identifier:
  - Format: #XXXXXXXX
  - Visible in the left menu
  - The bot connects using this

## Bot version and token
The version.py file in the bot folder:
  - BOT_NAME — bot name
  - BOT_VERSION — version number
  - BOT_TOKEN — Discord token

WARNING: Keep the token secret!
""",
        },
        {
            "id": "shortcuts",
            "title": "⌨️ Shortcuts",
            "content": """# ⌨️ Shortcuts and tips

## Keyboard shortcuts

Main window
  - Ctrl + N — Add new bot
  - Ctrl + R — Restart selected bot
  - Ctrl + S — Save settings
  - F5 — Refresh statistics

Logs
  - Ctrl + F — Search in logs
  - Ctrl + L — Clear logs

Tabs
  - Ctrl + Tab — Next bot
  - Ctrl + Shift + Tab — Previous bot

## Tips

Managing multiple bots
  - Use descriptive names (e.g. MusicBot, ModBot)
  - Order the tabs by importance (left to right)

Faster workflow
  - Enable Auto-start for frequently used bots
  - Use the Bulk Control buttons to start all
  - Turn on automatic backup (daily)

Debugging
  - If a bot stops, check the log with the ERROR filter
  - The stress command shows current CPU/RAM
  - Use the Crash Watchdog (Settings -> Bot Settings)

Security
  - Make a backup before major changes
  - Set a panel password if used on a shared PC
  - Never share the Discord token

Customization
  - Settings -> Discord theme (4 built-in)
  - Settings -> Error sound (your choice)
  - Extend further with plugins

## Troubleshooting

Bot won't start
  - Check that the .py file exists
  - Check the logs (ERROR filter)
  - Try manually: py bot.py in the bot folder

Panel doesn't detect the bot
  - Check that you used the /connect command
  - Verify the panel ID matches
  - Restarting the bot may help

Commander commands not showing
  - Discord refreshes slash commands hourly
  - Or: /commander_reload on a dev server
  - Or: restart the bot

Temperature not showing
  - Windows often doesn't expose it via WMI
  - Install LibreHardwareMonitor
  - Or ignore it (CPU % shows the load)
""",
        },
    ],
}


class WindowTutorialMixin:
    """Beépített tutorial / súgó ablak — kétnyelvű."""

    def open_tutorial_window(self):
        # A panel aktuális nyelvét használja, fallback English
        lang = getattr(self, "current_language", "English")
        sections = TUTORIAL_CONTENT.get(lang, TUTORIAL_CONTENT["English"])

        title_text = {
            "Magyar": "📖 Tutorial — Discord Bot Manager",
            "English": "📖 Tutorial — Discord Bot Manager",
        }.get(lang, "📖 Tutorial — Discord Bot Manager")

        header_text = {
            "Magyar": "📖  Discord Bot Manager — Teljes útmutató",
            "English": "📖  Discord Bot Manager — Complete Guide",
        }.get(lang, "📖  Discord Bot Manager — Complete Guide")

        categories_text = {
            "Magyar": "📚 Kategóriák",
            "English": "📚 Categories",
        }.get(lang, "📚 Categories")

        hint_text = {
            "Magyar": "💡 Válassz kategóriát\n      a bal oldalról",
            "English": "💡 Choose a category\n      from the left",
        }.get(lang, "💡 Choose a category")

        close_text = {
            "Magyar": "Bezárás",
            "English": "Close",
        }.get(lang, "Close")

        win = ctk.CTkToplevel(self)
        win.title(title_text)
        win.geometry("1100x700")
        win.minsize(900, 560)
        win.grab_set()

        win.update_idletasks()
        x = (win.winfo_screenwidth() - 1100) // 2
        y = (win.winfo_screenheight() - 700) // 2
        win.geometry(f"1100x700+{x}+{y}")

        # --- Fejléc ---
        header = ctk.CTkFrame(win, fg_color="#5865F2", corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text=header_text,
            font=("Arial", 20, "bold"), text_color="white"
        ).pack(side="left", padx=24, pady=16)

        ctk.CTkButton(
            header, text="🌐 GitHub",
            fg_color="#2c3e50", hover_color="#34495e",
            width=110, height=34,
            command=lambda: webbrowser.open(
                "https://github.com/slowik1kiwokr/Discord-Bot-Manager"
            )
        ).pack(side="right", padx=20, pady=16)

        # --- Fő tartalom ---
        main = ctk.CTkFrame(win, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=12, pady=12)

        left = ctk.CTkFrame(main, width=250, corner_radius=8)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        ctk.CTkLabel(
            left, text=categories_text,
            font=("Arial", 14, "bold"), anchor="w"
        ).pack(fill="x", padx=14, pady=(14, 8))

        right = ctk.CTkFrame(main, corner_radius=8)
        right.pack(side="right", fill="both", expand=True)

        content_box = ctk.CTkTextbox(
            right, wrap="word", font=("Consolas", 13),
            activate_scrollbars=True
        )
        content_box.pack(fill="both", expand=True, padx=10, pady=10)

        buttons = {}

        def show_section(section_id):
            for btn in buttons.values():
                btn.configure(fg_color="#2b2b2b")
            if section_id in buttons:
                buttons[section_id].configure(fg_color="#5865F2")

            for section in sections:
                if section["id"] == section_id:
                    content_box.configure(state="normal")
                    content_box.delete("1.0", "end")
                    content_box.insert("1.0", section["content"])
                    content_box.configure(state="disabled")
                    break

        for section in sections:
            btn = ctk.CTkButton(
                left,
                text=section["title"],
                anchor="w",
                fg_color="#2b2b2b",
                hover_color="#3a3a3a",
                height=38,
                font=("Arial", 12),
                command=lambda sid=section["id"]: show_section(sid),
            )
            btn.pack(fill="x", padx=10, pady=3)
            buttons[section["id"]] = btn

        ctk.CTkLabel(
            left,
            text=hint_text,
            font=("Arial", 10), text_color="#888",
            justify="left",
        ).pack(side="bottom", fill="x", padx=14, pady=12)

        ctk.CTkButton(
            win, text=close_text,
            fg_color="#555555", hover_color="#666666",
            width=120, height=36,
            command=win.destroy
        ).pack(side="bottom", pady=(0, 10))

        if sections:
            show_section(sections[0]["id"])