package com.example.purityores;

import java.util.LinkedHashMap;
import java.util.Map;

import net.minecraft.util.valueproviders.UniformInt;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.DropExperienceBlock;
import net.minecraft.world.level.block.RedStoneOreBlock;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModBlocks {
    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(PurityOres.MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(PurityOres.MODID);

    /** Every poor/rich ore block, keyed by registry name. */
    public static final Map<String, DeferredBlock<Block>> ORES = new LinkedHashMap<>();

    public static String blockName(OreType type, Tier tier, boolean deepslate) {
        return tier.id + "_" + (deepslate ? "deepslate_" : "") + type.id + "_ore";
    }

    static {
        for (OreType type : OreType.values()) {
            for (Tier tier : new Tier[] { Tier.POOR, Tier.RICH }) {
                register(type, tier, false);
                if (!type.nether) {
                    register(type, tier, true);
                }
            }
        }
    }

    private static void register(OreType type, Tier tier, boolean deepslate) {
        String name = blockName(type, tier, deepslate);
        Block base = deepslate ? type.deepslate : type.stone;
        BlockBehaviour.Properties props = BlockBehaviour.Properties.ofFullCopy(base);
        DeferredBlock<Block> block = BLOCKS.<Block>registerBlock(name, p -> createBlock(type, p), props);
        ITEMS.registerSimpleBlockItem(block);
        ORES.put(name, block);
    }

    /** Matches the vanilla block class of each ore (redstone needs its "lit" property, others drop XP). */
    private static Block createBlock(OreType type, BlockBehaviour.Properties props) {
        return switch (type) {
            case REDSTONE -> new RedStoneOreBlock(props);
            case COAL -> new DropExperienceBlock(UniformInt.of(0, 2), props);
            case LAPIS, NETHER_QUARTZ -> new DropExperienceBlock(UniformInt.of(2, 5), props);
            case DIAMOND, EMERALD -> new DropExperienceBlock(UniformInt.of(3, 7), props);
            case NETHER_GOLD -> new DropExperienceBlock(UniformInt.of(0, 1), props);
            default -> new Block(props);
        };
    }
}
