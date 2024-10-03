# Metatiled

*A program made with love for the community*

*Special thanks to all `pret` contributors*

## Description

A small Python application that converts an image in PNG format to a map compatible with [pokecrystal](https://github.com/pret/pokecrystal) or [polishedcrystal](https://github.com/Rangi42/polishedcrystal). The program divides the image into metatiles, identifies unique metatiles and tiles, and generates the necessary binary and assembly files for use in game development projects.

I see this as a complementary tool for [Polished Map](https://github.com/Rangi42/polished-map) and [Polished Map++](https://github.com/Rangi42/polished-map/tree/plusplus) made by legendary Rangi42.

<p align="center"><b>Original image (default palette):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/maps/pallet_town.png?raw=true" alt="Pallet Town Map" width="320" height="288">
</p>

<p align="center"><b>Generated tileset (blk):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/tilesets/pallet_town_blk.png?raw=true" alt="Pallet Town Tileset">
</p>

<p align="center"><b>Generated compressed tileset (ablk):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/tilesets/pallet_town_ablk.png?raw=true" alt="Pallet Town Compressed Tileset">
</p>

<br>

<p align="center"><b>Original image (monochrome palette):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/maps/fonto.png?raw=true" alt="Fonto Map" width="320" height="288">
</p>

<p align="center"><b>Generated tileset (blk):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/tilesets/fonto_blk.png?raw=true" alt="Fonto Tileset">
</p>

<p align="center"><b>Generated compressed tileset (ablk):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/tilesets/fonto_ablk.png?raw=true" alt="Fonto Compressed Tileset">
</p>

<br>

<p align="center"><b>Original image (custom palette):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/maps/new_bark_town.png?raw=true" alt="New Bark Town Map" width="320" height="288">
</p>

<p align="center"><b>Generated tileset (blk):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/tilesets/new_bark_town_blk.png?raw=true" alt="New Bark Town Tileset">
</p>

<p align="center"><b>Generated compressed tileset (ablk):</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/tilesets/new_bark_town_ablk.png?raw=true" alt="New Bark Town Compressed Tileset">
</p>

<br>

<p align="center"><b>Palette analysis:</b></p>
<p align="center">
<img src="https://raw.githubusercontent.com/j4n7/metatiled/refs/heads/master/examples/maps/wrong_palette_analysis.png?raw=true" alt="New Bark Town Map" width="320" height="288">
</p>
<p align="center">All tiles using the same palette are shown in a randomly assigned color.</p>
<p align="center">Tiles with more than 4 tones (colors) are displayed in their original form.</p>

## Why?

So far, there is no program that allows generating the necessary files to create a compatible map with the mentioned ROMs almost from scratch. 

Working directly on an image to generate a map with programs like Aseprite or Photoshop has its advantages. It's easier to design tiles on the go and see how they fit into the overall map. 

Additionally, this program allows compressing the tilesets for the .ablk format, so that only the strictly necessary tiles are used (to which different colors and X and Y flips can then be applied).

## Usage

```sh
python3 metatiled.py <map_image> [--palette <palette_name>] [--compress]
```
or
```sh
python3 metatiled.py <map_image> [-p <palette_name>] [-c]
```

<br>

To extract colors and tones from an image:
```sh
python3 metatiled.py <map_image> [--extract-palette]
```
or
```sh
python3 metatiled.py <map_image> [-e]
```

<br>

To check if palette is valid and, if not, output a guiding image:
```sh
python3 metatiled.py <map_image> [--analyze-palette]
```
or
```sh
python3 metatiled.py <map_image> [-a]
```

### Positional Arguments

- `<map_image>`: Name of the map image file in PNG format.

### Flags

- `--palette`, `-p`: Name of the palette to use that corresponds to the image. This argument is optional.
- `--compress`, `-c`: Apply additional compression to the tiles. This argument is optional.
- `--extract-palette`, `-e`: Generate a txt file with the palette of the map. This argument is optional.
- `--analyze-palette`, `-a`: Validates the palette and outputs a guiding image if it’s invalid. This argument is optional.

## Notes

- Ensure that the map image is in PNG format and is using a supported palette.
- It supports maps with a monocrhome palette (just 4 tones).
- It supports maps with a custom palette provided you include a txt file with the used colors. See the example folder to understand the format you need to use or use `--extract-palette`.
- The map image can have 1 custom color (made of 4 tones) not defined by the palette.
- The program should autodetect the palette. If you are having trouble use next argument.
- The `--palette` option is not required and must specify one of the available palettes. You have to make sure your image is using the that palette. All colors must be contained in that palette, except the 4 ones that are used for the roofs. 
- The `--compress` option is not required and, if used, will apply additional compression to the tiles.
- The `--extract-palette` option is not required and is meant to be used alone. It will generate a txt file with the palette of the map. That file will still require some manual adjustments.
- The `--analyze-palette` option is not required and is meant to be used alone. It will output an image if the palette is invalid, meaning it contains more than 7 colors or some tiles have more than 5 tones. The image helps identify problematic tiles, allowing you to manually correct the map.

## Examples

Use the provided `pallet_town.png` image. Then you can use [Polished Map](https://github.com/Rangi42/polished-map) or [Polished Map++](https://github.com/Rangi42/polished-map/tree/plusplus) to inspect the generated files.

### Example 1: Convert an image without compression (BLK)

To generate **blk** files compatible with pokecrystal:

```sh
python metatiled.py examples/maps/pallet_town.png
```
or
```sh
python metatiled.py examples/maps/pallet_town.png --palette day
```

This command converts the image `pallet_town.png` using the `day` palette and generates the necessary files without applying additional compression.

### Example 2: Convert an image with compression (ABLK)

To generate **ablk** files compatible with polishedcrystal:

```sh
python metatiled.py examples/maps/pallet_town.png --compress
```

This command converts the image `pallet_town.png` using the `day` palette and applies additional compression to the tiles.

## Generated Files

Depending on whether the `--compress` option is used, the program will generate different files:

### Without Compression (BLK)

- `Makefile`: Required by Polished Map.
- `maps/<MapName>.blk`: Binary file with the positions of the metatiles.
- `gfx/tilesets/<MapName>.png`: Grayscale image of the tileset.
- `gfx/tilesets/<MapName>_palette_map.asm`: Assembly file with the palette map.
- `data/tilesets/<MapName>_metatiles.bin`: Binary file with the metatiles.

### With Compression (ABLK)

- `Main.asm`: Required by Polished Map++.
- `maps/<MapName>.ablk`: Binary file with the positions of the metatiles.
- `gfx/tilesets/<MapName>.png`: Compressed image of the tileset.
- `data/tilesets/<MapName>_metatiles.bin`: Binary file with the compressed metatiles.
- `data/tilesets/<MapName>_attributes.bin`: Binary file with the metatile attributes.

## Available Default Palettes

The available default palettes are:

- `morn`
- `day`
- `nite`
- `dark`
- `indoor`

Each palette contains different color tones used to convert the map image.

## TODO

- Collision and priority masks
- Graphical interface
- Auto-import references directly into the ROM project
- Implement validation mechanisms

---
