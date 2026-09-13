import webbrowser

import customtkinter as ctk

from modules.languages import LANGUAGES


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
1. Indítsd el a panel.pyw-t (dupla kattintás vagy `py panel.pyw`)
2. Megjelenik a Splash képernyő — várj 3 másodpercet
3. Ha jelszót állítottál be, be kell írnod
4. Megnyílik a főablak

## Alap felépítés
A panel három részre oszlik:

Bal oldal — Színes kártyák (kategóriák)
  🎮 Vezérlés      — Start, Restart, Stop
  ⚡ Tömeges       — Összes indítása/leállítása
  🔌 Integráció    — Commander, Pluginok, Megjelenés
  📊 Statisztika   — Dashboard, riportok, backupok
  ⚙️ Rendszer      — Beállítások, Tutorial, GitHub
  🤖 AI és extrák  — AI funkciók, achievementek

Középső rész — Élő naplók
  • A futó botok üzenetei valós időben
  • Szűrők: ALL / ERRORS / SUCCESS / EVENTS
  • Keresés a naplókban

Jobb oldal — Pro metrikák
  • Bot neve, verziója, uptime
  • RAM, CPU, hőmérséklet
  • Szerverek, felhasználók, hibák

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
3. A bal oldali státusz zöldre vált
4. Az Élő naplók elkezdenek görögni

## Bot leállítása
1. Kattints a Stop gombra
2. A bot folyamat leáll, a státusz piros lesz

## Újraindítás
1. Kattints a Restart gombra
2. A panel leállítja, majd 1,5 másodperc múlva újraindítja

## Több bot kezelése
Fülek
  • Minden bot külön fülön jelenik meg
  • Az emoji és a szín a bot személyiségét mutatja
  • Kattints rájuk a váltáshoz

Jobb klikk egy fülre
  • Átnevezés
  • Törlés (csak ha nem az első bot)

Új bot hozzáadása
  • Kattints a + gombra a fülek mellett

## Bot megjelenés testreszabása
  • Sidebar → 🎨 Megjelenés
  • Válassz emojit (24 db)
  • Válassz színt (12 szín + egyéni hex)
  • Élő előnézet
  • 💾 Mentés

A szín a fülre és a bal oldali státuszjelzőre is hat.

## Tömeges vezérlés (Bulk Control)
A bal oldali menüben:
  • Összes indítása — összes bot indítása
  • Összes újraindítása — összes bot újraindítása
  • Összes leállítása — összes bot leállítása

## Automatikus újraindítás
A bot beállításainál (fő panel, középső rész):
  • Auto-indítás — a panel indulásakor automatikusan elindul
  • Auto Restart — időzített újraindítás (nap/óra/perc)
  • Midnight Restart — éjfélkor újraindul

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
Bal oldali menü → ⚙️ Beállítások

## Panel Settings fül

Panel azonosító
  • Egyedi azonosító, amivel a bot kapcsolódik
  • Használd a 📋 Parancs másolása gombot

Panel jelszó
  • Üresen hagyva: nincs védelem
  • Kitöltve: a panel induláskor kéri a jelszót

Nyelv
  • English / Magyar (az egész panel átvált)

Kicsinyítés tálcára
  • Ha be van kapcsolva, X-re a tálcára kerül
  • Jobb klikk a tálcaikonra → megnyitás

Discord Rich Presence
  • Discord profilodon megjelenik, hogy a panelt használod

Napló mentési szint
  • Mindent mentse
  • Csak hibák
  • Csak események
  • Sikeres interakciók

Hiba hang
  • Válassz hangot a legördülőből (8 hang)
  • A 🔊 Teszt hang gombbal meghallgathatod

Automatikus biztonsági mentés
  • Be/ki kapcsolható
  • Panel indulásakor azonnal
  • Időzített (pl. 24 óránként)

## Bot Settings fül

Maximum RAM használat
  • Ha a bot túllépi, a panel figyelmeztet
  • Opcionálisan automatikusan leállítja

Teszt mód
  • Csak a megadott Discord ID-k használhatják a botot

Tesztelők Discord ID-i
  • Vesszővel elválasztva
  • Pl.: 123456789012345678, 987654321098765432

Auto-Restart on Crash
  • Ha a bot összeomlik, automatikusan újraindul
  • Állítsd be a várakozási időt másodpercben

## 🤖 AI beállítások

Provider
  • OpenAI (GPT) — fizetős, de profi
  • Anthropic (Claude) — fizetős
  • Ollama (helyi) — INGYENES, a gépeden fut
  • LM Studio (helyi) — INGYENES

API kulcs
  • Csak OpenAI/Claude esetén kell
  • Ollama/LM Studio esetén üresen hagyható

Modell
  • Pl. gpt-4o-mini, llama3.2
  • Hagyd üresen az alapértelmezettnek
""",
        },
        {
            "id": "commander",
            "title": "⚡ Commander",
            "content": """# ⚡ Commander — Dinamikus parancsok

## Mi ez?
A Commanderrel kód írása nélkül hozhatsz létre Discord
parancsokat. Sima szöveges üzenet vagy szép embed formában.

## Használat
1. Bal oldali menü → ⚡ Commander
2. Kattints az ➕ Új parancs gombra
3. Válassz sablont a legördülőből
4. Töltsd ki a mezőket
5. 💾 Mentés

## Elérhető sablonok (8 db)

Szöveges üzenetek
  • Egyszerű szöveges üzenet
  • Üdvözlő szöveges üzenet

Embed üzenetek
  • Egyszerű embed (blurple)
  • Színes értesítő embed (narancs)
  • Hiba embed (piros)
  • Siker embed (zöld)
  • Segítség embed (több mezővel)

## Parancs beállításai

Név
  • Per jel nélkül (pl. parancs1 → /parancs1)
  • Csak betű, szám, alulvonás

Leírás
  • Megjelenik a Discord / menüben

Típus
  • Üzenet: sima szöveg
  • Embed: színes, formázott üzenet

Embed szín
  • Hex kód (pl. #5865F2)
  • 7 gyors gomb (Blurple, Zöld, Piros...)

Ephemeral
  • Csak a hívónak látszik (nem látszik másoknak)

Engedélyezve
  • Kikapcsolva: a bot nem tölti be

## Commander.py a botba
1. Kattints a 📤 Commander.py a botba gombra
2. A panel legenerálja a bot mappájába
3. A bot bot.py-jában legyen benne:
   await bot.load_extension("Commander")
4. Indítsd újra a botot

## Discord parancsok frissítése
A Discord 1 óránként frissíti a slash parancsokat.
Ha azonnal akarod:
  • Fejlesztői szerveren: /commander_reload
  • Vagy indítsd újra a botot
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
Bal oldali menü → 🧩 Pluginok

Bal oldal — a meglévő pluginok listája
Jobb oldal — a kiválasztott plugin kódja

## Új plugin létrehozása
1. Kattints az ➕ Új plugin gombra
2. Adj neki fájlnevet (pl. sajat_plugin.py)
3. Válassz sablont
4. Létrehozás

## Elérhető sablonok (14 db)

• Üres plugin
• Esemény loggoló
• Egyedi gomb a sidebar-hoz
• Egyedi ablak megnyitó gomb
• Üdvözlő üzenet a naplóban
• Bot állapot figyelő
• Hangjelzés hibánál
• Egyszerű számológép ablak
• Időjárás lekérdező (API példa)
• Téma váltó gombok
• Backup rotáció
• Discord webhook értesítés

## Plugin szerkesztése
1. Válaszd ki a bal oldali listából
2. Szerkeszd a jobb oldali szerkesztőben
3. 💾 Mentés — szintaktikai ellenőrzéssel

## Plugin törlése
1. Válaszd ki
2. 🗑️ Törlés

## Plugin újratöltése
Ha módosítottál egy plugint, a 🔄 Újratöltés gombbal
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
  • Az összes bot beállítását (bots.json)
  • A panel beállításait (settings.json)
  • A botok adatait (data/, .db, .json)

## Backup ablak
Bal oldali menü → 💾 Biztonsági mentések

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
  • Be/ki kapcsolható

Mentés panelindításkor
  • Induláskor azonnal készít egyet

Időzített mentés gyakorisága
  • Órában (pl. 24 = naponta)
  • 0 = kikapcsolva

## Mit tartalmaz a mentés?
  • bots.json — botok beállításai
  • settings.json — panel beállítások
  • bots/<bot_nev>/ — minden bot adata
  • .db, .sqlite — adatbázisok
  • data/ mappa — szerver adatok
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
  • Jelenlegi verzió → Új verzió

Changelog
  • A fejlesztő által írt változások listája

3 gomb:
  • ✅ Frissítés letöltése — letölti és telepíti
  • ⏰ Később — bezárja, 1 óra múlva újra jelzi
  • ❌ Kihagyás — nem jelzi, amíg újra nem indítod

## Letöltés folyamata
1. 📥 ZIP letöltése a GitHub-ról
2. 📦 Kicsomagolás
3. 🛑 Futó botok leállítása
4. 💾 Fájlok frissítése
5. 🏷️ Verziószám frissítése

## Védett fájlok
Ezek soha nem íródnak felül:
  • bots.json — botjaid beállításai
  • settings.json — panel beállítások
  • backups/ — mentések
  • plugins/ — pluginjaid
  • logs/ — naplók
  • Saját ikonok
  • panel_stats.json, achievements.json, streak.json

## Újraindítás
A letöltés után a panel kérdezi:
  • 🔄 Újraindítás most — bezárja és újraindítja
  • 🚪 Kilépés — bezárja, te indítod újra

## Manuális ellenőrzés
Bal oldali menü → 🔄 GitHub Frissítés
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
  • Bot neve, verziója
  • Uptime (munkamenet) — mióta fut
  • Heti uptime — összesített futási idő
  • Ping válaszidők (API / Msg)
  • Összes parancs

PC erőforrások
  • RAM használat
  • CPU használat
  • PC hőmérséklet (ha elérhető)
  • Szerverek (guilds) száma
  • Elért felhasználók
  • Hibák számlálója

## Statikus teljesítmény grafikon
Kattints a 📈 Teljesítmény grafikon gombra:

Időtáv választó
  • Utolsó 10 perc
  • Utolsó 1 óra
  • Utolsó 24 óra

Grafikonok
  • RAM használat (kék vonal)
  • CPU használat (zöld vonal)

Export
  • 💾 PNG mentése gombbal elmented a képet

## 📈 Élő animált grafikonok
Kattints a 📈 Élő grafikonok gombra:

  • Valós idejű animáció (másodpercenként frissül)
  • 🖱️ Hover → az érték megjelenik
  • 🔍 Görgess zoom-hoz
  • ✋ Húzd a pan-hez
  • Toolbar az alján (mentés, visszaállítás)

## 📐 Dashboard widgetek
Kattints a 📐 Dashboard gombra:

  • Kártyákban rendezve
  • Testreszabható (⚙️ Widgetek gomb)
  • Követett értékek:
    - Uptime, CPU, RAM, aktív botok, hibák
    - Parancsok, hőmérséklet, szerverek, felhasználók
  • Pipáld be, melyek jelenjenek meg

## 📅 Havi riport
Bal oldali menü → 📅 Havi riport

  • Elmúlt 12 hónap
  • Összesítő kártyák: hibák, parancsok, naplók, uptime
  • Botonkénti bontás
  • Top parancsok (Top 10)
  • Napi aktivitás diagram
  • 📤 Export JSON / 📄 Export szöveg

## 📊 Panel statisztika
Bal oldali menü → 📊 Panel statisztika

  • Hányszor nyitottad meg a panelt
  • Összes használati idő
  • Ez a session hossza
  • Első / utolsó megnyitás
  • 🔥 Legtöbbet használt funkciók (top lista)

## Naplók szűrése
A középső részen:

Szűrő gombok
  • ALL — összes napló
  • ERRORS — csak hibák (piros)
  • SUCCESS — csak sikerek (zöld)
  • EVENTS — csak események (lila)

Keresés
  • Írj be szöveget a keresőbe
  • Azonnal szűri a naplókat

Automatikus görgetés
  • Pipáld be — mindig a legfrissebb sorra ugrik
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
Bal oldali menü → 📌 Alapok / Integráció

## 4 fül

1. bot.py sablon
  • Kész bot.py kód, amit másolhatsz
  • Tartalmazza a Panel extension betöltést
  • Parancsok: /teszt, /parancsok

2. Panel.py kód
  • A Panel.py extension kódja
  • Ez teszi lehetővé a /connect parancsot
  • A bot statisztikáit a panelnek küldi

3. Tutorial
  • Lépésről lépésre útmutató

4. 🔧 Függőségek (ÚJ)
  • Megmutatja, melyik Python csomag van telepítve
  • ✅ Zöld pipa = telepítve
  • ❌ Piros X = hiányzik
  • ⚠️ Sárga = opcionális, hiányzik
  • Egy kattintással telepíthetők a hiányzók
  • 📋 Requirements.txt mentése

## Bot összekötése a panellel

1. lépés: Bot fájl kiválasztása
  • A fő panelen tallózd be a bot .py fájlját

2. lépés: Panel.py mentése
  • Kattints a 🔌 Panel.py összekötése gombra
  • A panel létrehozza a bot mappájában

3. lépés: bot.py módosítása
  • Nyisd meg a bot.py-t
  • Az on_ready() függvénybe írd:
    await bot.load_extension("Panel")

4. lépés: Bot újraindítás
  • A panelen indítsd újra a botot

5. lépés: /connect parancs
  • A panelen kattints a 📋 Parancs másolása gombra
  • Discordban írd be a másolt parancsot
  • Pl.: /connect panel_id:#ABC123 device:PC

6. lépés: Kész!
  • A bot most már a panelről vezérelhető
  • Discordból is: /start, /stop, /restart, /broadcast

## Elérhető Discord parancsok

Vezérlés (panelről)
  • /connect — kapcsolódás a panelhez
  • /start — bot indítása
  • /stop — bot leállítása
  • /restart — bot újraindítása
  • /status — bot állapota
  • /info — panel információ
  • /log — utolsó naplóbejegyzések
  • /stressz — rendszer-erőforrás ellenőrzés

Üzenetküldés
  • /broadcast — üzenet az összes szerverre

Kilépés
  • /kilepes — bot kilép egy szerverből

## Panel azonosító
Minden panelnek van egy egyedi azonosítója:
  • Formátum: #XXXXXXXX
  • A bal oldali menüben látható
  • Ezzel tud a bot kapcsolódni

## Bot verzió és token
A bot mappájában lévő version.py:
  • BOT_NAME — bot neve
  • BOT_VERSION — verziószám
  • BOT_TOKEN — Discord token

FIGYELEM: A tokent tartsd titokban!
""",
        },
        {
            "id": "ai_features",
            "title": "🤖 AI funkciók",
            "content": """# 🤖 AI funkciók

## Mi ez?
A panel 4 AI funkciót tartalmaz. Az AI **helyben fut**
(Ollama/LM Studio) vagy felhőben (OpenAI/Claude).

## ⚙️ AI beállítás
Settings ablak → 🤖 AI beállítások

Provider
  • OpenAI (GPT) — fizetős, profi
  • Anthropic (Claude) — fizetős
  • Ollama (helyi) — INGYENES, ajánlott
  • LM Studio (helyi) — INGYENES

Ollama telepítés (ingyenes, helyi AI):
  1. Töltsd le: ollama.com/download
  2. Telepítés után PowerShell-ben:
     ollama pull llama3.2
  3. Panelben: Provider = Ollama (helyi), Model = llama3.2
  4. Kész!

## 1. 🤖 AI Asszisztens
Bal oldali menü → 🤖 AI Asszisztens

Chat ablak, ahol kérdezhetsz:
  • „Hogyan készítsek backupot?"
  • „Miért crash-elt a botom?"
  • „Adj tanácsot a kódról."

A jobb felső sarokban látod, melyik providert használja.

## 2. ✨ AI Kód Generátor
Bal oldali menü → ✨ AI Kód Generátor

Leírás → Python kód:
  • „Csinálj egy /üdv parancsot"
  • „Készíts egy embed üzenetet"
  • „Írj egy moderációs parancsot"

A panel generálja a kódot, amit:
  • 💾 Elmenthetsz a bot mappájába
  • Vagy kimásolhatsz

## 3. 🔍 AI Hibaelemzés
Ha a bot crash-el, az AI elemzi a stack trace-t:
  • Megmondja a kiváltó okot
  • Javasol javítást
  • Kód példát ad

## 4. 📄 AI Dokumentáció
Egy Python fájlból Markdown dokumentációt készít:
  • Fájl célja
  • Függvények listája leírással
  • Használati példák

Használat:
  • Sidebar → 📄 AI Dokumentáció
  • Válassz egy .py fájlt
  • Az AI legenerálja a dokumentációt
  • 💾 Mentés Markdown fájlba

## 💡 Tipp
Az Ollama az első indításkor **10-30 másodpercig** is
eltarthat, mert a modellt betölti a memóriába.
Utána már gyors (2-5 másodperc).
""",
        },
        {
            "id": "achievements",
            "title": "🏆 Achievementek",
            "content": """# 🏆 Achievementek és Streak

## Achievement rendszer
Bal oldali menü → 🏆 Achievementek

15 teljesítmény, amit feloldhatsz:

🥇 Első lépés        — Elindítottál egy botot
💾 Biztonságos       — Készítettél egy backupot
🧩 Bővítő            — Létrehoztál egy plugint
⚡ Parancsnok        — Létrehoztál egy Commander parancsot
🤖 Sokaság           — 3 botot regisztráltál
🎯 Flotta            — 5 botot regisztráltál
🚀 Armada            — 10 botot regisztráltál
⏱️ Kitartó           — Egy bot 1 órán át futott
⏳ Hosszútávfutó     — Egy bot 10 órán át futott
🏆 Maratonista       — Egy bot 100 órán át futott
🗄️ Gyűjtögető        — 10 backupot készítettél
✨ Hibátlan nap      — Egy napig nem volt hiba
🎨 Művész            — Beállítottad egy bot emoji-ját/színét
⌨️ Gyorsujjú         — Használtál egy gyorsgombot
🌗 Változatos        — Váltottál témát

## Hogyan működik?
  • Automatikus — nem kell csinálnod semmit
  • Amikor eléred, felugrik egy toast értesítés
  • A 🏆 Achievementek ablakban látod az összeset
  • Zöld pipa = feloldva
  • 🔒 = még nem érted el

## 🔥 Napi streak
  • Automatikusan számolja, hány napja nyitod meg a panelt
  • Toast értesítés minden nap
  • Különleges üzenet 3, 7, 14, 30, 60, 100, 365 napnál
  • A legjobb streak-et is tárolja
  • Látható a sidebar-on (ha be van kapcsolva)

## Adatok tárolása
  • achievements.json — feloldott achievementek
  • streak.json — streak adatok

⚠️ Ezek a fájlok a te személyes adataid, nem kerülnek
fel a GitHubra (a .gitignore védi őket).
""",
        },
        {
            "id": "hotkeys",
            "title": "⌨️ Gyorsgombok",
            "content": """# ⌨️ Gyorsgombok és tippek

## Billentyűparancsok

Fő ablak
  • Ctrl + S — Beállítások mentése
  • Ctrl + B — Biztonsági mentés készítése
  • Ctrl + R — Összes bot újraindítása
  • Ctrl + F — Keresés a naplókban
  • Ctrl + L — Naplók törlése
  • Ctrl + T — Tutorial megnyitása
  • Ctrl + , — Beállítások megnyitása
  • Ctrl + W — Panel bezárása

Botváltás
  • Ctrl + 1 … Ctrl + 9 — Bot kiválasztása index alapján
  • Ctrl + Tab — Következő bot (ha támogatott)

Súgó
  • F1 — Tutorial
  • F2 — Gyorsgombok listája
  • F5 — Statisztikák frissítése

## Tippek

Több bot kezelése
  • Használj beszédes neveket (pl. ZeneBot, ModBot)
  • Állíts be emojit és színt minden botnak
  • Csoportosítsd a fülek sorrendjét (balról jobbra fontosság)

Gyorsabb munka
  • Állítsd be az Auto-indítás-t a gyakran használt botoknál
  • Használd a Bulk Control gombokat, ha mind induljon
  • Kapcsold be az automatikus backup-ot (napi)
  • Használd a hotkey-eket (Ctrl+S, Ctrl+B, Ctrl+R)

Hibakeresés
  • Ha a bot leáll, nézd meg a naplót ERROR szűrővel
  • A stressz parancs megmutatja az aktuális CPU/RAM-ot
  • Használd a Crash Watchdog-ot (Settings → Bot Settings)
  • Kérdezd meg az AI Asszisztenst (🤖)

Biztonság
  • Készíts backup-ot minden nagyobb változtatás előtt
  • Tartsd a panel jelszót, ha publikus gépen használod
  • A Discord tokent soha ne oszd meg

Testreszabás
  • Settings → Discord téma (4 beépített)
  • Settings → Hiba hang (8 választható)
  • 🎨 Megjelenés — bot emoji + szín
  • Pluginokkal tovább bővíthető

## Hibaelhárítás

A bot nem indul
  • Ellenőrizd, hogy a .py fájl létezik
  • Nézd meg a naplókat (ERROR szűrő)
  • Próbáld manuálisan: py bot.py a bot mappájában

A panel nem érzékeli a botot
  • Ellenőrizd, hogy a /connect parancsot használtad
  • Nézd meg, hogy a panel ID egyezik
  • Bot újraindítás segíthet

A Commander parancsok nem jelennek meg
  • Discord 1 óránként frissíti a slash parancsokat
  • Vagy: /commander_reload fejlesztői szerveren
  • Vagy: bot újraindítás

Az AI nem válaszol
  • Settings → AI provider helyes?
  • Ha Ollama: `ollama list` mutassa a modellt
  • Ha OpenAI: van-e érvényes API kulcs?
  • Próbáld kisebb modellt: `ollama pull llama3.2:1b`

Nem jelenik meg a hőmérséklet
  • A Windows gyakran nem adja ki WMI-n
  • Telepítsd a LibreHardwareMonitor-t
  • Vagy hagyd figyelmen kívül (CPU % mutatja a terhelést)
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
1. Launch panel.pyw (double-click or `py panel.pyw`)
2. The Splash screen appears — wait 3 seconds
3. If you set a password, enter it
4. The main window opens

## Basic layout
The panel is divided into three parts:

Left side — Colored cards (categories)
  🎮 Control      — Start, Restart, Stop
  ⚡ Bulk         — Start/Stop all
  🔌 Integration  — Commander, Plugins, Appearance
  📊 Statistics   — Dashboard, reports, backups
  ⚙️ System       — Settings, Tutorial, GitHub
  🤖 AI & extras  — AI features, achievements

Middle part — Live logs
  • Running bots' messages in real time
  • Filters: ALL / ERRORS / SUCCESS / EVENTS
  • Search in logs

Right side — Pro metrics
  • Bot name, version, uptime
  • RAM, CPU, temperature
  • Servers, users, errors

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
3. The left status turns green
4. Live logs start scrolling

## Stopping a bot
1. Click the Stop button
2. The bot process stops, status turns red

## Restarting
1. Click the Restart button
2. The panel stops it, then restarts after 1.5 seconds

## Managing multiple bots
Tabs
  • Each bot appears on a separate tab
  • The emoji and color show the bot's personality
  • Click them to switch

Right-click on a tab
  • Rename
  • Delete (only if not the first bot)

Adding a new bot
  • Click the + button next to the tabs

## Customizing bot appearance
  • Sidebar → 🎨 Appearance
  • Pick an emoji (24 options)
  • Pick a color (12 colors + custom hex)
  • Live preview
  • 💾 Save

The color affects both the tab and the left status indicator.

## Bulk Control
In the left menu:
  • Start All — start all bots
  • Restart All — restart all bots
  • Stop All — stop all bots

## Automatic restart
In the bot settings (main panel, middle section):
  • Auto-start — starts automatically when panel launches
  • Auto Restart — scheduled restart (day/hour/minute)
  • Midnight Restart — restarts at midnight

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
Left menu → ⚙️ Settings

## Panel Settings tab

Panel ID
  • Unique identifier the bot connects with
  • Use the 📋 Copy command button

Panel password
  • Empty: no protection
  • Filled: the panel asks for the password on launch

Language
  • English / Magyar (whole panel switches)

Minimize to tray
  • If enabled, X sends it to the system tray
  • Right-click the tray icon → open

Discord Rich Presence
  • Shows on your Discord profile that you use the panel

Log save level
  • Save everything
  • Only errors
  • Only events
  • Successful interactions

Error sound
  • Choose a sound from the dropdown (8 options)
  • Use the 🔊 Test sound button to preview

Automatic backup
  • On/off toggle
  • On panel startup
  • Scheduled (e.g. every 24 hours)

## Bot Settings tab

Maximum RAM usage
  • If the bot exceeds it, the panel warns
  • Optionally auto-terminates

Test mode
  • Only specified Discord IDs can use the bot

Tester Discord IDs
  • Comma-separated

Auto-Restart on Crash
  • If the bot crashes, it restarts automatically
  • Set the wait time in seconds

## 🤖 AI settings

Provider
  • OpenAI (GPT) — paid, professional
  • Anthropic (Claude) — paid
  • Ollama (local) — FREE, runs on your PC
  • LM Studio (local) — FREE

API key
  • Only needed for OpenAI/Claude
  • Leave empty for Ollama/LM Studio

Model
  • E.g. gpt-4o-mini, llama3.2
  • Leave empty for default
""",
        },
        {
            "id": "commander",
            "title": "⚡ Commander",
            "content": """# ⚡ Commander — Dynamic commands

## What is it?
Commander lets you create Discord commands without writing
any code. As plain text messages or beautiful embeds.

## Usage
1. Left menu → ⚡ Commander
2. Click the ➕ New command button
3. Choose a template from the dropdown
4. Fill in the fields
5. 💾 Save

## Available templates (8)

Text messages
  • Simple text message
  • Welcome text message

Embed messages
  • Simple embed (blurple)
  • Colorful notification embed (orange)
  • Error embed (red)
  • Success embed (green)
  • Help embed (multiple fields)

## Command settings

Name
  • Without slash (e.g. command1 → /command1)
  • Letters, numbers, underscore only

Description
  • Appears in the Discord / menu

Type
  • Message: plain text
  • Embed: colored, formatted message

Embed color
  • Hex code (e.g. #5865F2)
  • 7 quick buttons

Ephemeral
  • Only visible to the caller

Enabled
  • Disabled: the bot doesn't load it

## Commander.py to the bot
1. Click the 📤 Commander.py to bot button
2. The panel generates it in the bot folder
3. In the bot's bot.py, add:
   await bot.load_extension("Commander")
4. Restart the bot

## Refreshing Discord commands
Discord refreshes slash commands every hour.
To refresh immediately:
  • On a dev server: /commander_reload
  • Or restart the bot
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
Left menu → 🧩 Plugins

Left side — list of existing plugins
Right side — code of the selected plugin

## Creating a new plugin
1. Click the ➕ New plugin button
2. Give it a filename (e.g. my_plugin.py)
3. Choose a template
4. Create

## Available templates (14)

• Empty plugin
• Event logger
• Custom sidebar button
• Custom window button
• Welcome message in log
• Bot status watcher
• Sound alert on error
• Simple calculator window
• Weather query (API example)
• Theme switcher buttons
• Backup rotation
• Discord webhook notification

## Editing a plugin
1. Select it from the left list
2. Edit it in the right editor
3. 💾 Save — with syntax check

## Deleting a plugin
1. Select it
2. 🗑️ Delete

## Reloading plugins
If you modified a plugin, the 🔄 Reload button applies
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
  • All bot settings (bots.json)
  • Panel settings (settings.json)
  • Bot data (data/, .db, .json)

## Backup window
Left menu → 💾 Backups

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
  • On/off toggle

Backup on panel startup
  • Creates one immediately on launch

Scheduled backup interval
  • In hours (e.g. 24 = daily)
  • 0 = disabled

## What does the backup contain?
  • bots.json — bot settings
  • settings.json — panel settings
  • bots/<bot_name>/ — each bot's data
  • .db, .sqlite — databases
  • data/ folder — server data
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
  • Current version → New version

Changelog
  • List of changes written by the developer

3 buttons:
  • ✅ Download update — downloads and installs
  • ⏰ Later — closes, re-checks after 1 hour
  • ❌ Skip — won't show until you restart

## Download process
1. 📥 Download ZIP from GitHub
2. 📦 Extract
3. 🛑 Stop running bots
4. 💾 Update files
5. 🏷️ Update version number

## Protected files
These are never overwritten:
  • bots.json
  • settings.json
  • backups/
  • plugins/
  • logs/
  • Custom icons
  • panel_stats.json, achievements.json, streak.json

## Restart
After download, the panel asks:
  • 🔄 Restart now — closes and restarts
  • 🚪 Exit — closes, you restart manually

## Manual check
Left menu → 🔄 GitHub Update
Always shows whether there's a new version.
""",
        },
        {
            "id": "statistics",
            "title": "📊 Statistics",
            "content": """# 📊 Statistics

## Pro metrics (right side)
Visible on the right side of the main window:

Bot information
  • Bot name, version
  • Uptime (session)
  • Weekly uptime
  • Ping response times (API / Msg)
  • Total commands

PC resources
  • RAM usage
  • CPU usage
  • PC temperature (if available)
  • Server (guild) count
  • Users reached
  • Error counter

## Static performance chart
Click the 📈 Performance chart button:

Time range selector
  • Last 10 minutes
  • Last 1 hour
  • Last 24 hours

Charts
  • RAM usage (blue line)
  • CPU usage (green line)

Export
  • 💾 Save PNG button

## 📈 Live animated charts
Click the 📈 Live charts button:

  • Real-time animation
  • 🖱️ Hover → shows value
  • 🔍 Scroll to zoom
  • ✋ Drag to pan
  • Toolbar at the bottom

## 📐 Dashboard widgets
Click the 📐 Dashboard button:

  • Widgets in cards
  • Customizable (⚙️ Widgets button)
  • Metrics: Uptime, CPU, RAM, active bots, errors, etc.
  • Toggle which widgets are visible

## 📅 Monthly report
Left menu → 📅 Monthly report

  • Last 12 months
  • Summary cards: errors, commands, logs, uptime
  • Per-bot breakdown
  • Top commands (Top 10)
  • Daily activity
  • 📤 Export JSON / 📄 Export text

## 📊 Panel statistics
Left menu → 📊 Panel stats

  • How many times you opened the panel
  • Total usage time
  • Current session length
  • First / last opened
  • 🔥 Most used features (top list)

## Log filtering
In the middle part:

Filter buttons
  • ALL — all logs
  • ERRORS — errors only (red)
  • SUCCESS — successes only (green)
  • EVENTS — events only (purple)

Search
  • Type text in the search box
  • Filters logs instantly
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
Left menu → 📌 Basics / Integration

## 4 tabs

1. bot.py template
  • Ready-made bot.py code you can copy
  • Contains the Panel extension loading
  • Commands: /test, /commands

2. Panel.py code
  • The Panel.py extension code
  • Enables the /connect command
  • Sends bot statistics to the panel

3. Tutorial
  • Step-by-step guide

4. 🔧 Dependencies (NEW)
  • Shows which Python packages are installed
  • ✅ Green check = installed
  • ❌ Red X = missing
  • ⚠️ Yellow = optional, missing
  • Install missing packages with one click
  • 📋 Save requirements.txt

## Connecting your bot to the panel

Step 1: Select bot file
  • Browse your bot's .py file in the main panel

Step 2: Save Panel.py
  • Click the 🔌 Connect Panel.py button
  • The panel creates it in the bot folder

Step 3: Modify bot.py
  • Open bot.py
  • In the on_ready() function add:
    await bot.load_extension("Panel")

Step 4: Restart bot
  • Restart the bot from the panel

Step 5: /connect command
  • Click 📋 Copy command on the panel
  • Paste it in Discord

Step 6: Done!
  • The bot is now controllable from the panel

## Available Discord commands

Control (from panel)
  • /connect, /start, /stop, /restart
  • /status, /info, /log, /stress

Messaging
  • /broadcast — message to all servers

Leave
  • /kilepes — bot leaves a server

## Panel ID
Every panel has a unique identifier:
  • Format: #XXXXXXXX
  • Visible in the left menu

## Bot version and token
The version.py file in the bot folder:
  • BOT_NAME, BOT_VERSION, BOT_TOKEN

WARNING: Keep the token secret!
""",
        },
        {
            "id": "ai_features",
            "title": "🤖 AI Features",
            "content": """# 🤖 AI Features

## What is it?
The panel has 4 AI features. The AI runs **locally**
(Ollama/LM Studio) or in the cloud (OpenAI/Claude).

## ⚙️ AI Settings
Settings window → 🤖 AI settings

Provider
  • OpenAI (GPT) — paid, professional
  • Anthropic (Claude) — paid
  • Ollama (local) — FREE, recommended
  • LM Studio (local) — FREE

Ollama installation (free, local AI):
  1. Download: ollama.com/download
  2. After install, in PowerShell:
     ollama pull llama3.2
  3. In panel: Provider = Ollama, Model = llama3.2
  4. Done!

## 1. 🤖 AI Assistant
Left menu → 🤖 AI Assistant

Chat window where you can ask:
  • "How do I make a backup?"
  • "Why did my bot crash?"
  • "Give me advice on my code."

The top-right corner shows which provider is active.

## 2. ✨ AI Code Generator
Left menu → ✨ AI Code Generator

Description → Python code:
  • "Create a /hello command"
  • "Make an embed message"
  • "Write a moderation command"

Save the generated code to the bot folder.

## 3. 🔍 AI Error Analysis
If the bot crashes, AI analyzes the stack trace:
  • Identifies root cause
  • Suggests fixes
  • Provides code examples

## 4. 📄 AI Documentation
Generates Markdown docs from a Python file:
  • File purpose
  • Functions list with descriptions
  • Usage examples

Usage:
  • Sidebar → 📄 AI Documentation
  • Pick a .py file
  • AI generates the docs
  • 💾 Save to Markdown

## 💡 Tip
Ollama may take **10-30 seconds** on the first request
while it loads the model into memory.
After that it's fast (2-5 seconds).
""",
        },
        {
            "id": "achievements",
            "title": "🏆 Achievements",
            "content": """# 🏆 Achievements and Streak

## Achievement system
Left menu → 🏆 Achievements

15 achievements to unlock:

🥇 First step       — Started a bot
💾 Secure           — Made a backup
🧩 Extender         — Created a plugin
⚡ Commander        — Created a Commander command
🤖 Multitude        — Registered 3 bots
🎯 Fleet            — Registered 5 bots
🚀 Armada           — Registered 10 bots
⏱️ Persistent       — A bot ran for 1 hour
⏳ Long-runner      — A bot ran for 10 hours
🏆 Marathoner       — A bot ran for 100 hours
🗄️ Collector        — Made 10 backups
✨ Flawless day     — No errors for a day
🎨 Artist           — Set bot emoji/color
⌨️ Quick-fingered   — Used a hotkey
🌗 Versatile        — Switched theme

## How it works
  • Automatic — no action needed
  • Toast notification on unlock
  • View all in the 🏆 Achievements window
  • Green check = unlocked

## 🔥 Daily streak
  • Tracks how many days you've opened the panel
  • Toast on every day
  • Special message at 3, 7, 14, 30, 60, 100, 365 days
  • Best streak is stored

## Data storage
  • achievements.json, streak.json

⚠️ These are your personal data, not uploaded to GitHub.
""",
        },
        {
            "id": "hotkeys",
            "title": "⌨️ Hotkeys",
            "content": """# ⌨️ Hotkeys and tips

## Keyboard shortcuts

Main window
  • Ctrl + S — Save settings
  • Ctrl + B — Create backup
  • Ctrl + R — Restart all bots
  • Ctrl + F — Search in logs
  • Ctrl + L — Clear logs
  • Ctrl + T — Open tutorial
  • Ctrl + , — Open settings
  • Ctrl + W — Close panel

Bot switching
  • Ctrl + 1 … Ctrl + 9 — Select bot by index

Help
  • F1 — Tutorial
  • F2 — Hotkeys list
  • F5 — Refresh statistics

## Tips

Managing multiple bots
  • Use descriptive names (e.g. MusicBot, ModBot)
  • Set emoji and color for each bot
  • Order tabs by importance

Faster workflow
  • Enable Auto-start for frequently used bots
  • Use Bulk Control buttons
  • Turn on automatic backup
  • Use hotkeys

Debugging
  • Check log with ERROR filter
  • stress command shows current CPU/RAM
  • Use Crash Watchdog
  • Ask the AI Assistant

Security
  • Backup before major changes
  • Use panel password
  • Never share the Discord token

Customization
  • Settings → Discord theme (4 built-in)
  • Settings → Error sound (8 options)
  • 🎨 Appearance — bot emoji + color
  • Extend with plugins

## Troubleshooting

Bot won't start
  • Check that the .py file exists
  • Check the logs
  • Try manually: py bot.py

Panel doesn't detect the bot
  • Use the /connect command
  • Verify panel ID matches
  • Restarting may help

Commander commands not showing
  • Discord refreshes slash commands hourly
  • Or: /commander_reload on dev server

AI not responding
  • Check AI provider in Settings
  • If Ollama: `ollama list` should show the model
  • If OpenAI: valid API key?
  • Try smaller model: `ollama pull llama3.2:1b`

Temperature not showing
  • Windows often doesn't expose it via WMI
  • Install LibreHardwareMonitor
  • Or ignore it (CPU % shows load)
""",
        },
    ],
}


class WindowTutorialMixin:
    """Beépített tutorial / súgó ablak — kétnyelvű."""

    def open_tutorial_window(self):
        lang = getattr(self, "current_language", "English")
        sections = TUTORIAL_CONTENT.get(lang, TUTORIAL_CONTENT["English"])

        title_text = "📖 Tutorial — Discord Bot Manager"

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

        main = ctk.CTkFrame(win, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=12, pady=12)

        left = ctk.CTkFrame(main, width=260, corner_radius=8)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)

        ctk.CTkLabel(
            left, text=categories_text,
            font=("Arial", 14, "bold"), anchor="w"
        ).pack(fill="x", padx=14, pady=(14, 8))

        # Görgethető kategória lista
        left_scroll = ctk.CTkScrollableFrame(left, fg_color="transparent")
        left_scroll.pack(fill="both", expand=True, padx=4, pady=(0, 4))

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
                left_scroll,
                text=section["title"],
                anchor="w",
                fg_color="#2b2b2b",
                hover_color="#3a3a3a",
                height=38,
                font=("Arial", 12),
                command=lambda sid=section["id"]: show_section(sid),
            )
            btn.pack(fill="x", padx=4, pady=3)
            buttons[section["id"]] = btn

        ctk.CTkLabel(
            left,
            text=hint_text,
            font=("Arial", 10), text_color="#888",
            justify="left",
        ).pack(side="bottom", fill="x", padx=14, pady=8)

        ctk.CTkButton(
            win, text=close_text,
            fg_color="#555555", hover_color="#666666",
            width=120, height=36,
            command=win.destroy
        ).pack(side="bottom", pady=(0, 10))

        if sections:
            show_section(sections[0]["id"])