package com.biomassalvajes.worldgen;

import com.biomassalvajes.BiomasSalvajes;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.biome.Biome;

/** Claves de los biomas. Las definiciones JSON se generan con tools/generate.py. */
public class ModBiomes {
    public static final ResourceKey<Biome> CRYSTAL_FOREST = key("crystal_forest");
    public static final ResourceKey<Biome> GLOW_SWAMP = key("glow_swamp");
    public static final ResourceKey<Biome> OBSIDIAN_DESERT = key("obsidian_desert");
    public static final ResourceKey<Biome> AMBER_TUNDRA = key("amber_tundra");
    public static final ResourceKey<Biome> FUNGAL_JUNGLE = key("fungal_jungle");

    public static final ResourceKey<Biome> SKY_MEADOW = key("sky_meadow");
    public static final ResourceKey<Biome> CRIMSON_CANYON = key("crimson_canyon");
    public static final ResourceKey<Biome> SILVER_TAIGA = key("silver_taiga");
    public static final ResourceKey<Biome> BAOBAB_SAVANNA = key("baobab_savanna");
    public static final ResourceKey<Biome> AUTUMN_FOREST = key("autumn_forest");
    public static final ResourceKey<Biome> PEARL_COAST = key("pearl_coast");
    public static final ResourceKey<Biome> GOLDEN_MANGROVE = key("golden_mangrove");
    public static final ResourceKey<Biome> SALT_FLATS = key("salt_flats");
    public static final ResourceKey<Biome> BLUE_GLACIER = key("blue_glacier");
    public static final ResourceKey<Biome> VOLCANIC_CALDERA = key("volcanic_caldera");

    private static ResourceKey<Biome> key(String name) {
        return ResourceKey.create(Registries.BIOME, BiomasSalvajes.id(name));
    }
}
