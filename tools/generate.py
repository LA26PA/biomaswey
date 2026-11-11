#!/usr/bin/env python3
"""
Generador de recursos de Biomas Salvajes (Fabric 1.21.8).
Crea: texturas, modelos, blockstates, loot tables, recetas, tags, lang,
biomas, features, estructuras (.nbt) y sus JSON.
Uso:  pip install pillow   &&   python3 tools/generate.py
"""
import gzip, json, random, struct
from pathlib import Path
from PIL import Image

MOD = "biomassalvajes"
ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "src/main/resources"
ASSETS = RES / "assets" / MOD
DATA = RES / "data" / MOD
MC_DATA_VERSION = 4440  # 1.21.8


def wjson(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rgb(h):
    return int(h, 16)


# ---------------------------------------------------------------- TEXTURAS
def save_tex(name, img):
    p = ASSETS / "textures/block" / f"{name}.png"
    p.parent.mkdir(parents=True, exist_ok=True)
    img.save(p)


def noise_tex(pal, seed):
    r = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            im.putpixel((x, y), r.choice(pal) + (255,))
    return im


def streak_tex(pal, seed):  # lineas verticales (corteza)
    r = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    cols = [r.choice(pal) for _ in range(16)]
    for y in range(16):
        for x in range(16):
            c = cols[x] if r.random() > 0.25 else r.choice(pal)
            im.putpixel((x, y), c + (255,))
    return im


def ring_tex(pal, seed):  # extremo de tronco
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            d = max(abs(x - 7.5), abs(y - 7.5))
            c = pal[int(d) % len(pal)] if d < 7 else pal[-1]
            im.putpixel((x, y), c + (255,))
    return im


def planks_tex(pal, seed):
    r = random.Random(seed)
    im = Image.new("RGBA", (16, 16))
    for y in range(16):
        for x in range(16):
            c = pal[(y // 4) % len(pal)]
            if y % 4 == 3:
                c = tuple(int(v * 0.7) for v in c)
            elif r.random() < 0.15:
                c = tuple(min(255, int(v * 1.1)) for v in c)
            im.putpixel((x, y), c + (255,))
    return im


def dirt_tex():
    return noise_tex([(134, 96, 67), (121, 85, 58), (110, 77, 52), (146, 106, 76)], 99)


def side_tex(top_pal, seed):  # lado tipo "bloque de cesped" sobre tierra
    r = random.Random(seed)
    im = dirt_tex()
    for x in range(16):
        h = 3 + r.randint(0, 2)
        for y in range(h):
            im.putpixel((x, y), r.choice(top_pal) + (255,))
    return im


# nombre -> (es, en, tipo, paletas, luz, dureza/tool)
BLOCKS = {
    "crystal_log": dict(es="Tronco de cristal", en="Crystal Log", kind="pillar",
                        side=[(50, 140, 160), (70, 175, 195), (40, 115, 140)],
                        top=[(160, 235, 240), (110, 205, 215), (60, 150, 165)], tool="axe"),
    "crystal_planks": dict(es="Tablones de cristal", en="Crystal Planks", kind="planks",
                           pal=[(120, 210, 222), (100, 190, 206), (135, 222, 232)], tool="axe"),
    "crystal_leaves": dict(es="Hojas de cristal", en="Crystal Leaves", kind="leaves",
                           pal=[(90, 220, 235), (120, 240, 250), (70, 190, 215), (150, 250, 255)], tool="hoe"),
    "glow_moss_block": dict(es="Bloque de musgo luminoso", en="Glow Moss Block", kind="cube",
                            pal=[(40, 150, 110), (70, 200, 140), (120, 240, 170), (30, 120, 90)], tool="hoe"),
    "blue_mud": dict(es="Lodo azul", en="Blue Mud", kind="cube",
                     pal=[(30, 60, 110), (40, 80, 140), (25, 50, 95)], tool="shovel"),
    "black_sand": dict(es="Arena negra", en="Black Sand", kind="sand",
                       pal=[(30, 30, 34), (42, 42, 48), (22, 22, 26), (55, 55, 62)], tool="shovel"),
    "volcanic_glass": dict(es="Vidrio volcánico", en="Volcanic Glass", kind="cube",
                           pal=[(20, 10, 35), (35, 15, 60), (55, 25, 90), (15, 8, 25)], tool="pickaxe"),
    "amber_block": dict(es="Bloque de ámbar", en="Amber Block", kind="cube",
                        pal=[(240, 170, 40), (255, 195, 70), (220, 140, 20), (255, 215, 110)], tool="pickaxe"),
    "amber_permafrost": dict(es="Permafrost de ámbar", en="Amber Permafrost", kind="topside",
                             top=[(200, 175, 120), (215, 195, 150), (185, 160, 105), (240, 240, 245)],
                             side=[(215, 195, 150), (240, 240, 245), (200, 175, 120)], tool="shovel"),
    "red_mycelium": dict(es="Micelio rojo", en="Red Mycelium", kind="topside",
                         top=[(160, 40, 50), (190, 60, 70), (130, 30, 40)],
                         side=[(190, 60, 70), (160, 40, 50), (130, 30, 40)], tool="shovel"),
    "spore_stem": dict(es="Tallo esporado", en="Spore Stem", kind="pillar",
                       side=[(215, 200, 180), (190, 170, 150), (235, 225, 210), (180, 60, 70)],
                       top=[(225, 210, 190), (200, 180, 160), (180, 60, 70)], tool="axe"),
}

BIOME_NAMES = {
    "crystal_forest": ("Bosque de Cristal", "Crystal Forest"),
    "glow_swamp": ("Pantano Bioluminiscente", "Bioluminescent Swamp"),
    "obsidian_desert": ("Desierto de Obsidiana", "Obsidian Desert"),
    "amber_tundra": ("Tundra de Ámbar", "Amber Tundra"),
    "fungal_jungle": ("Jungla de Hongos Gigantes", "Giant Mushroom Jungle"),
}


def gen_blocks():
    seed = 1
    for name, b in BLOCKS.items():
        seed += 1
        k = b["kind"]
        full = f"{MOD}:block/{name}"
        if k in ("cube", "sand", "leaves"):
            save_tex(name, noise_tex(b["pal"], seed))
            model = {"parent": "minecraft:block/cube_all", "textures": {"all": full}}
            wjson(ASSETS / f"blockstates/{name}.json", {"variants": {"": {"model": full}}})
        elif k == "planks":
            save_tex(name, planks_tex(b["pal"], seed))
            model = {"parent": "minecraft:block/cube_all", "textures": {"all": full}}
            wjson(ASSETS / f"blockstates/{name}.json", {"variants": {"": {"model": full}}})
        elif k == "pillar":
            save_tex(name, streak_tex(b["side"], seed))
            save_tex(name + "_top", ring_tex(b["top"], seed))
            model = {"parent": "minecraft:block/cube_column",
                     "textures": {"end": full + "_top", "side": full}}
            wjson(ASSETS / f"blockstates/{name}.json", {"variants": {
                "axis=y": {"model": full},
                "axis=z": {"model": full, "x": 90},
                "axis=x": {"model": full, "x": 90, "y": 90}}})
        elif k == "topside":
            save_tex(name + "_top", noise_tex(b["top"], seed))
            save_tex(name + "_side", side_tex(b["side"], seed))
            model = {"parent": "minecraft:block/cube_bottom_top",
                     "textures": {"top": full + "_top", "side": full + "_side",
                                  "bottom": "minecraft:block/dirt"}}
            wjson(ASSETS / f"blockstates/{name}.json", {"variants": {"": {"model": full}}})
        wjson(ASSETS / f"models/block/{name}.json", model)
        wjson(ASSETS / f"items/{name}.json", {"model": {"type": "minecraft:model", "model": full}})

        # loot table
        drop = name
        if name == "red_mycelium" or name == "amber_permafrost":
            drop = None
        item = f"{MOD}:{drop}" if drop else "minecraft:dirt"
        if k == "leaves":
            loot = {"type": "minecraft:block", "pools": [
                {"rolls": 1, "bonus_rolls": 0,
                 "conditions": [{"condition": "minecraft:match_tool", "predicate": {"items": "minecraft:shears"}}],
                 "entries": [{"type": "minecraft:item", "name": f"{MOD}:{name}"}]},
                {"rolls": 1, "bonus_rolls": 0,
                 "conditions": [{"condition": "minecraft:random_chance", "chance": 0.05}],
                 "entries": [{"type": "minecraft:item", "name": "minecraft:stick"}]}]}
        else:
            loot = {"type": "minecraft:block", "pools": [
                {"rolls": 1, "bonus_rolls": 0,
                 "conditions": [{"condition": "minecraft:survives_explosion"}],
                 "entries": [{"type": "minecraft:item", "name": item}]}]}
        wjson(DATA / f"loot_table/blocks/{name}.json", loot)

    # receta: tablones
    wjson(DATA / "recipe/crystal_planks.json", {
        "type": "minecraft:crafting_shapeless", "category": "building",
        "ingredients": [f"{MOD}:crystal_log"],
        "result": {"id": f"{MOD}:crystal_planks", "count": 4}})


def gen_tags():
    tags = {
        "mineable/axe": ["crystal_log", "crystal_planks", "spore_stem"],
        "mineable/hoe": ["crystal_leaves", "glow_moss_block"],
        "mineable/shovel": ["blue_mud", "black_sand", "amber_permafrost", "red_mycelium"],
        "mineable/pickaxe": ["volcanic_glass", "amber_block"],
        "logs": ["crystal_log"], "logs_that_burn": ["crystal_log"],
        "planks": ["crystal_planks"], "leaves": ["crystal_leaves"],
        "dirt": ["blue_mud", "red_mycelium", "amber_permafrost"],
        "sand": ["black_sand"], "dry_vegetation_may_place_on": ["black_sand"],
        "mushroom_grow_block": ["red_mycelium"],
        "mooshrooms_spawnable_on": ["red_mycelium"],
        "animals_spawnable_on": ["blue_mud", "amber_permafrost"],
    }
    for k, v in EXTRA_TAGS.items():
        tags.setdefault(k, []).extend(v)
    for tag, vals in tags.items():
        wjson(RES / f"data/minecraft/tags/block/{tag}.json",
              {"replace": False, "values": [f"{MOD}:{v}" for v in vals]})
    for tag in ("logs", "logs_that_burn", "planks", "leaves"):
        wjson(RES / f"data/minecraft/tags/item/{tag}.json",
              {"replace": False, "values": [f"{MOD}:{v}" for v in tags[tag]]})


def gen_lang():
    en, es = {}, {}
    for n, b in BLOCKS.items():
        en[f"block.{MOD}.{n}"] = b["en"]
        es[f"block.{MOD}.{n}"] = b["es"]
    for n, (e, n_en) in BIOME_NAMES.items():
        es[f"biome.{MOD}.{n}"] = e
        en[f"biome.{MOD}.{n}"] = n_en
    wjson(ASSETS / "lang/en_us.json", en)
    wjson(ASSETS / "lang/es_es.json", es)
    wjson(ASSETS / "lang/es_ar.json", es)
    wjson(ASSETS / "lang/es_mx.json", es)


# ---------------------------------------------------------------- FEATURES
def state(name, props=None):
    s = {"Name": name}
    if props:
        s["Properties"] = props
    return s


def simple(name, props=None):
    return {"type": "minecraft:simple_state_provider", "state": state(name, props)}


def configured(name, obj):
    wjson(DATA / f"worldgen/configured_feature/{name}.json", obj)


def placed(name, feature, placement):
    wjson(DATA / f"worldgen/placed_feature/{name}.json", {"feature": feature, "placement": placement})


def tree_placement(count):
    return [{"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
            {"type": "minecraft:surface_water_depth_filter", "max_water_depth": 0},
            {"type": "minecraft:heightmap", "heightmap": "OCEAN_FLOOR"},
            {"type": "minecraft:biome"}]


def patch_placement(count, rarity=None):
    p = []
    if rarity:
        p.append({"type": "minecraft:rarity_filter", "chance": rarity})
    p += [{"type": "minecraft:count", "count": count}, {"type": "minecraft:in_square"},
          {"type": "minecraft:heightmap", "heightmap": "MOTION_BLOCKING"},
          {"type": "minecraft:biome"}]
    return p


def patch_cfg(block, tries=32, spread=7, solid_below=False):
    pred = {"type": "minecraft:matching_blocks", "blocks": "minecraft:air"}
    if solid_below:
        pred = {"type": "minecraft:all_of", "predicates": [
            pred, {"type": "minecraft:solid", "offset": [0, -1, 0]}]}
    return {"type": "minecraft:random_patch", "config": {
        "tries": tries, "xz_spread": spread, "y_spread": 3,
        "feature": {"feature": {"type": "minecraft:simple_block",
                                "config": {"to_place": simple(block)}},
                    "placement": [{"type": "minecraft:block_predicate_filter",
                                   "predicate": pred}]}}}


def gen_features():
    # Arbol de cristal
    configured("crystal_tree", {"type": "minecraft:tree", "config": {
        "trunk_provider": simple(f"{MOD}:crystal_log", {"axis": "y"}),
        "trunk_placer": {"type": "minecraft:straight_trunk_placer",
                         "base_height": 6, "height_rand_a": 3, "height_rand_b": 0},
        "foliage_provider": simple(f"{MOD}:crystal_leaves", {"distance": "7", "persistent": "false", "waterlogged": "false"}),
        "foliage_placer": {"type": "minecraft:blob_foliage_placer", "radius": 2, "offset": 0, "height": 3},
        "minimum_size": {"type": "minecraft:two_layers_feature_size", "limit": 1, "lower_size": 0, "upper_size": 1},
        "dirt_provider": simple("minecraft:dirt"),
        "ignore_vines": True}})
    placed("crystal_tree", f"{MOD}:crystal_tree", tree_placement(7))

    configured("crystal_flowers", patch_cfg("minecraft:cornflower", 24, 6))
    placed("crystal_flowers", f"{MOD}:crystal_flowers", patch_placement(1, 2))
    configured("crystal_grass", patch_cfg("minecraft:short_grass", 40, 7))
    placed("crystal_grass", f"{MOD}:crystal_grass", patch_placement(3))

    # Pantano
    placed("glow_swamp_tree", "minecraft:swamp_oak", tree_placement(3))
    configured("glow_orchids", patch_cfg("minecraft:blue_orchid", 20, 6))
    placed("glow_orchids", f"{MOD}:glow_orchids", patch_placement(2))
    configured("swamp_ferns", patch_cfg("minecraft:fern", 32, 7))
    placed("swamp_ferns", f"{MOD}:swamp_ferns", patch_placement(2))

    # Desierto
    configured("obsidian_dead_bush", patch_cfg("minecraft:dead_bush", 20, 6))
    placed("obsidian_dead_bush", f"{MOD}:obsidian_dead_bush", patch_placement(2))
    configured("obsidian_cactus", patch_cfg("minecraft:cactus", 10, 6))
    placed("obsidian_cactus", f"{MOD}:obsidian_cactus", patch_placement(1, 3))

    # Tundra
    placed("amber_spruce", "minecraft:spruce", tree_placement(2))
    configured("amber_ferns", patch_cfg("minecraft:fern", 24, 6))
    placed("amber_ferns", f"{MOD}:amber_ferns", patch_placement(1, 2))
    configured("amber_nuggets", patch_cfg(f"{MOD}:amber_block", 4, 3, True))
    placed("amber_nuggets", f"{MOD}:amber_nuggets", patch_placement(1, 3))

    # Jungla fungica
    placed("fungal_red_mushroom", "minecraft:huge_red_mushroom", tree_placement(3))
    placed("fungal_brown_mushroom", "minecraft:huge_brown_mushroom", tree_placement(1))
    configured("fungal_small_red", patch_cfg("minecraft:red_mushroom", 24, 6))
    placed("fungal_small_red", f"{MOD}:fungal_small_red", patch_placement(2))
    configured("fungal_small_brown", patch_cfg("minecraft:brown_mushroom", 24, 6))
    placed("fungal_small_brown", f"{MOD}:fungal_small_brown", patch_placement(2))


# ---------------------------------------------------------------- BIOMAS
ORES = ["minecraft:ore_dirt", "minecraft:ore_gravel", "minecraft:ore_granite_upper",
        "minecraft:ore_diorite_upper", "minecraft:ore_andesite_upper",
        "minecraft:ore_coal_upper", "minecraft:ore_coal_lower",
        "minecraft:ore_iron_upper", "minecraft:ore_iron_middle", "minecraft:ore_iron_small",
        "minecraft:ore_gold", "minecraft:ore_gold_lower", "minecraft:ore_redstone",
        "minecraft:ore_redstone_lower", "minecraft:ore_diamond", "minecraft:ore_diamond_large",
        "minecraft:ore_diamond_buried", "minecraft:ore_lapis", "minecraft:ore_lapis_buried",
        "minecraft:ore_copper"]


def mob(t, w, a, b):
    return {"type": f"minecraft:{t}", "weight": w, "minCount": a, "maxCount": b}


def monsters(extra=None, skeleton="skeleton", zombie="zombie"):
    m = [mob("spider", 100, 4, 4), mob(zombie, 95, 4, 4), mob(skeleton, 100, 4, 4),
         mob("creeper", 100, 4, 4), mob("enderman", 10, 1, 4), mob("witch", 5, 1, 1)]
    return m + (extra or [])


BIOMES = {
    "crystal_forest": dict(temp=0.6, down=0.6, rain=True, sky="8FD8FF", fog="C0F0FF",
                           water="3FB8D8", water_fog="1E7FA0", grass="4FD6C0", foliage="4FD6C0",
                           veg=[f"{MOD}:crystal_tree", f"{MOD}:crystal_grass", f"{MOD}:crystal_flowers"],
                           top=[], creature=[mob("sheep", 12, 4, 4), mob("rabbit", 8, 2, 3), mob("fox", 6, 1, 2)],
                           monster=monsters()),
    "glow_swamp": dict(temp=0.8, down=0.9, rain=True, sky="4A5A9A", fog="1B2A4A",
                       water="2F6FD0", water_fog="0A2A6A", grass="2FA37A", foliage="2FA37A",
                       veg=[f"{MOD}:glow_swamp_tree", f"{MOD}:glow_orchids", f"{MOD}:swamp_ferns"],
                       top=[], creature=[mob("frog", 10, 2, 5), mob("turtle", 4, 1, 2)],
                       monster=monsters([mob("slime", 1, 1, 1)])),
    "obsidian_desert": dict(temp=2.0, down=0.0, rain=False, sky="A05A5A", fog="D08A6A",
                            water="7A3A6A", water_fog="3A1A3A", grass="6A5A5A", foliage="6A5A5A",
                            veg=[f"{MOD}:obsidian_dead_bush", f"{MOD}:obsidian_cactus"],
                            top=[], creature=[mob("rabbit", 4, 2, 3), mob("armadillo", 6, 1, 2)],
                            monster=monsters(zombie="husk")),
    "amber_tundra": dict(temp=-0.3, down=0.4, rain=True, sky="FFC670", fog="FFE0A0",
                         water="C89A3A", water_fog="806020", grass="C8A850", foliage="B89040",
                         veg=[f"{MOD}:amber_spruce", f"{MOD}:amber_ferns", f"{MOD}:amber_nuggets"],
                         top=["minecraft:freeze_top_layer"],
                         creature=[mob("rabbit", 10, 2, 3), mob("polar_bear", 1, 1, 2), mob("fox", 8, 2, 4)],
                         monster=monsters(skeleton="stray")),
    "fungal_jungle": dict(temp=0.9, down=1.0, rain=True, sky="9A4A8A", fog="6A2A5A",
                          water="8A3A9A", water_fog="4A1A5A", grass="B03A5A", foliage="B03A5A",
                          veg=[f"{MOD}:fungal_red_mushroom", f"{MOD}:fungal_brown_mushroom",
                               f"{MOD}:fungal_small_red", f"{MOD}:fungal_small_brown"],
                          top=[], creature=[mob("mooshroom", 8, 4, 8)],
                          monster=[]),
}


def gen_biomes():
    for name, b in BIOMES.items():
        features = [[] for _ in range(11)]
        features[6] = ORES
        features[8] = ["minecraft:spring_water", "minecraft:spring_lava"]
        features[9] = b["veg"]
        features[10] = b["top"]
        wjson(DATA / f"worldgen/biome/{name}.json", {
            "has_precipitation": b["rain"],
            "temperature": b["temp"],
            "downfall": b["down"],
            "effects": {
                "sky_color": rgb(b["sky"]), "fog_color": rgb(b["fog"]),
                "water_color": rgb(b["water"]), "water_fog_color": rgb(b["water_fog"]),
                "grass_color": rgb(b["grass"]), "foliage_color": rgb(b["foliage"])},
            "spawners": {
                "monster": b["monster"], "creature": b["creature"],
                "ambient": [mob("bat", 10, 8, 8)],
                "water_creature": [mob("squid", 10, 1, 4)]},
            "spawn_costs": {},
            "carvers": ["minecraft:cave", "minecraft:cave_extra_underground", "minecraft:canyon"],
            "features": features})


# ---------------------------------------------------------------- NBT
def _s(s):
    b = s.encode("utf-8")
    return struct.pack(">H", len(b)) + b


def payload(tag, v):
    if tag == 3:
        return struct.pack(">i", v)
    if tag == 8:
        return _s(v)
    if tag == 9:
        t, items = v
        return bytes([t]) + struct.pack(">i", len(items)) + b"".join(payload(t, i) for i in items)
    if tag == 10:
        out = b""
        for k, (t, val) in v.items():
            out += bytes([t]) + _s(k) + payload(t, val)
        return out + b"\x00"
    raise ValueError(tag)


def write_nbt(path, root):
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = bytes([10]) + _s("") + payload(10, root)
    with gzip.GzipFile(filename="", mode="wb", fileobj=open(path, "wb"), mtime=0) as g:
        g.write(raw)


class Tpl:
    def __init__(self, sx, sy, sz):
        self.size = (sx, sy, sz)
        self.b = {}  # (x,y,z) -> (name, props, nbt)

    def set(self, x, y, z, name, props=None, nbt=None):
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.size[2]:
            self.b[(x, y, z)] = (name, props or {}, nbt)

    def fill(self, x0, y0, z0, x1, y1, z1, name, props=None):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.set(x, y, z, name, props)

    def box(self, x0, y0, z0, x1, y1, z1, wall, air=True):
        self.fill(x0, y0, z0, x1, y1, z1, wall)
        if air:
            self.fill(x0 + 1, y0 + 1, z0 + 1, x1 - 1, y1 - 1, z1 - 1, "minecraft:air")

    def save(self, name):
        palette, idx = [], {}
        blocks = []
        for pos, (n, p, nbt) in sorted(self.b.items()):
            key = (n, tuple(sorted(p.items())))
            if key not in idx:
                idx[key] = len(palette)
                e = {"Name": (8, n)}
                if p:
                    e["Properties"] = (10, {k: (8, v) for k, v in p.items()})
                palette.append(e)
            e = {"pos": (9, (3, list(pos))), "state": (3, idx[key])}
            if nbt:
                e["nbt"] = (10, {k: (8, v) for k, v in nbt.items()})
            blocks.append(e)
        root = {"DataVersion": (3, MC_DATA_VERSION),
                "size": (9, (3, list(self.size))),
                "palette": (9, (10, palette)),
                "blocks": (9, (10, blocks)),
                "entities": (9, (10, []))}
        write_nbt(DATA / f"structure/{name}.nbt", root)


def chest(loot, facing="south"):
    return ("minecraft:chest", {"facing": facing}, {"id": "minecraft:chest", "LootTable": loot})


def put_chest(t, x, y, z, loot, facing="south"):
    n, p, nbt = chest(loot, facing)
    t.set(x, y, z, n, p, nbt)


def build_crystal_tower():
    t = Tpl(9, 24, 9)
    P, L = f"{MOD}:crystal_planks", f"{MOD}:crystal_log"
    t.fill(0, 0, 0, 8, 0, 8, P)                    # base
    t.box(1, 0, 1, 7, 20, 7, P)                    # torre hueca
    for y in range(0, 21):                          # columnas de esquina
        for cx, cz in ((1, 1), (1, 7), (7, 1), (7, 7)):
            t.set(cx, y, cz, L, {"axis": "y"})
    for y in (6, 12, 18):                           # pisos
        t.fill(2, y, 2, 6, y, 6, P)
    for y in (3, 4, 9, 10, 15, 16):                 # ventanas
        for c in (2, 4, 6):
            t.set(1, y, c, "minecraft:glass"); t.set(7, y, c, "minecraft:glass")
            t.set(c, y, 1, "minecraft:glass"); t.set(c, y, 7, "minecraft:glass")
    t.set(4, 1, 7, "minecraft:air"); t.set(4, 2, 7, "minecraft:air")  # puerta
    for y in range(1, 20):                          # escalera continua
        t.set(4, y, 2, "minecraft:ladder", {"facing": "south"})
    put_chest(t, 3, 13, 4, "minecraft:chests/simple_dungeon")
    put_chest(t, 5, 19, 5, "minecraft:chests/simple_dungeon", "west")
    t.set(3, 7, 3, "minecraft:lantern", {"hanging": "false"})
    t.fill(1, 21, 1, 7, 21, 7, P)                   # techo escalonado
    t.fill(2, 22, 2, 6, 22, 6, P)
    t.fill(3, 23, 3, 5, 23, 5, "minecraft:sea_lantern")
    t.save("crystal_tower")


def stilt_hut(name, LG, PL, SLAB, ROOF):
    t = Tpl(9, 9, 9)
    for cx, cz in ((1, 1), (1, 7), (7, 1), (7, 7)):  # pilotes
        t.fill(cx, 0, cz, cx, 4, cz, LG, {"axis": "y"})
    t.fill(0, 4, 0, 8, 4, 8, PL)                     # plataforma
    t.fill(1, 5, 1, 7, 7, 7, PL)                     # paredes (luego se vacia)
    t.fill(2, 5, 2, 6, 7, 6, "minecraft:air")
    for cx, cz in ((1, 1), (1, 7), (7, 1), (7, 7)):
        t.fill(cx, 5, cz, cx, 7, cz, LG, {"axis": "y"})
    t.fill(0, 8, 0, 8, 8, 8, SLAB, {"type": "bottom"})  # techo
    t.fill(1, 8, 1, 7, 8, 7, ROOF)
    t.fill(2, 8, 2, 6, 8, 6, SLAB, {"type": "bottom"})
    for y in range(0, 4):                            # pilote del frente (apoyo de la escalera)
        t.set(4, y, 7, LG, {"axis": "y"})
    for y in range(0, 6):                            # escalera exterior
        t.set(4, y, 8, "minecraft:ladder", {"facing": "south"})
    t.set(3, 5, 7, "minecraft:air"); t.set(3, 6, 7, "minecraft:air")   # puerta
    for c in (2, 6):
        t.set(c, 6, 1, "minecraft:glass_pane"); t.set(c, 6, 7, "minecraft:glass_pane")
    t.set(2, 5, 2, "minecraft:cauldron")
    t.set(6, 5, 2, "minecraft:crafting_table")
    t.set(2, 5, 6, "minecraft:brewing_stand")
    put_chest(t, 6, 5, 6, "minecraft:chests/simple_dungeon", "west")
    t.set(4, 7, 2, "minecraft:lantern", {"hanging": "true"})
    t.save(name)


def build_witch_hut():
    stilt_hut("glow_witch_hut", "minecraft:dark_oak_log", "minecraft:dark_oak_planks",
              "minecraft:dark_oak_slab", f"{MOD}:glow_moss_block")


def build_mangrove_house():
    stilt_hut("mangrove_house", "minecraft:mangrove_log", "minecraft:mangrove_planks",
              "minecraft:mangrove_slab", "minecraft:shroomlight")


def build_inverted_pyramid():
    n = 21
    t = Tpl(n, 11, n)
    wall, glass = "minecraft:polished_blackstone_bricks", f"{MOD}:volcanic_glass"
    for y in range(0, 10):                           # capas: la punta abajo, ancha arriba
        w = 2 * y + 1
        o = 10 - y
        t.fill(o, y, o, o + w - 1, y, o + w - 1, wall)
        if w > 2:
            t.fill(o + 1, y, o + 1, o + w - 2, y, o + w - 2, "minecraft:air")
    t.fill(0, 10, 0, 20, 10, 20, glass)              # tapa
    t.fill(1, 10, 1, 19, 10, 19, "minecraft:blackstone")
    t.fill(9, 10, 9, 11, 10, 11, "minecraft:air")    # agujero de entrada
    put_chest(t, 10, 1, 10, "minecraft:chests/desert_pyramid", "north")
    t.set(10, 2, 10, "minecraft:water")              # amortigua la caida
    t.save("inverted_pyramid")


def build_amber_camp():
    t = Tpl(11, 6, 11)
    t.fill(0, 0, 0, 10, 0, 10, f"{MOD}:amber_permafrost")
    for z0 in (1, 7):                                # dos carpas
        for z in range(z0, z0 + 3):
            t.set(1, 1, z, "minecraft:orange_wool"); t.set(5, 1, z, "minecraft:orange_wool")
            t.set(2, 2, z, "minecraft:orange_wool"); t.set(4, 2, z, "minecraft:orange_wool")
            t.set(3, 3, z, "minecraft:orange_wool")
            for x in (2, 3, 4):
                t.set(x, 1, z, "minecraft:white_carpet")
    t.set(3, 0, 4, "minecraft:stone")
    t.set(3, 1, 4, "minecraft:campfire")
    for y in range(1, 5):                            # totem de ambar
        t.set(8, y, 5, f"{MOD}:amber_block")
    t.set(8, 5, 5, "minecraft:lantern", {"hanging": "false"})
    t.set(9, 1, 7, "minecraft:barrel", {"facing": "up"})
    t.set(9, 1, 8, "minecraft:barrel", {"facing": "up"})
    put_chest(t, 9, 1, 2, "minecraft:chests/simple_dungeon", "west")
    t.set(7, 1, 3, "minecraft:spruce_log", {"axis": "x"})
    t.set(7, 1, 4, "minecraft:spruce_log", {"axis": "x"})
    t.save("amber_camp")


def build_fungal_village():
    t = Tpl(19, 10, 11)
    t.fill(0, 0, 0, 18, 0, 10, "minecraft:dirt_path")
    S, C = "minecraft:mushroom_stem", "minecraft:red_mushroom_block"
    for hx in (2, 11):                               # dos casas-hongo
        t.box(hx, 0, 2, hx + 4, 4, 6, S)
        t.set(hx + 2, 1, 6, "minecraft:air"); t.set(hx + 2, 2, 6, "minecraft:air")  # puerta
        t.set(hx + 2, 2, 2, "minecraft:glass_pane")
        for dx in range(-1, 6):                      # sombrero 7x7 sin esquinas
            for dz in range(1, 8):
                if not (dx in (-1, 5) and dz in (1, 7)):
                    t.set(hx + dx, 5, dz, C)
        for dx in range(0, 5):
            for dz in range(2, 7):
                t.set(hx + dx, 6, dz, C)
        t.fill(hx + 1, 7, 3, hx + 3, 7, 5, C)
        t.set(hx + 2, 3, 4, "minecraft:lantern", {"hanging": "true"})
        t.set(hx + 1, 1, 3, "minecraft:crafting_table")
    put_chest(t, 14, 1, 5, "minecraft:chests/simple_dungeon", "west")
    t.set(9, 1, 5, f"{MOD}:spore_stem", {"axis": "y"})
    t.set(9, 2, 5, f"{MOD}:spore_stem", {"axis": "y"})
    t.set(9, 3, 5, "minecraft:lantern", {"hanging": "false"})
    t.save("fungal_village")


# estructura -> (bioma, spacing, separation, salt, adaptation, builder)
STRUCTURES = {
    "crystal_tower": ("crystal_forest", 22, 8, 1011, "beard_thin", build_crystal_tower),
    "glow_witch_hut": ("glow_swamp", 18, 6, 1012, "beard_thin", build_witch_hut),
    "inverted_pyramid": ("obsidian_desert", 28, 10, 1013, "none", build_inverted_pyramid),
    "amber_camp": ("amber_tundra", 16, 6, 1014, "beard_thin", build_amber_camp),
    "fungal_village": ("fungal_jungle", 20, 7, 1015, "beard_thin", build_fungal_village),
}


def gen_structures():
    for name, (biome, spacing, sep, salt, adapt, builder) in STRUCTURES.items():
        builder()
        wjson(DATA / f"worldgen/structure/{name}.json", {
            "type": "minecraft:jigsaw", "biomes": [f"{MOD}:{biome}"],
            "step": "surface_structures", "spawn_overrides": {},
            "terrain_adaptation": adapt, "start_pool": f"{MOD}:{name}/start",
            "size": 1, "start_height": {"absolute": -1},
            "project_start_to_heightmap": "WORLD_SURFACE_WG",
            "max_distance_from_center": 80, "use_expansion_hack": False})
        wjson(DATA / f"worldgen/template_pool/{name}/start.json", {
            "fallback": "minecraft:empty",
            "elements": [{"weight": 1, "element": {
                "element_type": "minecraft:single_pool_element",
                "location": f"{MOD}:{name}", "processors": "minecraft:empty",
                "projection": "rigid"}}]})
        wjson(DATA / f"worldgen/structure_set/{name}.json", {
            "structures": [{"structure": f"{MOD}:{name}", "weight": 1}],
            "placement": {"type": "minecraft:random_spread", "spacing": spacing,
                          "separation": sep, "salt": salt}})


# ======================================================= LOTE 2 (biomas 6-15)
BLOCKS.update({
    "cloud_block": dict(es="Bloque de nube", en="Cloud Block", kind="cube",
                        pal=[(245, 250, 255), (230, 240, 250), (215, 230, 245), (255, 255, 255)], tool="hoe"),
    "crimson_rock": dict(es="Roca carmesí", en="Crimson Rock", kind="planks",
                         pal=[(170, 60, 50), (150, 45, 40), (185, 80, 60), (130, 40, 40)], tool="pickaxe"),
    "silver_log": dict(es="Tronco plateado", en="Silver Log", kind="pillar",
                       side=[(190, 195, 205), (160, 170, 185), (130, 140, 155)],
                       top=[(220, 225, 235), (190, 195, 210), (150, 160, 175)], tool="axe"),
    "silver_leaves": dict(es="Hojas plateadas", en="Silver Leaves", kind="leaves",
                          pal=[(140, 180, 170), (170, 210, 200), (110, 150, 145), (200, 235, 225)], tool="hoe"),
    "baobab_log": dict(es="Tronco de baobab", en="Baobab Log", kind="pillar",
                       side=[(120, 90, 70), (100, 75, 58), (140, 105, 80)],
                       top=[(170, 140, 100), (140, 110, 80), (100, 75, 58)], tool="axe"),
    "autumn_leaves_orange": dict(es="Hojas otoñales naranjas", en="Orange Autumn Leaves", kind="leaves",
                                 pal=[(230, 130, 30), (250, 160, 50), (200, 100, 20), (255, 185, 80)], tool="hoe"),
    "autumn_leaves_red": dict(es="Hojas otoñales rojas", en="Red Autumn Leaves", kind="leaves",
                              pal=[(190, 40, 30), (220, 70, 40), (160, 30, 25), (235, 100, 60)], tool="hoe"),
    "pink_sand": dict(es="Arena rosa", en="Pink Sand", kind="sand",
                      pal=[(235, 175, 190), (245, 195, 205), (220, 160, 178), (250, 210, 218)], tool="shovel"),
    "pearl_block": dict(es="Bloque de perla", en="Pearl Block", kind="cube",
                        pal=[(240, 235, 245), (225, 220, 240), (250, 245, 255), (215, 205, 235)], tool="pickaxe"),
    "golden_mud": dict(es="Lodo dorado", en="Golden Mud", kind="cube",
                       pal=[(190, 150, 50), (170, 130, 40), (210, 175, 70)], tool="shovel"),
    "salt_block": dict(es="Bloque de sal", en="Salt Block", kind="cube",
                       pal=[(245, 245, 240), (230, 230, 225), (250, 250, 248), (215, 215, 212)], tool="pickaxe"),
    "glacial_ice": dict(es="Hielo glacial", en="Glacial Ice", kind="cube",
                        pal=[(130, 185, 235), (110, 165, 225), (150, 205, 245), (95, 145, 210)], tool="pickaxe"),
    "magma_basalt": dict(es="Basalto magmático", en="Magma Basalt", kind="cube",
                         pal=[(40, 35, 38), (60, 40, 35), (190, 70, 25), (45, 40, 42)], tool="pickaxe"),
})

EXTRA_TAGS = {
    "mineable/axe": ["silver_log", "baobab_log"],
    "mineable/hoe": ["silver_leaves", "autumn_leaves_orange", "autumn_leaves_red", "cloud_block"],
    "mineable/shovel": ["pink_sand", "golden_mud"],
    "mineable/pickaxe": ["crimson_rock", "pearl_block", "salt_block", "glacial_ice", "magma_basalt"],
    "logs": ["silver_log", "baobab_log"], "logs_that_burn": ["silver_log", "baobab_log"],
    "leaves": ["silver_leaves", "autumn_leaves_orange", "autumn_leaves_red"],
    "sand": ["pink_sand"], "dry_vegetation_may_place_on": ["pink_sand", "salt_block"],
    "dirt": ["golden_mud"], "animals_spawnable_on": ["golden_mud"],
}

BIOME_NAMES.update({
    "sky_meadow": ("Pradera Celeste", "Sky Meadow"),
    "crimson_canyon": ("Cañón Carmesí", "Crimson Canyon"),
    "silver_taiga": ("Taiga Plateada", "Silver Taiga"),
    "baobab_savanna": ("Sabana de Baobabs", "Baobab Savanna"),
    "autumn_forest": ("Bosque Otoñal", "Autumn Forest"),
    "pearl_coast": ("Costa de Perlas", "Pearl Coast"),
    "golden_mangrove": ("Manglar Dorado", "Golden Mangrove"),
    "salt_flats": ("Salinas Espejo", "Mirror Salt Flats"),
    "blue_glacier": ("Glaciar Azul", "Blue Glacier"),
    "volcanic_caldera": ("Caldera Volcánica", "Volcanic Caldera"),
})

BIOMES.update({
    "sky_meadow": dict(temp=0.5, down=0.4, rain=True, sky="A8C8FF", fog="E8F0FF", water="5FA8F0", water_fog="2F6FC0",
                       grass="B79CFF", foliage="B79CFF",
                       veg=[f"{MOD}:sky_flowers", f"{MOD}:sky_grass"], top=[],
                       creature=[mob("sheep", 12, 4, 4), mob("rabbit", 8, 2, 3), mob("horse", 5, 2, 4)],
                       monster=monsters()),
    "crimson_canyon": dict(temp=1.6, down=0.0, rain=False, sky="E08A6A", fog="F0B090", water="9A4A5A", water_fog="4A1A2A",
                           grass="A0503A", foliage="A0503A",
                           veg=[f"{MOD}:canyon_dead_bush"], top=[],
                           creature=[mob("rabbit", 4, 2, 3), mob("armadillo", 6, 1, 2)],
                           monster=monsters(zombie="husk")),
    "silver_taiga": dict(temp=-0.1, down=0.5, rain=True, sky="A0B8D0", fog="C8D8E8", water="6A9AC0", water_fog="3A6080",
                         grass="8FB0A8", foliage="8FB0A8",
                         veg=[f"{MOD}:silver_pine", f"{MOD}:silver_ferns"], top=[],
                         creature=[mob("wolf", 8, 4, 4), mob("rabbit", 8, 2, 3), mob("fox", 6, 1, 2)],
                         monster=monsters()),
    "baobab_savanna": dict(temp=1.2, down=0.0, rain=False, sky="FFD08A", fog="FFE8B0", water="3FA8A0", water_fog="1F6860",
                           grass="C8B040", foliage="B0A030",
                           veg=[f"{MOD}:baobab", f"{MOD}:savanna_grass"], top=[],
                           creature=[mob("horse", 1, 2, 6), mob("donkey", 1, 1, 1), mob("armadillo", 10, 2, 3)],
                           monster=monsters(zombie="husk")),
    "autumn_forest": dict(temp=0.4, down=0.6, rain=True, sky="FFB878", fog="FFD8A8", water="6A7A60", water_fog="3A4A30",
                          grass="D08030", foliage="D07020",
                          veg=[f"{MOD}:autumn_orange", f"{MOD}:autumn_red", f"{MOD}:autumn_grass"], top=[],
                          creature=[mob("pig", 10, 4, 4), mob("cow", 8, 4, 4), mob("chicken", 10, 4, 4)],
                          monster=monsters()),
    "pearl_coast": dict(temp=0.9, down=0.5, rain=True, sky="FFD0E0", fog="FFE8F0", water="5AD0E0", water_fog="2A90A0",
                        grass="A8D890", foliage="98C880",
                        veg=[f"{MOD}:pearl_clusters"], top=[],
                        creature=[mob("turtle", 5, 2, 5)], monster=monsters()),
    "golden_mangrove": dict(temp=0.9, down=0.9, rain=True, sky="E8D060", fog="F0E080", water="D0A840", water_fog="806820",
                            grass="C8B030", foliage="C0A828",
                            veg=[f"{MOD}:golden_mangrove_tree"], top=[],
                            creature=[mob("frog", 10, 2, 5)], monster=monsters([mob("slime", 1, 1, 1)])),
    "salt_flats": dict(temp=1.3, down=0.0, rain=False, sky="E8F0F8", fog="F8FFFF", water="9AC8D8", water_fog="5A8898",
                       grass="D8D8C0", foliage="C8C8A8",
                       veg=[f"{MOD}:salt_dead_bush"], top=[], creature=[],
                       monster=monsters(zombie="husk")),
    "blue_glacier": dict(temp=-0.8, down=0.5, rain=True, sky="80B8FF", fog="B8D8FF", water="3A70D0", water_fog="1A3A90",
                         grass="A0C8E0", foliage="A0C8E0",
                         veg=[], top=["minecraft:freeze_top_layer"],
                         creature=[mob("polar_bear", 1, 1, 2), mob("fox", 6, 1, 2)],
                         monster=monsters(skeleton="stray")),
    "volcanic_caldera": dict(temp=1.8, down=0.0, rain=False, sky="5A2A2A", fog="902A1A", water="C04020", water_fog="602010",
                             grass="5A4A40", foliage="5A4A40",
                             veg=[f"{MOD}:caldera_boulders"], top=[], creature=[],
                             monster=monsters([mob("magma_cube", 20, 2, 4)], zombie="husk")),
})


def tree2(name, log, leaf, base, ra, radius, fh, count):
    configured(name, {"type": "minecraft:tree", "config": {
        "trunk_provider": simple(log, {"axis": "y"}),
        "trunk_placer": {"type": "minecraft:straight_trunk_placer",
                         "base_height": base, "height_rand_a": ra, "height_rand_b": 0},
        "foliage_provider": simple(leaf, {"distance": "7", "persistent": "false", "waterlogged": "false"}),
        "foliage_placer": {"type": "minecraft:blob_foliage_placer", "radius": radius, "offset": 0, "height": fh},
        "minimum_size": {"type": "minecraft:two_layers_feature_size", "limit": 1, "lower_size": 0, "upper_size": 1},
        "dirt_provider": simple("minecraft:dirt"), "ignore_vines": True}})
    placed(name, f"{MOD}:{name}", tree_placement(count))


def patch2(name, block, tries, spread, count, rarity=None, solid=False):
    configured(name, patch_cfg(block, tries, spread, solid))
    placed(name, f"{MOD}:{name}", patch_placement(count, rarity))


def gen_features_2():
    patch2("sky_flowers", "minecraft:allium", 24, 6, 2)
    patch2("sky_grass", "minecraft:short_grass", 40, 7, 3)
    patch2("canyon_dead_bush", "minecraft:dead_bush", 20, 6, 2)
    tree2("silver_pine", f"{MOD}:silver_log", f"{MOD}:silver_leaves", 7, 4, 2, 4, 6)
    patch2("silver_ferns", "minecraft:fern", 32, 7, 2)
    tree2("baobab", f"{MOD}:baobab_log", "minecraft:acacia_leaves", 9, 3, 3, 3, 1)
    patch2("savanna_grass", "minecraft:short_grass", 40, 7, 4)
    tree2("autumn_orange", "minecraft:oak_log", f"{MOD}:autumn_leaves_orange", 5, 2, 2, 3, 3)
    tree2("autumn_red", "minecraft:oak_log", f"{MOD}:autumn_leaves_red", 5, 2, 2, 3, 3)
    patch2("autumn_grass", "minecraft:short_grass", 32, 7, 2)
    patch2("pearl_clusters", f"{MOD}:pearl_block", 3, 4, 1, 4, True)
    placed("golden_mangrove_tree", "minecraft:mangrove", tree_placement(3))
    patch2("salt_dead_bush", "minecraft:dead_bush", 12, 6, 1, 2)
    patch2("caldera_boulders", "minecraft:blackstone", 5, 3, 2, None, True)


# ---- estructuras del lote 2
def room(t, x0, y0, z0, w, h, d, wall, floor=None, roof=None, pillar=None, pillar_props=None):
    t.fill(x0, y0, z0, x0 + w - 1, y0 + h - 1, z0 + d - 1, wall)
    t.fill(x0 + 1, y0 + 1, z0 + 1, x0 + w - 2, y0 + h - 2, z0 + d - 2, "minecraft:air")
    if floor:
        t.fill(x0, y0, z0, x0 + w - 1, y0, z0 + d - 1, floor)
    if roof:
        t.fill(x0, y0 + h - 1, z0, x0 + w - 1, y0 + h - 1, z0 + d - 1, roof)
    if pillar:
        pp = {"axis": "y"} if pillar_props is None else pillar_props
        for cx, cz in ((x0, z0), (x0, z0 + d - 1), (x0 + w - 1, z0), (x0 + w - 1, z0 + d - 1)):
            t.fill(cx, y0, cz, cx, y0 + h - 1, cz, pillar, pp)
    cx = x0 + w // 2
    t.set(cx, y0 + 1, z0 + d - 1, "minecraft:air")
    t.set(cx, y0 + 2, z0 + d - 1, "minecraft:air")
    if h >= 5:
        for z in range(z0 + 2, z0 + d - 2, 2):
            t.set(x0, y0 + 2, z, "minecraft:glass_pane")
            t.set(x0 + w - 1, y0 + 2, z, "minecraft:glass_pane")
        t.set(cx, y0 + h - 2, z0 + d // 2, "minecraft:lantern", {"hanging": "true"})


SD = "minecraft:chests/simple_dungeon"


def build_wind_shrine():
    t = Tpl(11, 8, 11)
    t.fill(0, 0, 0, 10, 0, 10, f"{MOD}:cloud_block")
    for cx, cz in ((2, 2), (2, 8), (8, 2), (8, 8)):
        t.fill(cx, 1, cz, cx, 5, cz, "minecraft:quartz_pillar", {"axis": "y"})
    t.fill(1, 6, 1, 9, 6, 9, "minecraft:quartz_slab", {"type": "bottom"})
    t.fill(2, 6, 2, 8, 6, 8, "minecraft:quartz_block")
    t.set(5, 1, 5, "minecraft:quartz_block")
    put_chest(t, 5, 2, 5, SD)
    t.set(5, 5, 5, "minecraft:lantern", {"hanging": "true"})
    t.save("wind_shrine")


def build_canyon_ruins():
    t = Tpl(13, 6, 13)
    r = random.Random(7)
    W = f"{MOD}:crimson_rock"
    t.fill(0, 0, 0, 12, 0, 12, "minecraft:red_terracotta")
    for i in range(13):
        for x, z in ((i, 0), (i, 12), (0, i), (12, i)):
            for y in range(1, r.randint(1, 4) + 1):
                t.set(x, y, z, W if r.random() > 0.3 else "minecraft:red_sandstone")
    for cx, cz in ((0, 0), (0, 12), (12, 0), (12, 12)):
        t.fill(cx, 1, cz, cx, 5, cz, "minecraft:chiseled_red_sandstone")
    for y in range(1, 5):
        t.set(6, y, 12, "minecraft:air")
    put_chest(t, 6, 1, 6, SD)
    t.set(6, 1, 8, "minecraft:red_sandstone_slab", {"type": "bottom"})
    t.save("canyon_ruins")


def build_hunter_cabin():
    t = Tpl(9, 7, 9)
    room(t, 1, 0, 1, 7, 6, 7, "minecraft:spruce_planks", "minecraft:spruce_planks",
         "minecraft:spruce_planks", f"{MOD}:silver_log")
    put_chest(t, 2, 1, 2, SD, "east")
    t.set(6, 1, 2, "minecraft:furnace", {"facing": "south"})
    t.set(2, 1, 6, "minecraft:crafting_table")
    t.save("hunter_cabin")


def build_tribal_village():
    t = Tpl(19, 7, 9)
    t.fill(0, 0, 0, 18, 0, 8, "minecraft:coarse_dirt")
    for hx in (1, 11):
        room(t, hx, 0, 1, 7, 5, 7, "minecraft:orange_terracotta", "minecraft:acacia_planks",
             "minecraft:hay_block", f"{MOD}:baobab_log")
    put_chest(t, 2, 1, 2, SD, "east")
    put_chest(t, 12, 1, 2, SD, "east")
    t.set(9, 0, 4, "minecraft:stone")
    t.set(9, 1, 4, "minecraft:campfire")
    for y in range(1, 4):
        t.set(9, y, 7, f"{MOD}:baobab_log", {"axis": "y"})
    t.set(9, 4, 7, "minecraft:lantern", {"hanging": "false"})
    t.save("tribal_village")


def build_abandoned_mill():
    t = Tpl(11, 12, 8)
    room(t, 3, 0, 2, 5, 9, 5, "minecraft:oak_planks", "minecraft:cobblestone",
         "minecraft:oak_planks", "minecraft:oak_log")
    put_chest(t, 4, 1, 3, SD, "east")
    for x in range(0, 11):
        t.set(x, 6, 1, "minecraft:oak_fence")
    for y in range(1, 12):
        t.set(5, y, 1, "minecraft:oak_fence")
    t.set(5, 6, 1, "minecraft:oak_log", {"axis": "z"})
    t.save("abandoned_mill")


def build_pearl_lighthouse():
    t = Tpl(7, 19, 7)
    room(t, 1, 0, 1, 5, 16, 5, "minecraft:white_concrete", "minecraft:quartz_block", None,
         f"{MOD}:pearl_block", {})
    for y in range(1, 17):
        t.set(3, y, 2, "minecraft:ladder", {"facing": "south"})
    t.set(3, 15, 3, "minecraft:white_concrete")
    t.fill(1, 16, 1, 5, 17, 5, "minecraft:glass")
    t.fill(2, 16, 2, 4, 17, 4, "minecraft:air")
    t.set(3, 16, 2, "minecraft:ladder", {"facing": "south"})
    t.set(3, 16, 3, "minecraft:sea_lantern")
    put_chest(t, 4, 16, 4, SD, "west")
    t.fill(0, 18, 0, 6, 18, 6, "minecraft:quartz_slab", {"type": "bottom"})
    t.fill(1, 18, 1, 5, 18, 5, "minecraft:quartz_block")
    t.save("pearl_lighthouse")


def build_salt_temple():
    t = Tpl(15, 8, 15)
    S = f"{MOD}:salt_block"
    for sz, y0, y1 in ((15, 0, 1), (11, 2, 3), (7, 4, 5), (3, 6, 6)):
        o = (15 - sz) // 2
        t.fill(o, y0, o, o + sz - 1, y1, o + sz - 1, S)
    t.fill(6, 1, 6, 8, 2, 8, "minecraft:air")
    t.fill(7, 1, 9, 7, 2, 14, "minecraft:air")
    put_chest(t, 7, 1, 7, "minecraft:chests/desert_pyramid", "south")
    t.set(7, 2, 8, "minecraft:lantern", {"hanging": "true"})
    t.save("salt_temple")


def build_ice_crypt():
    t = Tpl(11, 7, 11)
    room(t, 1, 0, 1, 9, 6, 9, f"{MOD}:glacial_ice", "minecraft:packed_ice", "minecraft:packed_ice",
         "minecraft:blue_ice", {})
    put_chest(t, 2, 1, 2, SD, "east")
    put_chest(t, 8, 1, 8, SD, "west")
    for z in (4, 6):
        t.fill(5, 1, z, 5, 2, z, "minecraft:blue_ice")
    t.save("ice_crypt")


def build_dwarf_forge():
    t = Tpl(13, 8, 11)
    room(t, 1, 0, 1, 11, 7, 9, "minecraft:polished_blackstone_bricks", f"{MOD}:magma_basalt",
         "minecraft:polished_blackstone", "minecraft:polished_basalt")
    t.fill(4, 1, 3, 8, 1, 5, "minecraft:polished_blackstone")
    t.fill(5, 1, 4, 7, 1, 4, "minecraft:lava")
    t.set(3, 1, 7, "minecraft:anvil", {"facing": "east"})
    t.set(10, 1, 7, "minecraft:blast_furnace", {"facing": "north"})
    put_chest(t, 2, 1, 2, SD, "east")
    t.save("dwarf_forge")


STRUCTURES.update({
    "wind_shrine": ("sky_meadow", 24, 8, 1016, "beard_thin", build_wind_shrine),
    "canyon_ruins": ("crimson_canyon", 22, 8, 1017, "beard_thin", build_canyon_ruins),
    "hunter_cabin": ("silver_taiga", 18, 6, 1018, "beard_thin", build_hunter_cabin),
    "tribal_village": ("baobab_savanna", 24, 8, 1019, "beard_thin", build_tribal_village),
    "abandoned_mill": ("autumn_forest", 20, 7, 1020, "beard_thin", build_abandoned_mill),
    "pearl_lighthouse": ("pearl_coast", 20, 7, 1021, "beard_thin", build_pearl_lighthouse),
    "mangrove_house": ("golden_mangrove", 16, 6, 1022, "beard_thin", build_mangrove_house),
    "salt_temple": ("salt_flats", 28, 10, 1023, "beard_thin", build_salt_temple),
    "ice_crypt": ("blue_glacier", 22, 8, 1024, "beard_thin", build_ice_crypt),
    "dwarf_forge": ("volcanic_caldera", 24, 8, 1025, "beard_thin", build_dwarf_forge),
})


if __name__ == "__main__":
    gen_blocks()
    gen_tags()
    gen_lang()
    gen_features()
    gen_features_2()
    gen_biomes()
    gen_structures()
    print("Listo: recursos generados en", RES)
