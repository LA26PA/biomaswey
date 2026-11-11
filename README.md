# Biomas Salvajes (Fabric 1.21.8 + TerraBlender)

15 biomas, 24 bloques y 15 estructuras (lotes 1 y 2).

| # | Bioma | Bloques propios | Estructura |
|---|---|---|---|
| 1 | Bosque de Cristal | tronco, tablones, hojas de cristal | Torre del Prisma |
| 2 | Pantano Bioluminiscente | musgo luminoso, lodo azul | Cabaña de la Bruja Lumínica |
| 3 | Desierto de Obsidiana | arena negra, vidrio volcánico | Pirámide Invertida |
| 4 | Tundra de Ámbar | bloque de ámbar, permafrost | Campamento Congelado |
| 5 | Jungla de Hongos Gigantes | micelio rojo, tallo esporado | Aldea Fúngica |
| 6 | Pradera Celeste | bloque de nube | Santuario Eólico |
| 7 | Cañón Carmesí | roca carmesí | Ruinas del Cañón |
| 8 | Taiga Plateada | tronco y hojas plateadas | Cabaña del Cazador |
| 9 | Sabana de Baobabs | tronco de baobab | Aldea Tribal |
| 10 | Bosque Otoñal | hojas otoñales naranjas y rojas | Molino Abandonado |
| 11 | Costa de Perlas | arena rosa, bloque de perla | Faro de Perla |
| 12 | Manglar Dorado | lodo dorado | Casa de Manglar |
| 13 | Salinas Espejo | bloque de sal | Templo de Sal |
| 14 | Glaciar Azul | hielo glacial | Cripta de Hielo |
| 15 | Caldera Volcánica | basalto magmático | Forja Enana |

## Compilar
1. JDK 21.
2. `./gradlew build` (el wrapper ya está incluido) → `build/libs/biomassalvajes-0.1.0.jar`.
   Sin instalar nada: sube la carpeta a GitHub y el workflow `.github/workflows/build.yml` deja el jar como artefacto.
3. Instálalo en el server **y en cada cliente**, junto con Fabric API y TerraBlender (Fabric, 1.21.8).

Si cambias algo de `tools/generate.py`: `pip install pillow && python3 tools/generate.py`.

## Probar en un mundo nuevo
```
/locate biome biomassalvajes:sky_meadow
/locate structure biomassalvajes:wind_shrine
/place structure biomassalvajes:dwarf_forge
```
Los biomas solo aparecen en chunks nuevos. Para ver más, sube `REGION_WEIGHT` en `ModTerraBlender.java`.

## Ajustes conocidos
- Las hojas son opacas (sin transparencia): la capa de render cambió en 1.21.5+ y se añade cuando se pueda verificar.
- Añadir un bioma: `BIOMES` + `BIOME_NAMES` en el script, clave en `ModBiomes`, clima en `BiomasRegion`, regla en `ModSurfaceRules`.
