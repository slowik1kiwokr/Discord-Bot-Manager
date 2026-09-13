"""
Témák / skinek a DBM panelhez.
Minden téma egy dict, ami a színeket és a megjelenést határozza meg.
"""


# =====================================================================
#  TÉMÁK
# =====================================================================

THEMES = {
        # ------------------------------------------------------------------
    #  DBM (Alap) — világos sötétkék, jól látható
    # ------------------------------------------------------------------
    "DBM (Alap)": {
        "appearance_mode": "dark",
        "default_color_theme": "dark-blue",
        "colors": {
            # Akcent — blurple
            "accent": "#5865F2",
            "accent_hover": "#4752C4",

            # Sidebar — sötétkék
            "sidebar_bg": "#131720",

            # Kártyák — világosabb sötétkék
            "card_bg": "#1e2330",

            # Szövegek
            "text": "white",
            "subtext": "#8a8e98",

            # Gombok
            "save_btn": "#27ae60",
            "save_hover": "#2ecc71",

            # Keretek — blurple
            "border": "#3a4258",
            "border_glow": "#5865F2",

            # Fő háttér — sötétkék (nem fekete)
            "bg_main": "#0f1420",

            # Log — sötétkék, blurple kerettel
            "log_bg": "#131720",
            "log_border": "#5865F2",

            # Settings box
            "settings_box_bg": "#1e2330",

            # Top tab — mint a sidebar
            "top_tab_bg": "#131720",

            # Stat kártyák — világosabbak
            "stat_card_bg": "#252b3d",
            "stat_card_border": "#3a4258",
        },
    },

    # ------------------------------------------------------------------
    #  Discord Sötét (Alap)
    # ------------------------------------------------------------------
    "Discord Sötét (Alap)": {
        "appearance_mode": "dark",
        "default_color_theme": "blue",
        "colors": {
            "accent": "#1f538d",
            "accent_hover": "#143d6e",
            "sidebar_bg": "#2b2b2b",
            "card_bg": "#232323",
            "text": "white",
            "subtext": "#aaaaaa",
            "save_btn": "#27ae60",
            "save_hover": "#2ecc71",
            "border": "#3a3a3a",
            "bg_main": "#1e1e1e",
        },
    },

    # ------------------------------------------------------------------
    #  Discord Világos
    # ------------------------------------------------------------------
    "Discord Világos": {
        "appearance_mode": "light",
        "default_color_theme": "blue",
        "colors": {
            "accent": "#3b8ed0",
            "accent_hover": "#36719f",
            "sidebar_bg": "#e0e0e0",
            "card_bg": "#f0f0f0",
            "text": "black",
            "subtext": "#444444",
            "save_btn": "#27ae60",
            "save_hover": "#2ecc71",
            "border": "#b0b0b0",
            "bg_main": "#f5f5f5",
        },
    },

    # ------------------------------------------------------------------
    #  Discord Blurple (Lila-Kék)
    # ------------------------------------------------------------------
    "Discord Blurple (Lila-Kék)": {
        "appearance_mode": "dark",
        "default_color_theme": "dark-blue",
        "colors": {
            "accent": "#5865F2",
            "accent_hover": "#4752C4",
            "sidebar_bg": "#2f3136",
            "card_bg": "#202225",
            "text": "white",
            "subtext": "#b9bbbe",
            "save_btn": "#5865F2",
            "save_hover": "#4752C4",
            "border": "#40444b",
            "bg_main": "#1a1b1e",
        },
    },

    # ------------------------------------------------------------------
    #  Discord Zöld (Hacker)
    # ------------------------------------------------------------------
    "Discord Zöld (Hacker)": {
        "appearance_mode": "dark",
        "default_color_theme": "green",
        "colors": {
            "accent": "#2ecc71",
            "accent_hover": "#27ae60",
            "sidebar_bg": "#1b261b",
            "card_bg": "#141c14",
            "text": "white",
            "subtext": "#7ecc8e",
            "save_btn": "#2ecc71",
            "save_hover": "#27ae60",
            "border": "#2a3d2a",
            "bg_main": "#0e130e",
        },
    },
}


# =====================================================================
#  SEGÉDFÜGGVÉNYEK
# =====================================================================

DEFAULT_THEME = "DBM (Alap)"


def get_theme_names():
    """Az összes elérhető téma neve."""
    return list(THEMES.keys())


def get_theme(theme_name):
    """Egy téma teljes konfigurációja.

    Ha a téma nem létezik, az alapértelmezettet adja vissza.
    """
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


def get_theme_colors(theme_name):
    """Egy téma színei (másolat, hogy ne módosuljon az eredeti)."""
    theme = get_theme(theme_name)
    return theme["colors"].copy()


def get_appearance_mode(theme_name):
    """A téma megjelenési módja (dark / light)."""
    return get_theme(theme_name).get("appearance_mode", "dark")


def get_default_color_theme(theme_name):
    """A téma CustomTkinter alap színpalettája."""
    return get_theme(theme_name).get("default_color_theme", "blue")