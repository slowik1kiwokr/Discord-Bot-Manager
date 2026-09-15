════════════════════════════════════════════════════════════════════
  DISCORD BOT MANAGER
  Modern Discord bot kezelő panel
════════════════════════════════════════════════════════════════════

  Verzió:      2.5.0
  Készítette:  slowik1kiwokr
  GitHub:      https://github.com/slowik1kiwokr/Discord-Bot-Manager
  Támogatás:   https://github.com/slowik1kiwokr/Discord-Bot-Manager/issues


────────────────────────────────────────────────────────────────────
  🇭🇺  MAGYAR
────────────────────────────────────────────────────────────────────

📌 MI EZ?
  A Discord Bot Manager egy modern, grafikus felületű panel,
  amivel Discord botokat kezelhetsz kényelmesen:

    • Bot indítás / leállítás / újraindítás egy kattintással
    • Élő naplók és statisztikák (CPU, RAM, uptime)
    • AI asszisztens (OpenAI, Claude, Ollama, LM Studio)
    • Broadcast — üzenet minden szerverre
    • Commander — egyedi parancsok kezelése
    • Plugin rendszer saját bővítményekhez
    • Automatikus biztonsági mentés
    • Havi riportok és grafikonok
    • Kétnyelvű felület (Magyar / English)

────────────────────────────────────────────────────────────────────
  ⚙️  RENDSZERKÖVETELMÉNYEK
────────────────────────────────────────────────────────────────────

  • Windows 10 vagy újabb
  • Python 3.10 vagy újabb (ajánlott: 3.11+)
  • Internet kapcsolat (frissítésekhez és AI funkciókhoz)

────────────────────────────────────────────────────────────────────
  📥  TELEPÍTÉS — LÉPÉSRŐL LÉPÉSRE
────────────────────────────────────────────────────────────────────

  ⚠️  FONTOS: NE futtasd a telepítőt közvetlenül a ZIP-ből!
      Előbb csomagold ki a fájlokat egy rendes mappába.

  ┌────────────────────────────────────────────────────────────────┐
  │  1. TÖLTSD LE a ZIP-et a GitHub-ról:                           │
  │     https://github.com/slowik1kiwokr/Discord-Bot-Manager       │
  │                                                                │
  │  2. CSOMAGOLD KI a ZIP-et egy mappába:                         │
  │     Jobb klikk → "Kibontás ide..." (vagy "Extract to...")      │
  │                                                                │
  │     Az eredmény:                                               │
  │       Discord-Bot-Manager-main\                                │
  │       ├── installer.pyw      ← ezt kell futtatni               │
  │       ├── DBM\               ← panel fájljai                   │
  │       └── README.txt                                           │
  │                                                                │
  │  3. FUTTASD az installer.pyw-t (dupla klikk).                  │
  │                                                                │
  │  4. VÁLASZD KI a telepítési helyet (alap: Documents).          │
  │                                                                │
  │  5. PIPA:                                                      │
  │     ☑  Asztali parancsikon                                     │
  │     ☐  Start menü parancsikon                                  │
  │     ☑  Panel indítása telepítés után                           │
  │     ☐  Forrásmappa törlése (ha már nem kell)                   │
  │                                                                │
  │  6. KATTINTS a "📥 Telepítés" gombra.                          │
  └────────────────────────────────────────────────────────────────┘

  Kész! A panel elindul, és legközelebb már az asztali
  parancsikonról is indítható.

────────────────────────────────────────────────────────────────────
  🚀  ELSŐ INDÍTÁS
────────────────────────────────────────────────────────────────────

  Az első indításkor a panel:

    1. Ellenőrzi a Python csomagokat (Függőségek ablak).
       Ha hiányzik valami, egy kattintással telepítheted.

    2. Bekéri az első botod adatait:
         • Bot fájl (.py) útvonala
         • Bot token
         • Név, verzió, prefix

    3. Ha új botot készítesz, a panel generál egy teljes
       sablont (bot.py + panel_integrity.py + version.py).

────────────────────────────────────────────────────────────────────
  🧩  ELSŐ BOT BEÁLLÍTÁSA
────────────────────────────────────────────────────────────────────

  1. Kattints a "📌 Alapok / Integráció" menüre.
  2. Válaszd: "✅ Van már botom" vagy "🆕 Új botot készítek".
  3. Ha új botot készítesz:
       • Tallózd be a célmappát
       • A panel legenerálja a 3 fájlt
       • Töltsd ki a BOT_TOKEN-t a "Bot adatai" ablakban
  4. Indítsd el a botot, és Discordban írd be:
       /connect panel_id:<a panel azonosítója>

────────────────────────────────────────────────────────────────────
  ❓  GYAKORI PROBLÉMÁK
────────────────────────────────────────────────────────────────────

  ─── "A forrásmappa üres!" hiba ─────────────────────────────────
      → A telepítőt a ZIP-en BELÜLről futtattad.
      → Csomagold ki rendesen (jobb klikk → Kibontás), és
        onnan indítsd újra az installer.pyw-t.

  ─── "Python not found" ─────────────────────────────────────────
      → Telepítsd a Python 3.10+-t: https://python.org
      → Telepítéskor pipáld be: ☑ "Add Python to PATH"

  ─── A panel nem indul el ───────────────────────────────────────
      → Nyisd meg a Beállítások → Függőségek ablakot, és
        telepítsd a hiányzó csomagokat.
      → Ha még mindig nem indul, nézd meg a %temp%\dbm_installer.log
        fájlt (ha van).

  ─── Nem jelenik meg a frissítés ablak ──────────────────────────
      → Ellenőrizd: Beállítások → GitHub frissítés → "Azonnali ellenőrzés".
      → Ha a verziószám megegyezik, nincs új verzió.

────────────────────────────────────────────────────────────────────
  💡  TIPPEK
────────────────────────────────────────────────────────────────────

  • Az AFK képernyő automatikusan megjelenik, ha nem használod
    a panelt — élő bot-állapotot mutat.
  • Nyomd meg az F2-t a gyorsgombok listájához.
  • Ctrl+1..9 — botváltás index alapján.
  • A pluginok a Documents\Discord Bot Manager\plugins\ mappában
    vannak — bármikor bővítheted őket.

────────────────────────────────────────────────────────────────────
  📜  LICENC
────────────────────────────────────────────────────────────────────

  Ez a projekt nyílt forráskódú. A részletekért lásd a
  GitHub oldalon található LICENSE fájlt.

  Kérlek, tartsd meg a készítő nevét (slowik1kiwokr) és a
  GitHub linket bármilyen terjesztés esetén.

────────────────────────────────────────────────────────────────────
  🙏  KÖSZÖNET
────────────────────────────────────────────────────────────────────

  Köszönjük, hogy a Discord Bot Manager-t választottad!
  Ha hasznosnak találod, adj egy ⭐-t a GitHub-on, és jelezd
  a hibákat / ötleteket az Issues oldalon.


════════════════════════════════════════════════════════════════════
  🇬🇧  ENGLISH
════════════════════════════════════════════════════════════════════

📌 WHAT IS THIS?
  Discord Bot Manager is a modern, graphical panel for
  managing Discord bots with ease:

    • Start / stop / restart bots with one click
    • Live logs and statistics (CPU, RAM, uptime)
    • AI assistant (OpenAI, Claude, Ollama, LM Studio)
    • Broadcast — send messages to all servers
    • Commander — manage custom commands
    • Plugin system for your own extensions
    • Automatic backups
    • Monthly reports and charts
    • Bilingual interface (Hungarian / English)

────────────────────────────────────────────────────────────────────
  ⚙️  SYSTEM REQUIREMENTS
────────────────────────────────────────────────────────────────────

  • Windows 10 or newer
  • Python 3.10 or newer (3.11+ recommended)
  • Internet connection (for updates and AI features)

────────────────────────────────────────────────────────────────────
  📥  INSTALLATION — STEP BY STEP
────────────────────────────────────────────────────────────────────

  ⚠️  IMPORTANT: Do NOT run the installer directly from the ZIP!
      First extract the files into a proper folder.

  ┌────────────────────────────────────────────────────────────────┐
  │  1. DOWNLOAD the ZIP from GitHub:                              │
  │     https://github.com/slowik1kiwokr/Discord-Bot-Manager       │
  │                                                                │
  │  2. EXTRACT the ZIP into a folder:                             │
  │     Right-click → "Extract All..."                             │
  │                                                                │
  │     Result:                                                    │
  │       Discord-Bot-Manager-main\                                │
  │       ├── installer.pyw      ← run this                        │
  │       ├── DBM\               ← panel files                     │
  │       └── README.txt                                           │
  │                                                                │
  │  3. RUN installer.pyw (double-click).                          │
  │                                                                │
  │  4. CHOOSE the install location (default: Documents).          │
  │                                                                │
  │  5. CHECK the options:                                         │
  │     ☑  Create desktop shortcut                                 │
  │     ☐  Create Start Menu shortcut                              │
  │     ☑  Launch panel after install                              │
  │     ☐  Delete source folder (if no longer needed)              │
  │                                                                │
  │  6. CLICK the "📥 Install" button.                             │
  └────────────────────────────────────────────────────────────────┘

  Done! The panel will launch, and from now on you can
  start it from the desktop shortcut.

────────────────────────────────────────────────────────────────────
  🚀  FIRST LAUNCH
────────────────────────────────────────────────────────────────────

  On first launch, the panel will:

    1. Check the Python packages (Dependencies window).
       If something is missing, you can install it with one click.

    2. Ask for your first bot's data:
         • Bot file (.py) path
         • Bot token
         • Name, version, prefix

    3. If you're creating a new bot, the panel generates a
       complete template (bot.py + panel_integrity.py + version.py).

────────────────────────────────────────────────────────────────────
  🧩  SETTING UP YOUR FIRST BOT
────────────────────────────────────────────────────────────────────

  1. Click the "📌 Basics / Integration" menu.
  2. Choose: "✅ I already have a bot" or "🆕 I'm creating a new bot".
  3. If creating a new bot:
       • Browse the target folder
       • The panel generates the 3 files
       • Fill in BOT_TOKEN in the "Bot info" window
  4. Start the bot and in Discord type:
       /connect panel_id:<your panel ID>

────────────────────────────────────────────────────────────────────
  ❓  COMMON ISSUES
────────────────────────────────────────────────────────────────────

  ─── "Source folder is empty!" error ────────────────────────────
      → You ran the installer from INSIDE the ZIP.
      → Extract the ZIP properly (right-click → Extract All),
        then run installer.pyw from there.

  ─── "Python not found" ─────────────────────────────────────────
      → Install Python 3.10+: https://python.org
      → During install, check: ☑ "Add Python to PATH"

  ─── The panel won't start ──────────────────────────────────────
      → Open Settings → Dependencies, and install missing packages.
      → If it still fails, check %temp%\dbm_installer.log

  ─── The update window doesn't appear ───────────────────────────
      → Check: Settings → GitHub update → "Check now".
      → If the version matches, there's no new version.

────────────────────────────────────────────────────────────────────
  💡  TIPS
────────────────────────────────────────────────────────────────────

  • The AFK screen appears automatically when the panel is idle —
    it shows the live bot status.
  • Press F2 for the list of hotkeys.
  • Ctrl+1..9 — switch bot by index.
  • Plugins are located in Documents\Discord Bot Manager\plugins\
    — you can extend them anytime.

────────────────────────────────────────────────────────────────────
  📜  LICENSE
────────────────────────────────────────────────────────────────────

  This project is open source. For details, see the LICENSE
  file on the GitHub page.

  Please keep the author's name (slowik1kiwokr) and the
  GitHub link in any redistribution.

────────────────────────────────────────────────────────────────────
  🙏  THANKS
────────────────────────────────────────────────────────────────────

  Thank you for choosing Discord Bot Manager!
  If you find it useful, give it a ⭐ on GitHub, and report
  bugs / ideas on the Issues page.


════════════════════════════════════════════════════════════════════
  Made with ❤️  by slowik1kiwokr
  https://github.com/slowik1kiwokr/Discord-Bot-Manager
════════════════════════════════════════════════════════════════════