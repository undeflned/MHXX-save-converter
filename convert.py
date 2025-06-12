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
    # constants
    save_types = ["3DS", "XX", "GU"]
    file_lengths = [0x00481D88, 0x00481DAC, 0x004EB8BC]
    slot_positions = [[0x00126471, 0x00244C31, 0x003633F1], 
                      [0x00126495, 0x00244C55, 0x00363415], 
                      [0x0018CC99, 0x002AC55D, 0x003CBE21]]
    chat_positions = [[0x002434FD, 0x00361CBD, 0x0048047D], 
                      [0x00243521, 0x00361CE1, 0x004804A1], 
                      [0x002A9D25, 0x003C95E9, 0x004E8EAD]]
    chat_lengths = [5940, 5940, 10296]
    slot_info_positions = [0x00000004, 0x00000028, 0x00000028]

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
        ref_file[slot_info_positions[ref_type]+4:slot_positions[ref_type][0]]
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
        new_save += source_file[slot_positions[src_type][0]:]
    
    return new_save

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} source_save reference_save destination")
        sys.exit()
    new_save = convertion(sys.argv[1], sys.argv[2])
    with open(sys.argv[3], "wb") as f:
        f.write(new_save)
    print(f"Converted savedata has been saved to {os.path.abspath(sys.argv[3])}")