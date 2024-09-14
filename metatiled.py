import os
import argparse
from PIL import Image


palettes = {
    "morn": {
        "GRAY": [(28, 31, 16), (21, 21, 21), (13, 13, 13), (7, 7, 7)],
        "RED": [(28, 31, 16), (31, 19, 24), (30, 10, 6), (7, 7, 7)],
        "GREEN": [(22, 31, 10), (12, 25, 1), (5, 14, 0), (7, 7, 7)],
        "WATER": [(23, 23, 31), (18, 19, 31), (13, 12, 31), (7, 7, 7)],
        "YELLOW": [(28, 31, 16), (31, 31, 7), (31, 16, 1), (7, 7, 7)],
        "BROWN": [(28, 31, 16), (24, 18, 7), (20, 15, 3), (7, 7, 7)],
        "ROOF": [(28, 31, 16), (15, 31, 31), (5, 17, 31), (7, 7, 7)],
        "TEXT": [(31, 31, 16), (31, 31, 16), (14, 9, 0), (0, 0, 0)]
    },
    "day": {
        "GRAY": [(27, 31, 27), (21, 21, 21), (13, 13, 13), (7, 7, 7)],
        "RED": [(27, 31, 27), (31, 19, 24), (30, 10, 6), (7, 7, 7)],
        "GREEN": [(22, 31, 10), (12, 25, 1), (5, 14, 0), (7, 7, 7)],
        "WATER": [(23, 23, 31), (18, 19, 31), (13, 12, 31), (7, 7, 7)],
        "YELLOW": [(27, 31, 27), (31, 31, 7), (31, 16, 1), (7, 7, 7)],
        "BROWN": [(27, 31, 27), (24, 18, 7), (20, 15, 3), (7, 7, 7)],
        "ROOF": [(27, 31, 27), (15, 31, 31), (5, 17, 31), (7, 7, 7)],
        "TEXT": [(31, 31, 16), (31, 31, 16), (14, 9, 0), (0, 0, 0)]
    },
    "nite": {
        "GRAY": [(15, 14, 24), (11, 11, 19), (7, 7, 12), (0, 0, 0)],
        "RED": [(15, 14, 24), (14, 7, 17), (13, 0, 8), (0, 0, 0)],
        "GREEN": [(15, 14, 24), (8, 13, 19), (0, 11, 13), (0, 0, 0)],
        "WATER": [(15, 13, 27), (10, 9, 20), (4, 3, 18), (0, 0, 0)],
        "YELLOW": [(30, 30, 11), (16, 14, 18), (16, 14, 10), (0, 0, 0)],
        "BROWN": [(15, 14, 24), (12, 9, 15), (8, 4, 5), (0, 0, 0)],
        "ROOF": [(15, 14, 24), (13, 12, 23), (11, 9, 20), (0, 0, 0)],
        "TEXT": [(31, 31, 16), (31, 31, 16), (14, 9, 0), (0, 0, 0)]
    },
    "dark": {
        "GRAY": [(1, 1, 2), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        "RED": [(1, 1, 2), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        "GREEN": [(1, 1, 2), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        "WATER": [(1, 1, 2), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        "YELLOW": [(30, 30, 11), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        "BROWN": [(1, 1, 2), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        "ROOF": [(1, 1, 2), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
        "TEXT": [(31, 31, 16), (31, 31, 16), (14, 9, 0), (0, 0, 0)]
    },
    "indoor": {
        "GRAY": [(30, 28, 26), (19, 19, 19), (13, 13, 13), (7, 7, 7)],
        "RED": [(30, 28, 26), (31, 19, 24), (30, 10, 6), (7, 7, 7)],
        "GREEN": [(18, 24, 9), (15, 20, 1), (9, 13, 0), (7, 7, 7)],
        "WATER": [(30, 28, 26), (15, 16, 31), (9, 9, 31), (7, 7, 7)],
        "YELLOW": [(30, 28, 26), (31, 31, 7), (31, 16, 1), (7, 7, 7)],
        "BROWN": [(26, 24, 17), (21, 17, 7), (16, 13, 3), (7, 7, 7)],
        "ROOF": [(30, 28, 26), (17, 19, 31), (14, 16, 31), (7, 7, 7)],
        "TEXT": [(31, 31, 16), (31, 31, 16), (14, 9, 0), (0, 0, 0)]
    }
}


def is_same_tone(tile_tone, palette_tone, tolerance=1):
    match = all([abs(tile_tone[i] - palette_tone[i])
                <= tolerance for i in range(3)])
    return match


def is_same_color(tile_tones, palette_tones):
    match = all([any(is_same_tone(tile_tone, palette_tone)
                for palette_tone in palette_tones) for tile_tone in tile_tones])
    return match


def handle_palette(palette_name):
    palette_8bit = {k: [convert_to_8bit_rgb(
        c) for c in v] for k, v in palettes[palette_name].items()}
    return palette_8bit


def convert_to_5bit_rgb(color):
    return tuple((c * 31) // 255 for c in color)


def convert_to_8bit_rgb(color):
    return tuple((c * 255) // 31 for c in color)


def divide_into_metatiles(image):
    width, height = image.size
    metatiles = []
    for y in range(0, height, 32):
        for x in range(0, width, 32):
            metatile = image.crop((x, y, x + 32, y + 32))
            metatiles.append(metatile)
    return metatiles


def identify_unique_metatiles(metatiles):
    unique_metatiles = []
    metatile_positions = []
    for i, metatile in enumerate(metatiles):
        if metatile not in unique_metatiles:
            unique_metatiles.append(metatile)
        metatile_positions.append(unique_metatiles.index(metatile))
    return unique_metatiles, metatile_positions


def divide_metatiles_into_tiles(unique_metatiles, palette):
    unique_tiles = []
    tile_colors = []
    tile_grays = []

    for metatile in unique_metatiles:
        for y in range(0, 32, 8):
            for x in range(0, 32, 8):
                tile = metatile.crop((x, y, x + 8, y + 8))
                if tile not in unique_tiles:
                    unique_tiles.append(tile)

    get_roof_colors(unique_tiles, palette)

    for tile in unique_tiles:
        tile_tones = set(tile.getpixel((i % 8, i // 8)) for i in range(64))
        tile_tones = sorted(tile_tones, key=lambda c: (
            0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]), reverse=True)
        color, positions = get_tile_palette_color(tile_tones, palette)
        tile_colors.append(color)
        tile_grays.append(positions)

        print(color, positions)

    return unique_tiles, tile_colors, tile_grays


def get_roof_colors(unique_tiles, palette):
    def unique_sublists(lst):
        unique_list = []
        for sublist in lst:
            sublist_set = set(sublist)
            if not any(sublist_set.issubset(set(existing_sublist)) for existing_sublist in unique_list):
                unique_list.append(sublist)
        return unique_list

    def is_roof(tile_tones, palette):
        for color_name, palette_tones in palette.items():
            if all(any(is_same_tone(tile_tone, palette_tone) for palette_tone in palette_tones) for tile_tone in tile_tones):
                return False
        return True

    roof_tones = []
    for tile in unique_tiles:
        tile_tones = set(tile.getpixel((i % 8, i // 8)) for i in range(64))
        # Sort using luminance formula
        tile_tones = sorted(tile_tones, key=lambda c: (
            0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]), reverse=True)
        if is_roof(tile_tones, palette):
            roof_tones.append(tile_tones)

    palette['ROOF'] = unique_sublists(roof_tones)[0] if unique_sublists(roof_tones) else palette['ROOF']


def get_tile_palette_color(tile_tones, palette):
    matching_positions = {}

    for color_name, palette_tones in palette.items():
        positions = {}
        match = True
        for i, tile_tone in enumerate(tile_tones):
            found = False
            for j, palette_tone in enumerate(palette_tones):
                if is_same_tone(tile_tone, palette_tone):
                    positions[tile_tone] = j
                    found = True
                    break
            if not found:
                match = False
                break
        if match:
            matching_positions[color_name] = positions

    color_name = next(iter(matching_positions))
    return color_name, matching_positions[color_name]


def save_tileset_image(tiles, tile_grays, output_path, grayscale=True):
    tileset_image = Image.new('RGB', (128, 96), (255, 255, 255))

    if grayscale:
        grayscale = {
            0: (255, 255, 255),
            1: (170, 170, 170),
            2: (85, 85, 85),
            3: (0, 0, 0)
        }

        for i, tile in enumerate(tiles):
            grays = {gray: grayscale[position]
                     for gray, position in tile_grays[i].items()}
            new_tile = Image.new('RGB', (8, 8))
            for y in range(8):
                for x in range(8):
                    pixel = tile.getpixel((x, y))
                    new_tile.putpixel(
                        (x, y), grays.get(pixel, (255, 255, 255)))

            x = (i % 16) * 8
            y = (i // 16) * 8
            tileset_image.paste(new_tile, (x, y))

    else:
        for i, tile in enumerate(tiles):
            x = (i % 16) * 8
            y = (i // 16) * 8
            tileset_image.paste(tile, (x, y))

    tileset_image.save(output_path)


def save_metatiles_binary(metatiles, tiles, output_path):
    with open(output_path, 'wb') as f:
        for metatile in metatiles:
            for y in range(0, 32, 8):
                for x in range(0, 32, 8):
                    tile = metatile.crop((x, y, x + 8, y + 8))
                    tile_index = tiles.index(tile)
                    f.write(tile_index.to_bytes(1, 'big'))


def save_blk_file(output_path, metatile_positions):
    with open(output_path, 'wb') as f:
        for position in metatile_positions:
            f.write(position.to_bytes(1, 'big'))


def ensure_directories(base_dir):
    directories = [
        "data/tilesets",
        "gfx/tilesets",
        "maps"
    ]
    for directory in directories:
        path = os.path.join(base_dir, directory)
        if not os.path.exists(path):
            os.makedirs(path)


def ensure_makefile(base_dir):
    makefile_path = os.path.join(base_dir, "Makefile")
    if not os.path.exists(makefile_path):
        with open(makefile_path, 'w') as f:
            f.write("# Generated by Metatiled\n")
            f.write(
                "# Polished Map assumes a directory with a Makefile is the main project directory.\n")
            f.write("\n")


def generate_asm_file(colors, output_path):
    lines = []

    # Section 1
    for i in range(12):
        line_colors = colors[i * 8:(i + 1) * 8]
        if len(line_colors) < 8:
            line_colors.extend(['TEXT'] * (8 - len(line_colors)))
        line = "\ttilepal 0, " + ", ".join(line_colors)
        lines.append(line)

    # Section 2
    lines.append("")
    lines.append("rept 16")
    lines.append("    db $ff")
    lines.append("endr")
    lines.append("")

    # Section 3
    for i in range(12):
        line_colors = colors[(12 + i) * 8:(13 + i) * 8]
        if len(line_colors) < 8:
            line_colors.extend(['TEXT'] * (8 - len(line_colors)))
        line = "\ttilepal 1, " + ", ".join(line_colors)
        lines.append(line)

    # Línea vacía al final
    lines.append("")

    # Escribir las líneas al archivo
    with open(output_path, 'w') as f:
        for line in lines:
            f.write(line + '\n')


def main():
    parser = argparse.ArgumentParser(
        description='Process a Pokemon map for GameBoy Color.')
    parser.add_argument('map_image', type=str,
                        help='Name of the map image file (PNG).')
    parser.add_argument('--palette', '-p', type=str,
                        help='Name of the palette to use.', required=True)

    args = parser.parse_args()

    map_image = args.map_image
    palette_name = args.palette

    base_dir = os.path.dirname(map_image)
    base_name = os.path.splitext(os.path.basename(map_image))[0]

    ensure_directories(base_dir)
    ensure_makefile(base_dir)

    # Process map
    map_image = Image.open(map_image)
    palette = handle_palette(palette_name)
    metatiles = divide_into_metatiles(map_image)
    unique_metatiles, metatile_positions = identify_unique_metatiles(metatiles)
    tiles, tile_colors, tile_grays = divide_metatiles_into_tiles(
        unique_metatiles, palette)

    # Save files
    tileset_image_path = os.path.join(
        base_dir, 'gfx', 'tilesets', f'{base_name}.png')
    save_tileset_image(tiles, tile_grays, tileset_image_path, grayscale=True)

    metatiles_binary_path = os.path.join(
        base_dir, 'data', 'tilesets', f'{base_name}_metatiles.bin')
    save_metatiles_binary(unique_metatiles, tiles, metatiles_binary_path)

    blk_file_name = ''.join([word.capitalize()
                            for word in base_name.split('_')]) + '.blk'
    blk_file_path = os.path.join(base_dir, 'maps', blk_file_name)
    save_blk_file(blk_file_path, metatile_positions)

    asm_file_path = os.path.join(
        base_dir, 'gfx', 'tilesets', f'{base_name}_palette_map.asm')
    generate_asm_file(tile_colors, asm_file_path)


if __name__ == "__main__":
    main()
