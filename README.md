# Victory Road Map Plotter (`victory_map_plot.py`)

This repository provides tooling for visualising background tilemaps from the arcade game **Victory Road** by SNK (1986), the sequel to *Ikari Warriors*. The script decodes and renders the map layouts directly from raw ROM-extracted data and outputs PNG images for analysis or documentation.

This project aims to support game preservation, visual reverse engineering, and educational exploration of classic arcade hardware. No ROM data is distributed; users must provide their own legally sourced binary files.

---

## 📁 Data Format Overview

Victory Road uses tile and palette systems similar to Ikari Warriors, but with unique layout differences and expanded map structures.

### 1. Character Graphics (`gfx.bin`)

* Each tile: 8×8 pixels, 4 bits per pixel (4bpp)
* Each tile is 32 bytes (8 rows × 4 bytes)
* Graphics data is linear, tile index is direct

### 2. Tile Blocks (2x2 or Meta-Tiles)

* Maps consist of 16x16-pixel blocks made of 2x2 character tiles
* Each tile block entry is 3 bytes:

  * 2 bytes: Tile number
  * 1 byte: Palette + flip bits (high bits control X/Y flip)

### 3. Master Map (`map.bin`)

* The map consists of columns of tile blocks
* Each column is a vertical strip of 8 or more tile blocks (128+ pixels high)
* Map entries are 2 bytes (word), referencing a tile block offset
* Flip bits may be present in the high byte (bit 7 = Y flip, bit 6 = X flip)

---

## 🛠️ Script Functionality

`victory_map_plot.py` performs the following:

* Decodes character graphics and tile blocks
* Loads palette data in MAME-accurate RGB format
* Applies palette and flip bits
* Assembles map columns and composes full image
* Outputs final map as PNG

---

## ⚡ Usage

```bash
python victory_map_plot.py gfx.bin palette.bin tile2x2.bin map.bin output.png
```

### Optional Flags

* `--quantity <n>`: Only render the first `n` map columns
* `--offset`: Can specify a pointer inside the map data to start from

---

## 📃 Legal Notice

This project does **not** include any ROM data or copyrighted game content.
All tools here are for **documentation and analysis** of original arcade game formats. You must supply your own extracted binary files from your legally owned ROM sets.

---

## 📄 License

This project is released under the MIT License. See `LICENSE` for details.
