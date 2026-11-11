# Content for the Lumiwire website. Facts come from the app (Desktop/Projects/lumiwire):
# PLAN.md sections 5, 7 and 8, src/content/strings.ts (tips, Settings labels) and
# src/state/progression.ts (stars). Keep it true to the build that is in testers' hands.

SUPPORT_EMAIL = "sriramgoparaju99@gmail.com"   # support@<domain> once the domain and Email Routing exist
PLAY_URL = "https://play.google.com/store/apps/details?id=com.lumiwire.app"
APP_STORE_URL = ""                             # set on launch day (App Store Connect app id)
UPDATED = "11 November 2026"                   # "Last updated" on the legal pages

# Ads, hints, coins for sale and purchases arrive with Phase 10. Until that build reaches
# testers, the site says so; flip to True when it does (and rebuild).
SHOP_LIVE = False

FEATURES = [
    ("One answer, always", "Every board is proven by a solver to have exactly one solution, with every obstacle in place. Nothing is hidden and nothing is random, so careful thinking always gets you there."),
    ("Eight chapters, eight new ideas", "Dead chips, cut traces, fuses, relays, soldered traces, bridges, vias and wrap-around edges, each introduced gently on an easy board with a one-line tip."),
    ("Stars for style, not speed", "Draw every wire in one stroke for three stars. In the Journey the clock never counts."),
    ("A Daily that doesn't nag", "One board a day, the same for everyone, with a leaderboard if you want it. No streak counter on the home screen, and nothing lost for missing a day."),
    ("Blitz when you have a minute", "Sixty seconds of tiny boards. A board drawn in one stroke per wire adds two seconds. Daily and weekly leaderboards for the competitive."),
    ("Easy on the eyes", "Graphite in the dark, Paper in the light. Every pair has a symbol as well as a colour, and the colours are tuned to stay distinct for colour-blind players."),
    ("Plays offline", "Everything plays without a connection. Your results go up to the leaderboards when you're back online."),
] + ([
    ("Ads that wait their turn", "Never in the middle of a board: a short Ad break every third level from level 6, and Remove Ads, once, to end them. Other ads play only when you ask for one."),
] if SHOP_LIVE else [
    ("No sign-up", "No account to make and no email to give. Open it and play."),
])

RULES = [
    "Each pair of sockets has its own colour and its own symbol. Drag from one socket to its twin to lay a wire between them.",
    "Wires run along the grid, never diagonally. They never cross each other and never pass through another pair's socket.",
    "Drag through another wire to cut it: the cut part springs back. Drag from the middle of one of your wires to re-route it from there.",
    "The board is complete when every pair is joined and every cell is covered.",
    "Undo, Redo and Clear sit under the board. There are no wrong moves, no lives and no time limit in the Journey.",
]

OBSTACLES = [
    {"name": "Dead chips", "chapter": 2, "level": 51, "image": "obstacle-dead",
     "rule": "Dark blocks that are not part of the board. Wires go around them, and they cut boards into new shapes.",
     "alt": "A dark board with four dead chips: square dark blocks in four cells."},
    {"name": "Cut traces", "chapter": 3, "level": 101, "image": "obstacle-cut",
     "rule": "A broken-trace mark on the edge between two cells. No wire may cross that edge, but both cells still need filling.",
     "alt": "A board with short dashed marks on three cell edges; the wires route around them."},
    {"name": "Fuses", "chapter": 4, "level": 151, "image": "obstacle-fuse",
     "rule": "A fused socket starts dark and shows the symbol of the pair that powers it. Connect that pair and the fuse blows: the socket lights up in its own colour, ready to be wired.",
     "alt": "A board with one dark socket carrying a fuse mark and a small green triangle, the pair that powers it."},
    {"name": "Relays", "chapter": 5, "level": 201, "image": "obstacle-relay",
     "rule": "A diamond pad ringed in one colour. Only that colour's wire may pass through it, and that wire must.",
     "alt": "A board with diamond-shaped pads; the red and green wires pass through the diamonds in their own colour."},
    {"name": "Soldered traces", "chapter": 6, "level": 251, "image": "obstacle-solder",
     "rule": "A few cells of a wire already laid, with a joint at each end. They can't be cut or cleared, and their pair's wire has to run through them.",
     "alt": "A board with a short blue wire segment already laid in the top right corner."},
    {"name": "Bridges", "chapter": 7, "level": 301, "image": "obstacle-bridge",
     "rule": "An overpass that takes two wires straight through: one passes under, the other crosses on top.",
     "alt": "A solved light board where a green wire crosses over a dark blue wire on a bridge near the bottom right."},
    {"name": "Vias", "chapter": 8, "level": 351, "image": "obstacle-via",
     "rule": "Two holes with the same letter. A wire that goes into one comes out of the other, so far-apart parts of the board join up.",
     "alt": "A light board with two holes marked A; the blue wire enters one and carries on from the other."},
    {"name": "Wrap-around edges", "chapter": 8, "level": 371, "image": "obstacle-wrap",
     "rule": "On a board with dashed side edges, a wire leaving the right edge comes back in on the left, and the other way round.",
     "alt": "A solved light board with dashed left and right edges and small arrows where wires leave one side and enter the other."},
]

STARS = [
    (3, "Every wire drawn in one stroke" + (", with no wire revealed by a hint." if SHOP_LIVE else ".")),
    (2, "Finished any other way: a wire took two strokes, was cut or re-routed" + (", or was revealed by a hint." if SHOP_LIVE else ".")),
]

MODES = [
    ("Journey", "The main road: 400 levels in eight chapters. Levels climb gently, every sixth one is a Challenge, and each chapter ends with a boss."),
    ("Daily", "One board a day for everyone, new at 00:00 UTC, using only obstacles you have already met. The timer stays hidden unless you switch it on; your time goes to the Daily leaderboard. Past days wait in the calendar."),
    ("Blitz", "Opens after Journey level 10. Solve as many tiny boards as you can in 60 seconds: 4×4, then 5×5, then 6×6. A board drawn in one stroke per wire adds two seconds. Everyone gets the same boards each day."),
]

CHAPTERS = [
    ("Mainboard", 1, 50, "the basics"),
    ("Power Grid", 51, 100, "dead chips and rectangular boards"),
    ("Neon District", 101, 150, "cut traces"),
    ("Server Farm", 151, 200, "fuses"),
    ("Orbit", 201, 250, "relays"),
    ("Deep Core", 251, 300, "soldered traces"),
    ("Quantum", 301, 350, "bridges"),
    ("Nebula", 351, 400, "vias and wrap-around edges"),
]

FAQ = [
    ("How do I play?",
     "Drag from a socket to the socket with the same colour and symbol to lay a wire. Wires can't cross, and the board is finished when every pair is joined and every cell is covered. The How to play page has the details and every obstacle."),
    ("Is there really only one solution?",
     "Yes. Every board was checked by a solver before it shipped, with all its obstacles in place, and has exactly one solution. Nothing is hidden and nothing is random, so you can always reason your way to it without guessing."),
    ("I'm stuck. What now?",
     "Start at the edges and corners: pairs near a wall, or next to each other, usually have only one sensible route. Look for cells that only one wire could reach. "
     + ("If you'd still like help, the Hint button can reveal a wire, for coins or a short ad you choose to watch. A level with a revealed wire earns at most two stars."
        if SHOP_LIVE else "Hints arrive in a coming update.")),
    ("When does the Daily puzzle change?",
     "At 00:00 UTC (5:30 am in India), with the same board for everyone. It only uses obstacles you have already met in the Journey. The timer is hidden unless you switch it on in the pause menu, but your time still goes to the Daily leaderboard. Solve it on days in a row and the result says how many; nothing happens if you miss a day. Past days are in the calendar"
     + (", for a few coins or a short ad." if SHOP_LIVE else ".")),
    ("How does Blitz work?",
     "Blitz opens after Journey level 10. You have 60 seconds to solve as many tiny boards as you can: 4×4 at first, then 5×5, then 6×6. A board drawn with every wire in one stroke adds 2 seconds. Everyone gets the same boards on the same day, so the leaderboards are fair."
     + (" Once a round, you can add 15 seconds by watching a short ad." if SHOP_LIVE else "")),
    ("How do the leaderboards work?",
     "There are three: today's Daily (fastest time), Blitz today (most boards, then fastest) and Blitz week (your best Blitz score of each day, added up). A result goes up only when it beats your own best, and you see the top 100 and your own place. You appear under a display name: a random one, like \"Copper Fox\", until you change it in Settings → Display name (up to 16 characters)."),
    ("Does Lumiwire work offline?",
     "Yes. Every level, the Daily and Blitz play without a connection. Your results and your saved progress go up the next time you're online. The leaderboards need a connection to show."),
    ("Can I move my progress to a new phone?",
     "Not yet. Lumiwire has no sign-in: your progress is saved against an anonymous account that belongs to the app on your phone, and there is nothing we could look it up by on another phone."
     + (" Purchases are different: Remove Ads comes back on any phone signed in to the same store account." if SHOP_LIVE else "")),
    ("What does Reset progress do?",
     "Settings → Reset progress starts the Journey over, on your phone and in your cloud save: stars and levels go back to the beginning. Your Daily and Blitz records stay. It asks twice, and it can't be undone."),
] + ([
    ("Will an ad interrupt a board?",
     "Never. Ads come between levels: an Ad break after every third Journey level from level 6 (or after a Blitz round), with a short card first, and never within two minutes of another ad. Every other ad plays only when you ask for one, for a hint or extra coins. Remove Ads, a one-time purchase, ends the Ad breaks; the ads you choose stay available."),
    ("How do I restore a purchase?",
     "Open the Shop or Settings and tap Restore purchases, on a phone signed in to the same Google Play or App Store account you bought with. Remove Ads comes back. Coin packs are spent when you buy them, so restoring doesn't add them again."),
    ("How do I change my ad privacy choices?",
     "Where the law requires Google's consent form (for example in the EEA and the UK), Settings shows Privacy options, which reopens it. On iPhone you can change whether apps may track you in Settings → Privacy & Security → Tracking. On Android you can reset or delete your advertising ID in your phone's settings."),
] if SHOP_LIVE else []) + [
    ("I'm colour-blind. Can I play?",
     "Yes. Every pair has its own symbol as well as its colour (circle, square, triangle and so on), so no board depends on telling colours apart, and the wire colours are tuned to stay distinct for the common kinds of colour blindness."),
    ("How do I turn off sounds or vibration?",
     "Settings has switches for Sound, Music and Haptics."),
    ("How do I delete my account?",
     "Settings → Delete account. It needs a connection and asks twice, then deletes your cloud save, your rows on every leaderboard and your anonymous account, and then everything on the phone. The delete-account page explains what is removed and what is kept."),
]
