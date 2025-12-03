#GT3GTRWUnpacker
import os
import struct
import time

print("GT3GTRWUnpacker - Made by Misuka")

#header struct
header_size_bytes = 0x60 #0x60 header length
magic = 0x0 #GTRW
unused = 0x4
unused2 = 0x8
end_of_file_pointer = 0xC
unk_count_uint32 = 0x10
unk_angle_maybe_uint32 = 0x14 #affects AI pathing, also affects start pos of ai in quali mode
unk_float = 0x18
unk_value_uint32_4 = 0x1C
light_flag_uint16 = 0x20 #at least 2nd byte affects lightning on night tracks
unk_flag_or_count_uint16_2 = 0x22
sector_data_pointer = 0x24
car_start_pos_count_uint32 = 0x28
car_start_pos_data_pointer = 0x2C
ground_coll_node_count_maybe_uint32 = 0x30
ground_coll_data_pointer = 0x34 #Might also contain data for gear suggestions, as they mess up as well. also messes AI
wall_coll_node_count_maybe_uint32 = 0x38
wall_coll_data_pointer = 0x3C
unk_count_uint32_2 = 0x40
pitbox_finishline_data_pointer = 0x44 #breaks AI as well
ground_coll_data_pointer_2 = 0x48 #doesn't break AI, seems to break pitboxes howeber.
wall_coll_data_pointer_2 = 0x4C
unk_count_uint32_3 = 0x50 #not always used
gadget_data_pointer = 0x54
unk_night_course_start_grid_light_vfx_value_uint32 = 0x58 #affects lightning seemingly at the start grid? night course only seemingly, not a pointer, doesn't upd in game mem
light_vfx_pointer = 0x5C #at least makes car all black on night courses

pointer_list = (sector_data_pointer, car_start_pos_data_pointer, ground_coll_data_pointer, wall_coll_data_pointer, pitbox_finishline_data_pointer, ground_coll_data_pointer_2,
                wall_coll_data_pointer_2, gadget_data_pointer, light_vfx_pointer)

pointer_list_outputted_files = ("11sectordata.bin", "13startgridposdata.bin", "15groundcolldata.bin", "17wallcolldata.bin", "19pitbox_finishlinedata.bin",
                                "20groundcolldata2.bin", "21wallcolldata2.bin", "23gadgetdata.bin", "25lightdata.bin")

pointer_offsets_in_file = (0x24, 0x2C, 0x34, 0x3C, 0x44, 0x48, 0x4C, 0x54, 0x5C)

#program functions

def read_all_pointers_from_runway(runway, pointers):
    results = []
    try:
        with open(runway, 'rb') as f:
            for offset in pointers:
                f.seek(offset, 0)
                value = struct.unpack("<I", f.read(4))[0]
                results.append(value)
        return results
    except:
        print("Unexpected problem occured during file processing.")

def read_and_dump_data_from_runway(runway, pointervalues):
    try:

        with open(runway, 'rb') as f:

            #first instance; make folders
            output_folder = runway+"_out"
            os.makedirs(output_folder, exist_ok=True)

            #read and dump magic
            f.seek(magic, 0)
            magic_data = f.read(4)

            magic_path = os.path.join(output_folder, "01magic.bin")
            with open(magic_path, 'wb') as out_file:
                print("Dumping 01magic.bin to", magic_path)
                out_file.write(magic_data)

            #read and dump unused1
            f.seek(unused, 0)
            unused1_data = f.read(4)

            unused1_path = os.path.join(output_folder, "02unused1.bin")
            with open(unused1_path, 'wb') as out_file:
                print("Dumping 02unused1.bin to", unused1_path)
                out_file.write(unused1_data)

            #read and dump unused2
            f.seek(unused2, 0)
            unused2_data = f.read(4)

            unused2_path = os.path.join(output_folder, "03unused2.bin")
            with open(unused2_path, 'wb') as out_file:
                print("Dumping 03unused2.bin to", unused2_path)
                out_file.write(unused2_data)

            #read and dump eof
            f.seek(end_of_file_pointer, 0)
            eof_data = f.read(4)

            eof_path = os.path.join(output_folder, "04eof.bin")
            with open(eof_path, 'wb') as out_file:
                print("Dumping 04eof.bin to", eof_path)
                out_file.write(eof_data)
    
            #read and dump unk_count_uint32
            f.seek(unk_count_uint32, 0)
            unk_count_data = f.read(4)

            unk_count_path = os.path.join(output_folder, "05unk_count.bin")
            with open(unk_count_path, 'wb') as out_file:
                print("Dumping 05unk_count.bin to", unk_count_path)
                out_file.write(unk_count_data)

            #read and dump unk_angle_maybe_uint32
            f.seek(unk_angle_maybe_uint32, 0)
            unk_angle_data = f.read(4)

            unk_angle_path = os.path.join(output_folder, "06unk_angle_maybe.bin")
            with open(unk_angle_path, 'wb') as out_file:
                print("Dumping 06unk_angle_maybe.bin to", unk_angle_path)
                out_file.write(unk_angle_data)

            #read and dump unk_float
            f.seek(unk_float, 0)
            unk_float_data = f.read(4)

            unk_float_path = os.path.join(output_folder, "07unk_float.bin")
            with open(unk_float_path, 'wb') as out_file:
                print("Dumping 07unk_float.bin to", unk_float_path)
                out_file.write(unk_float_data)

            #read and dump unk_value_uint32_4
            f.seek(unk_value_uint32_4, 0)
            unk_value2_data = f.read(4)

            unk_value2_path = os.path.join(output_folder, "08unk_value2.bin")
            with open(unk_value2_path, 'wb') as out_file:
                print("Dumping 08unk_value2.bin to", unk_value2_path)
                out_file.write(unk_value2_data)

            #read and dump light_flag_uint16
            f.seek(light_flag_uint16, 0)
            light_flag_data = f.read(2)

            light_flag_path = os.path.join(output_folder, "09light_flag.bin")
            with open(light_flag_path, 'wb') as out_file:
                print("Dumping 09light_flag.bin to", light_flag_path)
                out_file.write(light_flag_data)

            #read and dump unk_flag_or_count_uint16_2
            f.seek(unk_flag_or_count_uint16_2, 0)
            unk_flag_count_data = f.read(2)

            unk_flag_count_path = os.path.join(output_folder, "10unk_flag_or_count.bin")
            with open(unk_flag_count_path, 'wb') as out_file:
                print("Dumping 10unk_flag_or_count.bin to", unk_flag_count_path)
                out_file.write(unk_flag_count_data)

            #read and dump sector_data_pointer
            f.seek(pointervalues[0], 0)
            read_size = pointervalues[1] - pointervalues[0]
            sector_pointer_data = f.read(read_size)

            sector_data_path = os.path.join(output_folder, "11sectordata.bin")
            with open(sector_data_path, 'wb') as out_file:
                print("Dumping 11sectordata.bin to", sector_data_path)
                out_file.write(sector_pointer_data)

            #read and dump car_start_pos_count
            f.seek(car_start_pos_count_uint32, 0)
            car_start_pos_count_data = f.read(4)

            car_start_pos_count_path = os.path.join(output_folder, "12startgridcount.bin")
            with open(car_start_pos_count_path, 'wb') as out_file:
                print("Dumping 12startgridcount.bin to", car_start_pos_count_path)
                out_file.write(car_start_pos_count_data)

            #read and dump car_start_pos_data_pointer
            f.seek(pointervalues[1], 0)
            read_size = pointervalues[2] - pointervalues[1]
            car_start_pos_pointer_data = f.read(read_size)

            car_start_pos_data_path = os.path.join(output_folder, "13startgridposdata.bin")
            with open(car_start_pos_data_path, 'wb') as out_file:
                print("Dumping 13startgridposdata.bin to", car_start_pos_data_path)
                out_file.write(car_start_pos_pointer_data)

            #read and dump ground_coll_node_count_maybe_uint32
            f.seek(ground_coll_node_count_maybe_uint32, 0)
            ground_coll_node_count_data = f.read(4)

            ground_coll_node_count_path = os.path.join(output_folder, "14groundcollnodecount.bin")
            with open(ground_coll_node_count_path, 'wb') as out_file:
                print("Dumping 14groundcollnodecount.bin to", ground_coll_node_count_path)
                out_file.write(ground_coll_node_count_data)

            #read and dump ground_coll_data_pointer
            f.seek(pointervalues[2], 0)
            read_size = pointervalues[3] - pointervalues[2]
            ground_coll_pointer_data = f.read(read_size)

            ground_coll_path = os.path.join(output_folder, "15groundcolldata.bin")
            with open(ground_coll_path, 'wb') as out_file:
                print("Dumping 15groundcolldata.bin to", ground_coll_path)
                out_file.write(ground_coll_pointer_data)

            #read and dump wall_coll_node_count_maybe_uint32
            f.seek(wall_coll_node_count_maybe_uint32, 0)
            wall_coll_node_count_data = f.read(4)

            wall_coll_node_count_path = os.path.join(output_folder, "16wallcollnodecount.bin")
            with open(wall_coll_node_count_path, 'wb') as out_file:
                print("Dumping 16wallcollnodecount.bin to", wall_coll_node_count_path)
                out_file.write(wall_coll_node_count_data)

            #read and dump wall_coll_data_pointer
            f.seek(pointervalues[3], 0)
            read_size = pointervalues[4] - pointervalues[3]
            wall_coll_pointer_data = f.read(read_size)

            wall_coll_path = os.path.join(output_folder, "17wallcolldata.bin")
            with open(wall_coll_path, 'wb') as out_file:
                print("Dumping 17wallcolldata.bin to", wall_coll_path)
                out_file.write(wall_coll_pointer_data)

            #read and dump unk_count_uint32_2
            f.seek(unk_count_uint32_2, 0)
            unk_count2_data = f.read(4)

            unk_count2_path = os.path.join(output_folder, "18unkcount2.bin")
            with open(unk_count2_path, 'wb') as out_file:
                print("Dumping 18unkcount2.bin to", unk_count2_path)
                out_file.write(unk_count2_data)

            #read and dump pitbox_finishline_data_pointer
            f.seek(pointervalues[4], 0)
            read_size = pointervalues[5] - pointervalues[4]
            pitbox_finishline_pointer_data = f.read(read_size)

            pitbox_finishline_path = os.path.join(output_folder, "19pitbox_finishlinedata.bin")
            with open(pitbox_finishline_path, 'wb') as out_file:
                print("Dumping 19pitbox_finishlinedata.bin to", pitbox_finishline_path)
                out_file.write(pitbox_finishline_pointer_data)

            #read and dump ground_coll_data_pointer_2
            f.seek(pointervalues[5], 0)
            read_size = pointervalues[6] - pointervalues[5]
            ground_coll_pointer2_data = f.read(read_size)

            ground_coll2_path = os.path.join(output_folder, "20groundcolldata2.bin")
            with open(ground_coll2_path, 'wb') as out_file:
                print("Dumping 20groundcolldata2.bin to", ground_coll2_path)
                out_file.write(ground_coll_pointer2_data)

            #read and dump wall_coll_data_pointer_2
            f.seek(pointervalues[6], 0)
            read_size = pointervalues[7] - pointervalues[6]
            wall_coll_pointer2_data = f.read(read_size)

            wall_coll2_path = os.path.join(output_folder, "21wallcolldata2.bin")
            with open(wall_coll2_path, 'wb') as out_file:
                print("Dumping 21wallcolldata2.bin to", wall_coll2_path)
                out_file.write(wall_coll_pointer2_data)

            #read and dump unk_count_uint32_3
            f.seek(unk_count_uint32_3, 0)
            unk_count3_data = f.read(4)

            unk_count3_path = os.path.join(output_folder, "22unkcount3.bin")
            with open(unk_count3_path, 'wb') as out_file:
                print("Dumping 22unkcount3.bin to", unk_count3_path)
                out_file.write(unk_count3_data)

            #read and dump gadget_data_pointer
            f.seek(pointervalues[7], 0)
            read_size = pointervalues[8] - pointervalues[7]
            gadget_pointer_data = f.read(read_size)

            gadget_path = os.path.join(output_folder, "23gadgetdata.bin")
            with open(gadget_path, 'wb') as out_file:
                print("Dumping 23gadgetdata.bin to", gadget_path)
                out_file.write(gadget_pointer_data)

            #read and dump unk_night_course_start_grid_light_vfx_value_uint32
            f.seek(unk_night_course_start_grid_light_vfx_value_uint32, 0)
            unk_night_light_data = f.read(4)

            unk_night_light_path = os.path.join(output_folder, "24unknightlight.bin")
            with open(unk_night_light_path, 'wb') as out_file:
                print("Dumping 24unknightlight.bin to", unk_night_light_path)
                out_file.write(unk_night_light_data)

            #read and dump light_vfx_pointer
            f.seek(pointervalues[8], 0)
            f.seek(0, 2)
            eof = f.tell()

            read_size = eof - pointervalues[8]

            f.seek(pointervalues[8], 0)
            light_pointer_data = f.read(read_size)
        
            light_path = os.path.join(output_folder, "25lightdata.bin")
            with open(light_path, 'wb') as out_file:
                print("Dumping 25lightdata.bin to", light_path)
                out_file.write(light_pointer_data)

            print("GTRW extraction completed.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An unexpected error occured during file extracting:", e)


def create_runway_from_data(runway):
    try:
        # Get all files in output folder
        #files = sorted(os.listdir(runway+"_out"))
        output_folder = runway+"_out"

        # Header: read static fields from extracted files
        header = bytearray(header_size_bytes)
        header_field_files = [
            ("01magic.bin", 0x0, 4),
            ("02unused1.bin", 0x4, 4),
            ("03unused2.bin", 0x8, 4),
            ("04eof.bin", 0xC, 4),
            ("05unk_count.bin", 0x10, 4),
            ("06unk_angle_maybe.bin", 0x14, 4),
            ("07unk_float.bin", 0x18, 4),
            ("08unk_value2.bin", 0x1C, 4),
            ("09light_flag.bin", 0x20, 2),
            ("10unk_flag_or_count.bin", 0x22, 2),
            ("12startgridcount.bin", 0x28, 4),
            ("14groundcollnodecount.bin", 0x30, 4),
            ("16wallcollnodecount.bin", 0x38, 4),
            ("18unkcount2.bin", 0x40, 4),
            ("22unkcount3.bin", 0x50, 4),
            ("24unknightlight.bin", 0x58, 4),
        ]

        for filename, offset, length in header_field_files:
            path = os.path.join(output_folder, filename)
            with open(path, "rb") as f:
                data = f.read(length)
                header[offset:offset+length] = data

        # Open new file and write header first
        with open(runway+"_new", 'wb') as out_f:
            out_f.write(header)
            cur_offset = header_size_bytes

            # Append pointered sections
            pointer_values_new = []
            for filename in pointer_list_outputted_files:
                path = os.path.join(output_folder, filename)
                with open(path, "rb") as f:
                    data = f.read()
                    pointer_values_new.append(cur_offset)
                    out_f.write(data)
                    cur_offset += len(data)

        # Patch pointer fields and EOF
        with open(runway+"_new", 'r+b') as out_f:
            # Update pointer offsets
            for header_offset, section_offset in zip(pointer_offsets_in_file, pointer_values_new):
                out_f.seek(header_offset)
                out_f.write(struct.pack("<I", section_offset))

            # Update EOF pointer
            out_f.seek(end_of_file_pointer)
            out_f.write(struct.pack("<I", cur_offset))

        print("GTRW file building finished.")

    except FileNotFoundError:
        print("Some extracted file is missing.")
    except Exception as e:
        print("Unexpected error occurred during file building:", e)


#user action
def main():
    while True:
        print()
        user_command = input('Choose action: "B"=Build, "U"=Unpack, "E"=Exit: ')
        if user_command.lower() == "e":
            print("Exiting...")
            time.sleep(1.5)
            break
        elif user_command.lower() == "b":
            selected_runway = input("Input runway filename: ")
            create_runway_from_data(selected_runway)
        elif user_command.lower() == "u":
            selected_runway = input("Input runway filename: ")
            pointer_values = read_all_pointers_from_runway(selected_runway, pointer_list)
            print()
            read_and_dump_data_from_runway(selected_runway, pointer_values)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()