package com.biomassalvajes.block;

import com.biomassalvajes.BiomasSalvajes;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.ColorRGBA;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.ColoredFallingBlock;
import net.minecraft.world.level.block.TintedParticleLeavesBlock;
import net.minecraft.world.level.block.RotatedPillarBlock;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;

public class ModBlocks {
    /** Todos los bloques del mod, en orden de registro (se usan para la pestaña creativa). */
    public static final Map<String, Block> ALL = new LinkedHashMap<>();

    // ---- Bosque de Cristal
    public static final Block CRYSTAL_LOG = reg("crystal_log", RotatedPillarBlock::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_CYAN).strength(2.0F).sound(SoundType.WOOD));
    public static final Block CRYSTAL_PLANKS = reg("crystal_planks", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_LIGHT_BLUE).strength(2.0F, 3.0F).sound(SoundType.WOOD));
    public static final Block CRYSTAL_LEAVES = reg("crystal_leaves", p -> new TintedParticleLeavesBlock(0.0F, p),
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_LIGHT_BLUE).strength(0.2F).randomTicks()
                    .sound(SoundType.GRASS).noOcclusion()
                    .isSuffocating((s, l, p) -> false).isViewBlocking((s, l, p) -> false));

    // ---- Pantano Bioluminiscente
    public static final Block GLOW_MOSS_BLOCK = reg("glow_moss_block", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.EMERALD).strength(0.1F)
                    .sound(SoundType.MOSS).lightLevel(s -> 8));
    public static final Block BLUE_MUD = reg("blue_mud", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_BLUE).strength(0.5F).sound(SoundType.MUD));

    // ---- Desierto de Obsidiana
    public static final Block BLACK_SAND = reg("black_sand",
            p -> new ColoredFallingBlock(new ColorRGBA(0x1E1E22), p),
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_BLACK).strength(0.5F).sound(SoundType.SAND));
    public static final Block VOLCANIC_GLASS = reg("volcanic_glass", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PURPLE).strength(3.0F, 12.0F)
                    .requiresCorrectToolForDrops().sound(SoundType.STONE));

    // ---- Tundra de Ámbar
    public static final Block AMBER_BLOCK = reg("amber_block", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_ORANGE).strength(1.5F, 3.0F)
                    .requiresCorrectToolForDrops().sound(SoundType.GLASS).lightLevel(s -> 4));
    public static final Block AMBER_PERMAFROST = reg("amber_permafrost", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.SAND).strength(0.6F).sound(SoundType.GRAVEL));

    // ---- Jungla de Hongos Gigantes
    public static final Block RED_MYCELIUM = reg("red_mycelium", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_RED).strength(0.6F).sound(SoundType.GRASS));
    public static final Block SPORE_STEM = reg("spore_stem", RotatedPillarBlock::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.TERRACOTTA_WHITE).strength(1.5F).sound(SoundType.WOOD));

    // ---- Lote 2
    public static final Block CLOUD_BLOCK = reg("cloud_block", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.SNOW).strength(0.3F).sound(SoundType.WOOL));
    public static final Block CRIMSON_ROCK = reg("crimson_rock", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_RED).strength(1.5F, 6.0F)
                    .requiresCorrectToolForDrops().sound(SoundType.STONE));
    public static final Block SILVER_LOG = reg("silver_log", RotatedPillarBlock::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_LIGHT_GRAY).strength(2.0F).sound(SoundType.WOOD));
    public static final Block SILVER_LEAVES = reg("silver_leaves", p -> new TintedParticleLeavesBlock(0.0F, p), leaves(MapColor.COLOR_LIGHT_GRAY));
    public static final Block BAOBAB_LOG = reg("baobab_log", RotatedPillarBlock::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_BROWN).strength(2.0F).sound(SoundType.WOOD));
    public static final Block AUTUMN_LEAVES_ORANGE = reg("autumn_leaves_orange", p -> new TintedParticleLeavesBlock(0.0F, p), leaves(MapColor.COLOR_ORANGE));
    public static final Block AUTUMN_LEAVES_RED = reg("autumn_leaves_red", p -> new TintedParticleLeavesBlock(0.0F, p), leaves(MapColor.COLOR_RED));
    public static final Block PINK_SAND = reg("pink_sand",
            p -> new ColoredFallingBlock(new ColorRGBA(0xE8B4C0), p),
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_PINK).strength(0.5F).sound(SoundType.SAND));
    public static final Block PEARL_BLOCK = reg("pearl_block", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.QUARTZ).strength(1.5F, 3.0F)
                    .requiresCorrectToolForDrops().sound(SoundType.STONE).lightLevel(s -> 3));
    public static final Block GOLDEN_MUD = reg("golden_mud", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.GOLD).strength(0.5F).sound(SoundType.MUD));
    public static final Block SALT_BLOCK = reg("salt_block", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.SNOW).strength(0.8F)
                    .requiresCorrectToolForDrops().sound(SoundType.STONE));
    public static final Block GLACIAL_ICE = reg("glacial_ice", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.ICE).strength(0.8F).friction(0.98F)
                    .requiresCorrectToolForDrops().sound(SoundType.GLASS));
    public static final Block MAGMA_BASALT = reg("magma_basalt", Block::new,
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_BLACK).strength(2.0F, 6.0F)
                    .requiresCorrectToolForDrops().sound(SoundType.BASALT).lightLevel(s -> 3));

    private static BlockBehaviour.Properties leaves(MapColor color) {
        return BlockBehaviour.Properties.of().mapColor(color).strength(0.2F).randomTicks()
                .sound(SoundType.GRASS).noOcclusion()
                .isSuffocating((s, l, p) -> false).isViewBlocking((s, l, p) -> false);
    }

    private static Block reg(String name, Function<BlockBehaviour.Properties, Block> factory,
                             BlockBehaviour.Properties props) {
        ResourceLocation id = BiomasSalvajes.id(name);
        ResourceKey<Block> blockKey = ResourceKey.create(Registries.BLOCK, id);
        Block block = Registry.register(BuiltInRegistries.BLOCK, blockKey, factory.apply(props.setId(blockKey)));

        ResourceKey<Item> itemKey = ResourceKey.create(Registries.ITEM, id);
        Registry.register(BuiltInRegistries.ITEM, itemKey,
                new BlockItem(block, new Item.Properties().setId(itemKey).useBlockDescriptionPrefix()));
        ALL.put(name, block);
        return block;
    }

    /** Fuerza la carga de la clase (y por tanto el registro de los bloques). */
    public static void init() {
    }
}
