package com.biomassalvajes.worldgen;

import com.biomassalvajes.block.ModBlocks;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.levelgen.Noises;
import net.minecraft.world.level.levelgen.SurfaceRules;

/** Qué bloques forman la superficie de cada bioma. Lo que no se define aquí usa la superficie vanilla. */
public class ModSurfaceRules {
    private static SurfaceRules.RuleSource block(Block b) {
        return SurfaceRules.state(b.defaultBlockState());
    }

    /** Manchas según ruido (SURFACE_SECONDARY). */
    private static SurfaceRules.ConditionSource noise(double min, double max) {
        return SurfaceRules.noiseCondition(Noises.SURFACE_SECONDARY, min, max);
    }

    /** Solo cambia el bloque de arriba; el resto queda vanilla. */
    private static SurfaceRules.RuleSource top(ResourceKey<Biome> key, SurfaceRules.RuleSource top) {
        return SurfaceRules.ifTrue(SurfaceRules.isBiome(key), SurfaceRules.ifTrue(SurfaceRules.ON_FLOOR, top));
    }

    /** Cambia el bloque de arriba y el de debajo. */
    private static SurfaceRules.RuleSource biome(ResourceKey<Biome> key, SurfaceRules.RuleSource top,
                                                 SurfaceRules.RuleSource under) {
        return SurfaceRules.ifTrue(SurfaceRules.isBiome(key), SurfaceRules.sequence(
                SurfaceRules.ifTrue(SurfaceRules.ON_FLOOR, top),
                SurfaceRules.ifTrue(SurfaceRules.UNDER_FLOOR, under)));
    }

    private static SurfaceRules.RuleSource vanilla(Block b) {
        return SurfaceRules.state(b.defaultBlockState());
    }

    public static SurfaceRules.RuleSource makeRules() {
        return SurfaceRules.sequence(
                // Bosque de Cristal: hierba y tierra vanilla (el color viene del bioma).

                // Pantano: lodo azul con manchas de musgo luminoso
                biome(ModBiomes.GLOW_SWAMP,
                        SurfaceRules.sequence(
                                SurfaceRules.ifTrue(noise(0.35D, 1.0D), block(ModBlocks.GLOW_MOSS_BLOCK)),
                                block(ModBlocks.BLUE_MUD)),
                        block(ModBlocks.BLUE_MUD)),
                // Desierto de Obsidiana
                biome(ModBiomes.OBSIDIAN_DESERT,
                        SurfaceRules.sequence(
                                SurfaceRules.ifTrue(noise(0.55D, 1.0D), block(ModBlocks.VOLCANIC_GLASS)),
                                block(ModBlocks.BLACK_SAND)),
                        vanilla(Blocks.BLACKSTONE)),
                // Tundra de Ámbar
                biome(ModBiomes.AMBER_TUNDRA,
                        SurfaceRules.sequence(
                                SurfaceRules.ifTrue(noise(0.45D, 1.0D), vanilla(Blocks.SNOW_BLOCK)),
                                block(ModBlocks.AMBER_PERMAFROST)),
                        vanilla(Blocks.DIRT)),
                // Jungla fúngica
                biome(ModBiomes.FUNGAL_JUNGLE, block(ModBlocks.RED_MYCELIUM), vanilla(Blocks.DIRT)),

                // ---- Lote 2
                top(ModBiomes.SKY_MEADOW, SurfaceRules.ifTrue(noise(0.50D, 1.0D), block(ModBlocks.CLOUD_BLOCK))),
                biome(ModBiomes.CRIMSON_CANYON,
                        SurfaceRules.sequence(
                                SurfaceRules.ifTrue(noise(0.30D, 1.0D), vanilla(Blocks.RED_SAND)),
                                block(ModBlocks.CRIMSON_ROCK)),
                        block(ModBlocks.CRIMSON_ROCK)),
                top(ModBiomes.SILVER_TAIGA, SurfaceRules.ifTrue(noise(0.35D, 1.0D), vanilla(Blocks.PODZOL))),
                top(ModBiomes.BAOBAB_SAVANNA, SurfaceRules.ifTrue(noise(0.30D, 1.0D), vanilla(Blocks.COARSE_DIRT))),
                top(ModBiomes.AUTUMN_FOREST, SurfaceRules.ifTrue(noise(0.35D, 1.0D), vanilla(Blocks.PODZOL))),
                biome(ModBiomes.PEARL_COAST,
                        SurfaceRules.sequence(
                                SurfaceRules.ifTrue(noise(0.55D, 1.0D), block(ModBlocks.PEARL_BLOCK)),
                                block(ModBlocks.PINK_SAND)),
                        block(ModBlocks.PINK_SAND)),
                biome(ModBiomes.GOLDEN_MANGROVE, block(ModBlocks.GOLDEN_MUD), block(ModBlocks.GOLDEN_MUD)),
                biome(ModBiomes.SALT_FLATS, block(ModBlocks.SALT_BLOCK), block(ModBlocks.SALT_BLOCK)),
                biome(ModBiomes.BLUE_GLACIER,
                        SurfaceRules.sequence(
                                SurfaceRules.ifTrue(noise(0.40D, 1.0D), block(ModBlocks.GLACIAL_ICE)),
                                vanilla(Blocks.SNOW_BLOCK)),
                        vanilla(Blocks.PACKED_ICE)),
                biome(ModBiomes.VOLCANIC_CALDERA,
                        SurfaceRules.sequence(
                                SurfaceRules.ifTrue(noise(0.50D, 1.0D), vanilla(Blocks.MAGMA_BLOCK)),
                                block(ModBlocks.MAGMA_BASALT)),
                        vanilla(Blocks.BASALT)));
    }
}
