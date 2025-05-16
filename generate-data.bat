REM Victory Road and other from same hardware share almost all the layout of image / plotting routines across many titles, this one kind of a follow up to Ikai Warriors

REM Make the graphics for BG
copy /b p17.4c+p18.2c+p19.4b+p20.2b bg-origin.bin
python .\python\reversebyte.py bg-origin.bin
python .\python\rotate90.py reverse_bg-origin.bin rotated_bg.original.bin 16 16
python .\python\reversebyte.py rotated_bg.original.bin
python .\python\swapnybbles.py reverse_rotated_bg.original.bin

REM Save map data
python .\python\savebit.py p2.8p all_maps.bin 17A0 8c00
python .\python\savebit.py p2.8p Map_offset_data.bin 1700 a0
REM because the map is stored left right we just split up this so we can make single strips for each side.
python .\python\splitchunks.py Map_offset_data.bin Map_right.bin Map_left.bin 1


REM Make the Palette Data from the rom Palette files, we use same weighted method as Mame does
python .\python\make_palette4.py c1.1k c2.2l c3.1l all_palettes

REM Now we make the PNG maps from the data generates
REM game uses a left and portion of the tile memory for effects to alternate between levels display. (personally a bit offputting!)

python .\python\victory_map_plot.py swapped_reverse_rotated_bg.original.bin all_maps.bin all_palettes_2.bin Map_offset_data.bin Big_final_level.png
python .\python\victory_map_plot.py swapped_reverse_rotated_bg.original.bin all_maps.bin all_palettes_2.bin Map_right.bin Big_final_right-side.png
python .\python\victory_map_plot.py swapped_reverse_rotated_bg.original.bin all_maps.bin all_palettes_2.bin Map_left.bin Big_final_level-side.png
