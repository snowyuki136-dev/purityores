package com.example.purityores;

import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.world.level.levelgen.feature.configurations.FeatureConfiguration;

public record PurityVeinConfig(OreType ore) implements FeatureConfiguration {
    public static final Codec<PurityVeinConfig> CODEC = RecordCodecBuilder.create(instance -> instance.group(
            OreType.CODEC.fieldOf("ore").forGetter(PurityVeinConfig::ore)
    ).apply(instance, PurityVeinConfig::new));
}
