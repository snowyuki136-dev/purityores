package com.example.purityores;

import com.mojang.serialization.Codec;
import net.minecraft.util.StringRepresentable;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.Blocks;

public enum OreType implements StringRepresentable {
    //            id               stone ore                  deepslate ore                  base vein size
    COAL("coal",                   Blocks.COAL_ORE,           Blocks.DEEPSLATE_COAL_ORE,     14),
    COPPER("copper",               Blocks.COPPER_ORE,         Blocks.DEEPSLATE_COPPER_ORE,   10),
    IRON("iron",                   Blocks.IRON_ORE,           Blocks.DEEPSLATE_IRON_ORE,      9),
    GOLD("gold",                   Blocks.GOLD_ORE,           Blocks.DEEPSLATE_GOLD_ORE,      9),
    REDSTONE("redstone",           Blocks.REDSTONE_ORE,       Blocks.DEEPSLATE_REDSTONE_ORE,  8),
    LAPIS("lapis",                 Blocks.LAPIS_ORE,          Blocks.DEEPSLATE_LAPIS_ORE,     7),
    DIAMOND("diamond",             Blocks.DIAMOND_ORE,        Blocks.DEEPSLATE_DIAMOND_ORE,   4),
    EMERALD("emerald",             Blocks.EMERALD_ORE,        Blocks.DEEPSLATE_EMERALD_ORE,   2),
    NETHER_GOLD("nether_gold",     Blocks.NETHER_GOLD_ORE,    null,                          10),
    NETHER_QUARTZ("nether_quartz", Blocks.NETHER_QUARTZ_ORE,  null,                          14);

    public static final Codec<OreType> CODEC = StringRepresentable.fromEnum(OreType::values);

    public final String id;
    public final Block stone;
    public final Block deepslate; // null for nether ores
    public final int size;
    public final boolean nether;

    OreType(String id, Block stone, Block deepslate, int size) {
        this.id = id;
        this.stone = stone;
        this.deepslate = deepslate;
        this.size = size;
        this.nether = deepslate == null;
    }

    @Override
    public String getSerializedName() {
        return id;
    }
}
