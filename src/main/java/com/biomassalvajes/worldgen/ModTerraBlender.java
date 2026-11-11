package com.biomassalvajes.worldgen;

import com.biomassalvajes.BiomasSalvajes;
import terrablender.api.Regions;
import terrablender.api.SurfaceRuleManager;
import terrablender.api.TerraBlenderApi;

/** Punto de entrada "terrablender" (ver fabric.mod.json). */
public class ModTerraBlender implements TerraBlenderApi {
    /** Peso de la región frente a los biomas vanilla. Súbelo para ver más biomas del mod. */
    private static final int REGION_WEIGHT = 6;

    @Override
    public void onTerraBlenderInitialized() {
        Regions.register(new BiomasRegion(BiomasSalvajes.id("overworld"), REGION_WEIGHT));
        SurfaceRuleManager.addSurfaceRules(SurfaceRuleManager.RuleCategory.OVERWORLD,
                BiomasSalvajes.MOD_ID, ModSurfaceRules.makeRules());
    }
}
