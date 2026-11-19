package com.example.purityores;

import net.minecraft.world.item.CreativeModeTabs;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;

@Mod(PurityOres.MODID)
public class PurityOres {
    public static final String MODID = "purityores";

    public PurityOres(IEventBus modBus) {
        ModBlocks.BLOCKS.register(modBus);
        ModBlocks.ITEMS.register(modBus);
        ModFeatures.FEATURES.register(modBus);
        modBus.addListener(this::addToCreativeTab);
    }

    private void addToCreativeTab(BuildCreativeModeTabContentsEvent event) {
        if (event.getTabKey() == CreativeModeTabs.NATURAL_BLOCKS) {
            ModBlocks.ORES.values().forEach(block -> event.accept(block.get()));
        }
    }
}
