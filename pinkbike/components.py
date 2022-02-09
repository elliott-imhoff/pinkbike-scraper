"""Keywords used to classify component make and models."""


class Fork:
    """Stores important keywords for fork type parsing."""

    def __init__(
        self, make, keywords, models=None, trims=None, springs=None, dampers=None
    ):
        """Construct an instance of fork keyword info."""
        self.make = make
        self.keywords = keywords
        self.models = models if models else []
        self.trims = trims if models else []
        self.springs = springs
        self.dampers = dampers


forks = {
    "Fox": Fork(
        "Fox",
        [
            "Fox",
            "Factory",
            "Elite",
            "Rhythm",
            "float",
            "Talas",
            "For 34",
            "Fork 38",
            "36 grip 2",
        ],
        ["32", "34", "36", "38", "40"],
        ["831", "Step Cast", "Factory", "Elite", "Performance", "Rhythm", "Evolution"],
        ["Float", "Talas", "Van", "Vanilla"],
        ["Grip2", "Grip", "Fit4", "CTD", "RLC", "RL", "RC2", "R"],
    ),
    "RockShox": Fork(
        "RockShox",
        [
            "RockShox",
            "RockShock",
            "Roxshox",
            "Rickshox",
            "Rock",
            "ZEB",
            "Pike",
            "Lyrik",
            "Yari",
            "SID ",
            "Recon",
            "Reba",
            "Revelation",
            "Judy",
            "Lyric",
            "Lyrick",
            "35 gold rl",
            "RS1",
            "Sektor",
        ],
    ),
    "Cane Creek": Fork("Cane Creek", ["Cane Creek", "Helm", "MKII"]),
    "DVO": Fork("DVO", ["DVO", "Diamond", "Onyx"]),
    "Ohlins": Fork("Ohlins", ["Ohlins", "RXF", "RXF36"]),
    "Marzocchi": Fork(
        "Marzocchi", ["Marzocchi", "Marzzochi", "Bomber", "Z1", "Z2", "Marzochii"]
    ),
    "Manitou": Fork("Manitou", ["Manitou", "Maintou", "Mezzer"]),
    "Magura": Fork("Magura", ["Magura", "Maguar"]),
    "Trust": Fork("Trust", ["Trust", "Message", "Shout"]),
    "Suntour": Fork("Suntour", ["Suntour", "Sountour", "xcr"]),
    "X-Fusion": Fork("X-Fusion", ["X-Fusion", "xfusion", "Fusion"]),
    "White Brothers": Fork("White Brothers", ["White Brothers"]),
    "Cannondale": Fork("Cannondale", ["Cannondale", "Lefty"]),
    "Giant": Fork("Giant", ["Giant", "Crest"]),
    "MRP": Fork("MRP", ["Ribbon", "Stage", "Loop"]),
    "Spinner": Fork("Spinner", ["Odesa", "Spinner"]),
    "Bos Deville": Fork("Bos Deville", ["Deville", "Devile"]),
    "Lauf": Fork("Lauf", ["Lauf"]),
    "Formula": Fork("Formula", ["Formula", "Selva"]),
    "DT Swiss": Fork("DT Swiss", ["DT Swiss", "DT OPM"]),
    "EXT": Fork("EXT", ["Ext Era"]),
}
