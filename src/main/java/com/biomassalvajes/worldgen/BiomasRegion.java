package com.biomassalvajes.worldgen;

import com.mojang.datafixers.util.Pair;
import java.util.function.Consumer;
import net.minecraft.core.Registry;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.biome.Climate;
import net.minecraft.world.level.biome.Climate.Parameter;
import terrablender.api.Region;
import terrablender.api.RegionType;

/**
 * Región de TerraBlender con todos los biomas del mod.
 * El peso decide cuánto del mundo ocupa frente a los biomas vanilla (peso vanilla = 10 por defecto).
 */
public class BiomasRegion extends Region {
    public BiomasRegion(ResourceLocation name, int weight) {
        super(name, RegionType.OVERWORLD, weight);
    }

    @Override
    public void addBiomes(Registry<Biome> registry, Consumer<Pair<Climate.ParameterPoint, ResourceKey<Biome>>> mapper) {
        // add(mapper, bioma, temperatura, humedad, continentalidad, erosión, rareza)
        add(mapper, ModBiomes.CRYSTAL_FOREST,   span(-0.15F, 0.20F), span(0.10F, 0.50F), span(-0.11F, 1.0F), span(-0.5F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.GLOW_SWAMP,       span(0.20F, 0.55F),  span(0.30F, 1.00F), span(-0.11F, 0.30F), span(0.45F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.OBSIDIAN_DESERT,  span(0.55F, 1.00F),  span(-1.0F, -0.35F), span(-0.10F, 1.0F), span(-0.2F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.AMBER_TUNDRA,     span(-1.0F, -0.45F), span(-0.35F, 0.30F), span(-0.10F, 1.0F), span(-1.0F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.FUNGAL_JUNGLE,    span(0.55F, 1.00F),  span(0.30F, 1.00F), span(0.03F, 1.0F),  span(-1.0F, 0.2F), span(-1.0F, 1.0F));
        // ---- Lote 2
        add(mapper, ModBiomes.SKY_MEADOW,       span(0.00F, 0.40F),  span(-0.10F, 0.30F), span(0.03F, 1.0F),  span(0.20F, 0.80F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.CRIMSON_CANYON,   span(0.55F, 1.00F),  span(-0.35F, 0.10F), span(0.30F, 1.0F),  span(-1.0F, -0.2F), span(-1.0F, 0.3F));
        add(mapper, ModBiomes.SILVER_TAIGA,     span(-0.45F, -0.15F), span(0.10F, 0.60F), span(-0.10F, 1.0F), span(-1.0F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.BAOBAB_SAVANNA,   span(0.55F, 1.00F),  span(-0.10F, 0.30F), span(-0.10F, 1.0F), span(0.20F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.AUTUMN_FOREST,    span(-0.15F, 0.20F), span(-0.10F, 0.30F), span(-0.10F, 1.0F), span(-1.0F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.PEARL_COAST,      span(0.20F, 0.55F),  span(-0.35F, 0.10F), span(-0.45F, -0.11F), span(0.55F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.GOLDEN_MANGROVE,  span(0.55F, 1.00F),  span(0.30F, 1.00F), span(-0.19F, 0.00F), span(0.45F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.SALT_FLATS,       span(0.20F, 0.55F),  span(-1.0F, -0.35F), span(-0.10F, 0.30F), span(0.55F, 1.0F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.BLUE_GLACIER,     span(-1.0F, -0.45F), span(0.30F, 1.00F), span(0.30F, 1.0F),  span(-1.0F, 0.2F), span(-1.0F, 1.0F));
        add(mapper, ModBiomes.VOLCANIC_CALDERA, span(0.55F, 1.00F),  span(-0.35F, 0.10F), span(0.55F, 1.0F),  span(-1.0F, -0.2F), span(0.3F, 1.0F));
    }

    private static Parameter span(float min, float max) {
        return Parameter.span(min, max);
    }

    private static void add(Consumer<Pair<Climate.ParameterPoint, ResourceKey<Biome>>> mapper, ResourceKey<Biome> biome,
                            Parameter temperature, Parameter humidity, Parameter continentalness,
                            Parameter erosion, Parameter weirdness) {
        // depth 0.0 = superficie
        mapper.accept(Pair.of(
                Climate.parameters(temperature, humidity, continentalness, erosion, Parameter.point(0.0F), weirdness, 0.0F),
                biome));
    }
}
