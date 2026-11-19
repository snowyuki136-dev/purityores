package com.example.purityores;

import java.util.function.Supplier;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.feature.Feature;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModFeatures {
    public static final DeferredRegister<Feature<?>> FEATURES =
            DeferredRegister.create(Registries.FEATURE, PurityOres.MODID);

    public static final Supplier<PurityVeinFeature> PURITY_VEIN =
            FEATURES.register("purity_vein", () -> new PurityVeinFeature(PurityVeinConfig.CODEC));
}
