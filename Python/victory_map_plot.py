import sys
from PIL import Image

# Constants
TILE_WIDTH = 16
TILE_HEIGHT = 16
TILES_PER_ROW = 16  # screen width in tiles
PIXELS_PER_TILE = TILE_WIDTH * TILE_HEIGHT
BYTES_PER_TILE = PIXELS_PER_TILE // 2  # 4bpp -> 2 pixels per byte

def load_palette(palette_file):
    palette = []
    with open(palette_file, 'rb') as f:
        data = f.read()
        for i in range(0, len(data), 3):
            r = data[i]
            g = data[i + 1]
            b = data[i + 2]
            palette.append((r, g, b))
    return palette

def load_tiles(tiles_file):
    with open(tiles_file, 'rb') as f:
        return f.read()

def load_map(map_file):
    map_data = []
    with open(map_file, 'rb') as f:
        raw = f.read()
        for i in range(0, len(raw), 2):
            word = raw[i] | (raw[i+1] << 8)
            map_data.append(word)  # NO masking
    return map_data

def load_table(table_file):
    table_data = []
    with open(table_file, 'rb') as f:
        raw = f.read()
        for i in range(0, len(raw)):  # start from 1, skipping first byte
            table_data.append(raw[i])
    return table_data

def draw_chunks(tiles_data, map_data, palette, chunk_starts, chunks_per_image, base_output_file):
    entries_per_chunk = 16 * TILES_PER_ROW
    image_width = TILES_PER_ROW * TILE_WIDTH

    total_chunks = len(chunk_starts)
    if chunks_per_image is None:
        chunks_per_image = total_chunks

    image_height = TILE_HEIGHT * 16 * chunks_per_image

    img = Image.new('RGB', (image_width, image_height))
    pixels = img.load()

    image_counter = 1
    chunk_in_image = 0

    for offset_index, chunk_start_index in enumerate(chunk_starts):
        print(f"Processing chunk {offset_index + 1}: table value = {chunk_start_index}")

        chunk_start = chunk_start_index * 256
        chunk_data = map_data[chunk_start:chunk_start + entries_per_chunk]

        y_offset = (chunks_per_image - chunk_in_image - 1) * 16 * TILE_HEIGHT

        for index, tile_word in enumerate(chunk_data):
            tile_x = (index % TILES_PER_ROW) * TILE_WIDTH
            tile_y = (16 * TILE_HEIGHT - ((index // TILES_PER_ROW) + 1) * TILE_HEIGHT) + y_offset

            tile_index = tile_word & 0x03FF  # Need to mask of any stray bits as could cause an error
            palette_index = (tile_word >> 12) & 0xF  # upper 4 bits = palette select

            tile_offset = tile_index * BYTES_PER_TILE
            tile_data = tiles_data[tile_offset:tile_offset + BYTES_PER_TILE]

            for y in range(TILE_HEIGHT):
                for x in range(0, TILE_WIDTH, 2):
                    byte_index = (y * TILE_WIDTH + x) // 2
                    byte = tile_data[byte_index]

                    pixel1 = (byte & 0xF0) >> 4
                    pixel2 = (byte & 0x0F)

                    # Correct palette lookup
                    color1 = palette[(palette_index * 16) + pixel1]
                    color2 = palette[(palette_index * 16) + pixel2]

                    pixels[tile_x + x, tile_y + y] = color1
                    pixels[tile_x + x + 1, tile_y + y] = color2

        chunk_in_image += 1

        if chunk_in_image == chunks_per_image or offset_index == len(chunk_starts) - 1:
            output_name = base_output_file.replace(".png", f"_{image_counter}.png")
            img.save(output_name)
            image_counter += 1
            chunk_in_image = 0
            if offset_index != len(chunk_starts) - 1:
                remaining_chunks = total_chunks - offset_index - 1
                current_chunks = min(chunks_per_image, remaining_chunks)
                image_height = TILE_HEIGHT * 16 * current_chunks
                img = Image.new('RGB', (image_width, image_height))
                pixels = img.load()

def main():
    if len(sys.argv) < 6:
        print("Usage: python ikari_map_plot3.py tiles.bin map.bin palette.bin table.bin output.png [chunks_per_image]")
        return

    tiles_file = sys.argv[1]
    map_file = sys.argv[2]
    palette_file = sys.argv[3]
    table_file = sys.argv[4]
    output_file = sys.argv[5]
    chunks_per_image = int(sys.argv[6]) if len(sys.argv) >= 7 else None

    palette = load_palette(palette_file)
    tiles_data = load_tiles(tiles_file)
    map_data = load_map(map_file)
    table_data = load_table(table_file)

    draw_chunks(tiles_data, map_data, palette, table_data, chunks_per_image, output_file)

if __name__ == "__main__":
    main()
