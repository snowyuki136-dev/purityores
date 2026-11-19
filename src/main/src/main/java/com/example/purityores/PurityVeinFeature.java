package com.example.purityores;

import com.mojang.serialization.Codec;
import net.minecraft.core.BlockPos;
import net.minecraft.tags.BlockTags;
import net.minecraft.util.RandomSource;
import net.minecraft.world.level.WorldGenLevel;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.minecraft.world.level.levelgen.feature.FeaturePlaceContext;

public class PurityVeinFeature extends Feature<PurityVeinConfig> {
    public PurityVeinFeature(Codec<PurityVeinConfig> codec) {
        super(codec);
    }

    @Override
    public boolean place(FeaturePlaceContext<PurityVeinConfig> ctx) {
        WorldGenLevel level = ctx.level();
        RandomSource random = ctx.random();
        BlockPos origin = ctx.origin();
        OreType ore = ctx.config().ore();

        // Roll the purity of this vein: 50% poor, 35% normal, 15% rich
        float roll = random.nextFloat();
        Tier tier = roll < 0.50f ? Tier.POOR : roll < 0.85f ? Tier.NORMAL : Tier.RICH;
        int size = switch (tier) {
            case POOR -> (int) Math.ceil(ore.size * 1.4);
            case NORMAL -> ore.size;
            case RICH -> Math.max(1, ore.size / 2);
        };

        // Random-walk blob around the origin
        BlockPos.MutableBlockPos pos = origin.mutable();
        int placed = 0;
        for (int i = 0; i < size * 4 && placed < size; i++) {
            pos.move(random.nextInt(3) - 1, random.nextInt(3) - 1, random.nextInt(3) - 1);
            if (pos.distManhattan(origin) > 6) {
                pos.set(origin);
            }
            if (!level.ensureCanWrite(pos)) {
                continue;
            }

            BlockState existing = level.getBlockState(pos);
            boolean deepslate;
            if (ore.nether) {
                if (!existing.is(Blocks.NETHERRACK)) continue;
                deepslate = false;
            } else if (existing.is(BlockTags.STONE_ORE_REPLACEABLES)) {
                deepslate = false;
            } else if (existing.is(BlockTags.DEEPSLATE_ORE_REPLACEABLES)) {
                deepslate = true;
            } else {
                continue;
            }

            level.setBlock(pos, stateFor(ore, tier, deepslate), 2);
            placed++;
        }
        return placed > 0;
    }

    private static BlockState stateFor(OreType ore, Tier tier, boolean deepslate) {
        if (tier == Tier.NORMAL) {
            return (deepslate ? ore.deepslate : ore.stone).defaultBlockState();
        }
        return ModBlocks.ORES.get(ModBlocks.blockName(ore, tier, deepslate)).get().defaultBlockState();
    }
}
