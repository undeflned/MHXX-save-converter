import sys
import os


def get_file(file_path: str):
    file = open(file_path, 'rb')
    with file:
        new_file = file.read()
        file.close()
    return new_file


def fix_chat_ww2jp(new_save_data, save, slot_position, chat_position):
    chat_range = 100
    extra_chat_bytes = 44

    new_save_data += save[slot_position:chat_position]
    for i in range(1, chat_range):
        new_save_data += save[
            chat_position + (104 * (i - 1)): chat_position + (104 * i) - extra_chat_bytes
        ]

    return new_save_data


def fix_chat_jp2ww(new_save_data, save, slot_position, chat_position):
    chat_range = 100
    extra_chat_bytes = bytes(44)

    new_save_data += save[slot_position:chat_position]
    for i in range(1, chat_range):
        new_save_data += (
            save[chat_position + (60 * (i - 1)) : chat_position + (60 * i)]
            + extra_chat_bytes
        )

    return new_save_data


def convertion(source, reference):
    save_types = ["3DS", "XX", "GU"]
    file_lengths = [4726152, 4726188, 5159100]
    initial_positions = (1205361, 1205397, 1625241)
    slot_positions = [[1205361, 2378801, 3552241], 
                      [1205397, 2378837, 3552277], 
                      [1625241, 2803037, 3980833]]
    chat_positions = [[2372861, 3546301, 4719741], 
                      [2372897, 3546337, 4719777], 
                      [2792741, 3970537, 5148333]]
    chat_lengths = [5940, 5940, 10296]
    slot_info_positions = [4, 40, 40]

    source_file = get_file(source)
    try:
        src_type = file_lengths.index(len(source_file))
    except ValueError:
        print("Source file is invalid.")
        sys.exit()
    ref_file = get_file(reference)
    try:
        ref_type = file_lengths.index(len(ref_file))
    except ValueError:
        print("Reference file is invalid.")
        sys.exit()
    
    print(f"Converting {save_types[src_type]} savedata to {save_types[ref_type]} savedata...")

    # new header
    new_save = ref_file[:slot_info_positions[ref_type]] + source_file[slot_info_positions[src_type]:slot_info_positions[src_type]+4] + \
        ref_file[slot_info_positions[ref_type]+4:initial_positions[ref_type]]
    # chat convertion + save data concatenation
    if src_type in (0, 1) and ref_type == 2:
        for i, chat_position in enumerate(chat_positions[src_type]):
            new_save = fix_chat_jp2ww(new_save, source_file, slot_positions[src_type][i], chat_position)
        new_save += source_file[chat_positions[src_type][2] + chat_lengths[src_type]:]
    elif src_type == 2 and ref_type in (0, 1):
        for i, chat_position in enumerate(chat_positions[src_type]):
            new_save = fix_chat_ww2jp(new_save, source_file, slot_positions[src_type][i], chat_position)
        new_save += source_file[chat_positions[src_type][2] + chat_lengths[src_type]:]
    else:
        new_save += source_file[initial_positions[src_type]:]
    
    return new_save

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python convert.py <source_save> <reference_save> <destination>")
        sys.exit()
    new_save = convertion(sys.argv[1], sys.argv[2])
    with open(sys.argv[3], "wb") as f:
        f.write(new_save)
    print(f"Converted savedata has been saved to {os.path.abspath(sys.argv[3])}")