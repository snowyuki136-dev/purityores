#!/usr/bin/env python3
"""Generates every JSON resource and placeholder texture for the Purity Ores mod.
Run from anywhere:  python generate_resources.py
Edit the ORES table to change drops, counts, heights, tools or biomes, then re-run.
(Vein sizes live in OreType.java.)"""
import json, os, random, struct, zlib

MOD = "purityores"
RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main", "resources"))

# id, stone block, deepslate block, drop item, minDrop, maxDrop, count, minY, maxY, tool, biome tag, ore RGB
ORES = [
    ("coal",          "coal_ore",           "deepslate_coal_ore",     "coal",         1, 1, 30,   0, 192, None,    "#minecraft:is_overworld", (30, 30, 30)),
    ("copper",        "copper_ore",         "deepslate_copper_ore",   "raw_copper",   2, 5, 16, -16, 112, "stone", "#minecraft:is_overworld", (205, 120, 80)),
    ("iron",          "iron_ore",           "deepslate_iron_ore",     "raw_iron",     1, 1, 25, -64,  72, "stone", "#minecraft:is_overworld", (216, 175, 147)),
    ("gold",          "gold_ore",           "deepslate_gold_ore",     "raw_gold",     1, 1,  6, -64,  32, "iron",  "#minecraft:is_overworld", (252, 238, 75)),
    ("redstone",      "redstone_ore",       "deepslate_redstone_ore", "redstone",     4, 5,  8, -64,  15, "iron",  "#minecraft:is_overworld", (210, 20, 20)),
    ("lapis",         "lapis_ore",          "deepslate_lapis_ore",    "lapis_lazuli", 4, 9,  3, -64,  64, "stone", "#minecraft:is_overworld", (30, 70, 175)),
    ("diamond",       "diamond_ore",        "deepslate_diamond_ore",  "diamond",      1, 1,  7, -64,  16, "iron",  "#minecraft:is_overworld", (90, 230, 220)),
    ("emerald",       "emerald_ore",        "deepslate_emerald_ore",  "emerald",      1, 1,  6, -16, 320, "iron",  "#minecraft:is_mountain",  (30, 200, 80)),
    ("nether_gold",   "nether_gold_ore",    None,                     "gold_nugget",  2, 6, 10,  10, 117, None,    "#minecraft:is_nether",    (252, 238, 75)),
    ("nether_quartz", "nether_quartz_ore",  None,                     "quartz",       1, 1, 16,  10, 117, None,    "#minecraft:is_nether",    (240, 235, 225)),
]

VANILLA_OVERWORLD = [
    "ore_coal_upper", "ore_coal_lower", "ore_iron_upper", "ore_iron_middle", "ore_iron_small",
    "ore_copper", "ore_copper_large", "ore_gold", "ore_gold_lower", "ore_gold_extra",
    "ore_redstone", "ore_redstone_lower", "ore_diamond", "ore_diamond_medium", "ore_diamond_large",
    "ore_diamond_buried", "ore_lapis", "ore_lapis_buried", "ore_emerald",
]
VANILLA_NETHER = ["ore_gold_nether", "ore_gold_deltas", "ore_quartz_nether", "ore_quartz_deltas"]

BASES = {"stone": (125, 125, 125), "deepslate": (80, 80, 86), "netherrack": (112, 48, 48)}


def put(rel, obj):
    path = os.path.join(RES, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def title(name):
    return " ".join(w.capitalize() for w in name.split("_"))


def write_png(path, pixels):
    raw = b"".join(b"\x00" + bytes(c for px in row for c in px) for row in pixels)
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", 16, 16, 8, 6, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(png)


def clamp(v):
    return max(0, min(255, v))


def placeholder_texture(path, base, ore_rgb, blobs, rnd):
    px = [[tuple(clamp(c + rnd.randint(-12, 12)) for c in base) + (255,) for _ in range(16)] for _ in range(16)]
    for _ in range(blobs):
        cx, cy = rnd.randint(1, 13), rnd.randint(1, 13)
        cells = [(0, 0), (1, 0), (0, 1), (1, 1)]
        cells.append(rnd.choice([(-1, 0), (2, 1), (1, 2), (0, -1)]))
        for dx, dy in cells:
            x, y = cx + dx, cy + dy
            if 0 <= x < 16 and 0 <= y < 16:
                px[y][x] = tuple(clamp(c + rnd.randint(-15, 15)) for c in ore_rgb) + (255,)
    write_png(path, px)


def loot_table(name, drop, lo, hi):
    return {
        "type": "minecraft:block",
        "pools": [{
            "bonus_rolls": 0.0,
            "entries": [{
                "type": "minecraft:alternatives",
                "children": [
                    {
                        "type": "minecraft:item",
                        "conditions": [{
                            "condition": "minecraft:match_tool",
                            "predicate": {"predicates": {"minecraft:enchantments": [
                                {"enchantments": "minecraft:silk_touch", "levels": {"min": 1}}]}},
                        }],
                        "name": f"{MOD}:{name}",
                    },
                    {
                        "type": "minecraft:item",
                        "functions": [
                            {"function": "minecraft:set_count",
                             "count": {"type": "minecraft:uniform", "min": lo, "max": hi}},
                            {"function": "minecraft:apply_bonus", "enchantment": "minecraft:fortune",
                             "formula": "minecraft:ore_drops"},
                            {"function": "minecraft:explosion_decay"},
                        ],
                        "name": f"minecraft:{drop}",
                    },
                ],
            }],
            "rolls": 1.0,
        }],
        "random_sequence": f"{MOD}:blocks/{name}",
    }


lang = {}
all_blocks = []
tool_tags = {"stone": [], "iron": []}

for (oid, stone_name, deep_name, drop, dmin, dmax, count, miny, maxy, tool, biomes, rgb) in ORES:
    # --- world generation ---
    feature_id = f"{oid}_purity_vein"
    put(f"data/{MOD}/worldgen/configured_feature/{feature_id}.json",
        {"type": f"{MOD}:purity_vein", "config": {"ore": oid}})
    put(f"data/{MOD}/worldgen/placed_feature/{feature_id}.json", {
        "feature": f"{MOD}:{feature_id}",
        "placement": [
            {"type": "minecraft:count", "count": count},
            {"type": "minecraft:in_square"},
            {"type": "minecraft:height_range", "height": {
                "type": "minecraft:uniform",
                "min_inclusive": {"absolute": miny}, "max_inclusive": {"absolute": maxy}}},
            {"type": "minecraft:biome"},
        ],
    })
    put(f"data/{MOD}/neoforge/biome_modifier/add_{feature_id}.json", {
        "type": "neoforge:add_features", "biomes": biomes,
        "features": f"{MOD}:{feature_id}", "step": "underground_ores"})

    # --- blocks ---
    hosts = [(False, "netherrack" if oid.startswith("nether") else "stone")]
    if deep_name:
        hosts.append((True, "deepslate"))
    for deepslate, base_key in hosts:
        for tier in ("poor", "rich"):
            name = f"{tier}_{'deepslate_' if deepslate else ''}{oid}_ore"
            all_blocks.append(f"{MOD}:{name}")
            lang[f"block.{MOD}.{name}"] = title(name)
            model = {"model": f"{MOD}:block/{name}"}
            if oid == "redstone":  # redstone ore blocks have a "lit" property
                variants = {"lit=false": model, "lit=true": model}
            else:
                variants = {"": model}
            put(f"assets/{MOD}/blockstates/{name}.json", {"variants": variants})
            put(f"assets/{MOD}/models/block/{name}.json",
                {"parent": "minecraft:block/cube_all", "textures": {"all": f"{MOD}:block/{name}"}})
            put(f"assets/{MOD}/models/item/{name}.json", {"parent": f"{MOD}:block/{name}"})
            lo, hi = (dmin * 0.25, dmax * 0.75) if tier == "poor" else (dmin * 1.5, dmax * 2.0)
            put(f"data/{MOD}/loot_table/blocks/{name}.json", loot_table(name, drop, lo, hi))
            if tool:
                tool_tags[tool].append(f"{MOD}:{name}")
            rnd = random.Random(name)
            placeholder_texture(os.path.join(RES, f"assets/{MOD}/textures/block/{name}.png"),
                                BASES[base_key], rgb, 2 if tier == "poor" else 5, rnd)

put(f"assets/{MOD}/lang/en_us.json", lang)
put("data/minecraft/tags/block/mineable/pickaxe.json", {"replace": False, "values": all_blocks})
put("data/minecraft/tags/block/needs_stone_tool.json", {"replace": False, "values": tool_tags["stone"]})
put("data/minecraft/tags/block/needs_iron_tool.json", {"replace": False, "values": tool_tags["iron"]})

# --- remove vanilla ore generation ---
put(f"data/{MOD}/neoforge/biome_modifier/remove_vanilla_ores_overworld.json", {
    "type": "neoforge:remove_features", "biomes": "#minecraft:is_overworld",
    "features": [f"minecraft:{n}" for n in VANILLA_OVERWORLD]})
put(f"data/{MOD}/neoforge/biome_modifier/remove_vanilla_ores_nether.json", {
    "type": "neoforge:remove_features", "biomes": "#minecraft:is_nether",
    "features": [f"minecraft:{n}" for n in VANILLA_NETHER]})

print(f"Generated resources for {len(all_blocks)} blocks in {RES}")
