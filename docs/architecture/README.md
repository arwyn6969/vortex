# Vortex Architecture Diagrams

This directory contains Mermaid diagrams representing the architectural structure of the Vortex system, particularly focusing on the zone system and its relationship to the Kabbalah Tree of Life.

## Available Diagrams

### 1. Zones Structure (`zones_structure.mmd`)
This diagram shows the program's zone structure, organized according to the three pillars:
- **Left Pillar (Severity)**: Zen Zone (Binah), Gains Grotto (Gevurah), Glory Pond/Meme Studio (Hod)
- **Middle Pillar (Balance)**: Crown Pond (Keter), Vibe Temple (Tiferet), Harmony Pond (Yesod), Kingdom Pond (Malkhut)
- **Right Pillar (Mercy)**: Brain Galaxy/Wisdom Pond (Chokhmah), Mercy Pond (Chesed), Boundaries Pond (Netzach)

The diagram displays the exact path connections between these zones based on the traditional Kabbalah structure, with numbered paths and Hebrew letter associations. The pillars are positioned in their traditional order: Severity (left), Balance (middle), and Mercy (right).

### 2. Kabbalah Tree of Life (`kabbalah_tree.mmd`)
This diagram represents the Tree of Life structure with:
- All 10 Sefirot with their elements, colors, and assigned guides
- The 22 connecting paths with their Hebrew letters and path numbers
- Color-coded pillars and spheres
- Complete correspondences for each Sefira

The paths are organized according to the structure found in the traditional Kabbalah, with each path shown with its Hebrew letter.

### 3. Traditional Tree of Life (`traditional_kabbalah.mmd`)
This diagram represents the most accurate traditional Tree of Life layout with:
- Numbered Sefirot in their correct positions
- All 22 paths with Hebrew letters
- Colored Sefirot according to traditional attributions
- Clear pillar structure (Left/Severity, Middle/Balance, Right/Mercy)
- The "Lightning Flash" path of creation highlighted

This representation closely follows classical Kabbalistic traditions and provides the most accurate visual reference for understanding the relationships between Sefirot.

## Path Structure

The path structure is specifically based on the data in `vortex/src/mythology/sefirot.py`, which defines the correct connections between each Sefirah. This is important because:

1. **Energetic Flow**: Each path represents a specific energetic connection and transformation
2. **Hebrew Letters**: Each path corresponds to a specific Hebrew letter with metaphysical significance
3. **Progression**: The paths represent the correct order of spiritual development
4. **Game Mechanics**: The connections determine how players can navigate between zones

## Viewing the Diagrams

These diagrams are in Mermaid format. You can view them using:

1. VS Code with the Mermaid extension
2. Online Mermaid Live Editor: https://mermaid.live
3. GitHub (which natively supports Mermaid in markdown)

## Diagram Updates

When updating the zone system, please ensure to:
1. Maintain the correct correspondences between zones and Sefirot
2. Update guide assignments appropriately
3. Preserve the traditional path connections and their numbering
4. Keep the color coding consistent with the mythological symbolism
5. Reference the structure in `vortex/src/mythology/sefirot.py` for the correct path definitions

## References

- `vortex/src/zones/`: Implementation of the zone system
- `vortex/src/mythology/sefirot.py`: Definitive source for path connections between Sefirot
- `vortex/src/mythology/`: Mythological correspondences and archetype definitions
- `vortex/src/guides/`: Guide implementations for each zone 