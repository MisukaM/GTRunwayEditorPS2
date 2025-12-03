# GT4RNW4Editor
import os
import struct
import time

print("GT4RNW4Editor - Made by Misuka. Based on research done by Nenkai. Further help from angel hunter!")

# header struct; based on research on the format by Nenkai.
header_size_bytes = 0xC0  # 0xC0 header length
magic = 0x0  # RNW4
RelocatePtr = 0x4  # int32
RelocateFileSize = 0x8  # EOF pointer stored in header
Flags = 0xC  # int32
Version = 0x10
CourseLength = 0x14
StartVCoord = 0x18
GoalVCoord = 0x1C
BoundsSetMin = 0x20
BoundsSetMax = 0x2C
CheckpointListCount = 0x38
GridCount = 0x3A
CheckpointCount = 0x3C
CheckpointLookupIndicesCount = 0x3E
UnkEmpty_0x40 = 0x40
GadgetsCount = 0x44
RoadVerticesCount = 0x46
RoadTriCount = 0x48
ClusterCount = 0x4A
KdTreeMaxDepth = 0x4C
BoundVerticesCount = 0x4E
UnkCount = 0x50
PitstopCount = 0x52
SectionCount = 0x54
UnkEmpty_0x56 = 0x56

# pointer header offsets (where pointer uint32s are stored in header)
CheckpointListOffset = 0x58
GridsOffset = 0x5C
CheckpointsOffset = 0x60
CheckpointLookupIndicesOffset = 0x64
LightSetsOffset = 0x68
unkOffset = 0x6C
GadgetsOffsets = 0x70
RoadVerticesOffset = 0x74
RoadTrisOffset = 0x78
ClusterListOffset = 0x7C
CollisionKDTreeOffset = 0x80
BoundVerticesOffset = 0x84
BoundIndicesCount = 0x88
BoundIndicesOffset = 0x8C
PitStopsOffset = 0x90
TireSoundRelatedFlagsMaybe = 0x94
Unk_0x98 = 0x98
SectionsOffset = 0x9C

pointer_list = (
    CheckpointListOffset, GridsOffset, CheckpointsOffset, CheckpointLookupIndicesOffset, LightSetsOffset, unkOffset,
    GadgetsOffsets, RoadVerticesOffset, RoadTrisOffset, ClusterListOffset, CollisionKDTreeOffset, BoundVerticesOffset,
    BoundIndicesOffset, PitStopsOffset, SectionsOffset
)

# Files produced by the extractor (one per pointer index)
pointer_list_outputted_files = (
    "26CheckpointListOffset.bin",
    "27GridsOffset.bin",
    "28CheckpointsOffset.bin",
    "29CheckpointLookupIndicesOffset.bin",
    "30LightSetsOffset.bin",
    "31unkOffset.bin",
    "32GadgetsOffsets.bin",
    "33RoadVerticesOffset.bin",
    "34RoadTrisOffset.bin",
    "35ClusterListOffset.bin",
    "36CollisionKDTreeOffset.bin",
    "37BoundVerticesOffset.bin",
    "39BoundIndicesOffset.bin",
    "40PitStopsOffset.bin",
    "43SectionsOffset.bin",
)

# Where to write the pointers back into header
pointer_offsets_in_file = (
    0x58, 0x5C, 0x60, 0x64, 0x68, 0x6C, 0x70, 0x74, 0x78, 0x7C, 0x80, 0x84, 0x8C, 0x90, 0x9C
)


def read_all_pointers_from_runway(runway, pointers):
    """
    Read uint32 pointers from header offsets in 'pointers' (list of header offsets).
    Returns list of integer pointer values, same order as pointers parameter.
    """
    results = []
    try:
        with open(runway, "rb") as f:
            for offset in pointers:
                f.seek(offset, 0)
                raw = f.read(4)
                if len(raw) < 4:
                    raise EOFError(f"Header truncated while reading pointer at offset {offset}")
                value = struct.unpack("<I", raw)[0]
                results.append(value)
        return results
    except Exception as e:
        print("Unexpected problem occurred during reading pointers:", e)
        return None


def read_and_dump_data_from_runway(runway, pointer_ranges=None):
    """
    Robust extractor:
      - reads pointers from header
      - sorts pointers by absolute pointer value (file layout order)
      - extracts each distinct region (ptr -> next_ptr or EOF)
      - writes the per-index files (pointer_list_outputted_files) so that indices that pointed to same pointer value get same content
    """
    try:
        with open(runway, "rb") as f:
            output_folder = runway + "_out"
            os.makedirs(output_folder, exist_ok=True)

            # read header-static fields and write them out (unchanged)
            def dump_static(offset, length, outname):
                f.seek(offset, 0)
                data = f.read(length)
                with open(os.path.join(output_folder, outname), "wb") as out_file:
                    print(f"Dumping {outname} to {os.path.join(output_folder, outname)}")
                    out_file.write(data)

            dump_static(magic, 4, "01magic.bin")
            dump_static(RelocatePtr, 4, "02RelocatePtr.bin")
            dump_static(RelocateFileSize, 4, "03RelocateFileSize.bin")
            dump_static(Flags, 4, "04Flags.bin")
            dump_static(Version, 4, "05Version.bin")
            dump_static(CourseLength, 4, "06CourseLength.bin")
            dump_static(StartVCoord, 4, "07StartVCoord.bin")
            dump_static(GoalVCoord, 4, "08GoalVCoord.bin")
            dump_static(BoundsSetMin, 12, "09BoundsSetMin.bin")
            dump_static(BoundsSetMax, 12, "10BoundsSetMax.bin")
            dump_static(CheckpointListCount, 2, "11CheckpointListCount.bin")
            dump_static(GridCount, 2, "12GridCount.bin")
            dump_static(CheckpointCount, 2, "13CheckpointCount.bin")
            dump_static(CheckpointLookupIndicesCount, 2, "14CheckpointLookupIndicesCount.bin")
            dump_static(UnkEmpty_0x40, 4, "15UnkEmpty_0x40.bin")
            dump_static(GadgetsCount, 2, "16GadgetsCount.bin")
            dump_static(RoadVerticesCount, 2, "17RoadVerticesCount.bin")
            dump_static(RoadTriCount, 2, "18RoadTriCount.bin")
            dump_static(ClusterCount, 2, "19ClusterCount.bin")
            dump_static(KdTreeMaxDepth, 2, "20KdTreeMaxDepth.bin")
            dump_static(BoundVerticesCount, 2, "21BoundVerticesCount.bin")
            dump_static(UnkCount, 2, "22UnkCount.bin")
            dump_static(PitstopCount, 2, "23PitstopCount.bin")
            dump_static(SectionCount, 2, "24SectionCount.bin")
            dump_static(UnkEmpty_0x56, 2, "25UnkEmpty_0x56.bin")

            # get EOF once
            f.seek(0, 2)
            eof = f.tell()
            print("File EOF:", eof)

            # read pointers from header
            raw_pointers = read_all_pointers_from_runway(runway, pointer_list)
            if raw_pointers is None:
                raise RuntimeError("Failed to read header pointers")

            # Build (index, ptr) list and sort by ptr value (file order)
            indexed = list(enumerate(raw_pointers))  # list of (index, ptr)
            # For sorting, treat ptr==0 as special: we'll place them at front but they represent 'no section'
            # However, to ensure correct layout we will skip ptr==0 for extraction (no data)
            sorted_by_ptr = sorted([x for x in indexed if x[1] != 0], key=lambda x: x[1])

            # Create mapping: ptr_value -> data bytes (read only once)
            ptr_to_data = {}
            # Also mapping ptr_value -> list of indices that referenced it
            ptr_to_indices = {}
            for idx, ptr in indexed:
                ptr_to_indices.setdefault(ptr, []).append(idx)

            # Compute distinct sorted pointer list (excluding 0)
            distinct_sorted_ptrs = sorted({ptr for (_, ptr) in sorted_by_ptr})

            # For each distinct ptr, find its end border (next larger ptr or EOF), read region
            for i, ptr in enumerate(distinct_sorted_ptrs):
                # next_end is next distinct ptr greater than current, or EOF
                next_end = None
                for candidate in distinct_sorted_ptrs:
                    if candidate > ptr:
                        next_end = candidate
                        break
                if next_end is None:
                    next_end = eof
                # Defensive checks
                if ptr >= eof:
                    # pointer points beyond EOF - skip and map to empty bytes
                    print(f"Pointer {ptr} >= EOF ({eof}), writing empty region for it")
                    ptr_to_data[ptr] = b""
                    continue
                if next_end <= ptr:
                    print(f"Non-increasing region for ptr {ptr} -> next_end {next_end}; skipping")
                    ptr_to_data[ptr] = b""
                    continue
                read_len = next_end - ptr
                f.seek(ptr, 0)
                data = f.read(read_len)
                if len(data) != read_len:
                    print(f"Warning: read {len(data)} bytes for ptr {ptr}, expected {read_len}")
                ptr_to_data[ptr] = data
                print(f"Extracted region ptr=0x{ptr:08X} size={len(data)} (ends at 0x{next_end:08X})")

            # Now write per-index files (use pointer_list_outputted_files order)
            # For ptr == 0 we'll create an empty file to keep indices aligned.
            for idx, outname in enumerate(pointer_list_outputted_files):
                ptr = raw_pointers[idx]
                outpath = os.path.join(output_folder, outname)
                data = ptr_to_data.get(ptr, b"")
                with open(outpath, "wb") as out_f:
                    out_f.write(data)
                print(f"Wrote {outname} for pointer index {idx} (orig ptr=0x{ptr:08X}) size={len(data)}")

            # Also dump bound-indices count and dynamic small fields that we kept earlier
            f.seek(BoundIndicesCount, 0)
            BoundIndicesCount_data = f.read(4)
            with open(os.path.join(output_folder, "38BoundIndicesCount.bin"), "wb") as out_f:
                out_f.write(BoundIndicesCount_data)
                print("Dumped 38BoundIndicesCount.bin")

            f.seek(TireSoundRelatedFlagsMaybe, 0)
            TireSoundRelatedFlagsMaybe_data = f.read(4)
            with open(os.path.join(output_folder, "41TireSoundRelatedFlagsMaybe.bin"), "wb") as out_f:
                out_f.write(TireSoundRelatedFlagsMaybe_data)
                print("Dumped 41TireSoundRelatedFlagsMaybe.bin")

            f.seek(Unk_0x98, 0)
            Unk_0x98_data = f.read(4)
            with open(os.path.join(output_folder, "42Unk_0x98.bin"), "wb") as out_f:
                out_f.write(Unk_0x98_data)
                print("Dumped 42Unk_0x98.bin")

            print("RNW4 extraction completed.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print("An unexpected error occurred during file extracting:", e)


def create_runway_from_data(runway):
    """
    Rebuild runway_new from the extracted files in runway_out folder.
    Algorithm:
      - read original pointers from the original source file to preserve equality & mapping
      - compute unique pointer values and sort them (file layout order)
      - write data blocks in sorted order (only once per unique pointer)
      - build mapping original_index -> new_offset (reuse offsets for duplicates)
      - patch header with new offsets and EOF
    """
    try:
        output_folder = runway + "_out"

        # Build header bytes from header_field_files
        header = bytearray(header_size_bytes)
        header_field_files = [
            ("01magic.bin", 0x0, 4),
            ("02RelocatePtr.bin", 0x4, 4),
            ("03RelocateFileSize.bin", 0x8, 4),
            ("04Flags.bin", 0xC, 4),
            ("05Version.bin", 0x10, 4),
            ("06CourseLength.bin", 0x14, 4),
            ("07StartVCoord.bin", 0x18, 4),
            ("08GoalVCoord.bin", 0x1C, 4),
            ("09BoundsSetMin.bin", 0x20, 12),
            ("10BoundsSetMax.bin", 0x2C, 12),
            ("11CheckpointListCount.bin", 0x38, 2),
            ("12GridCount.bin", 0x3A, 2),
            ("13CheckpointCount.bin", 0x3C, 2),
            ("14CheckpointLookupIndicesCount.bin", 0x3E, 2),
            ("15UnkEmpty_0x40.bin", 0x40, 4),
            ("16GadgetsCount.bin", 0x44, 2),
            ("17RoadVerticesCount.bin", 0x46, 2),
            ("18RoadTriCount.bin", 0x48, 2),
            ("19ClusterCount.bin", 0x4A, 2),
            ("20KdTreeMaxDepth.bin", 0x4C, 2),
            ("21BoundVerticesCount.bin", 0x4E, 2),
            ("22UnkCount.bin", 0x50, 2),
            ("23PitstopCount.bin", 0x52, 2),
            ("24SectionCount.bin", 0x54, 2),
            ("25UnkEmpty_0x56.bin", 0x56, 2),
            ("38BoundIndicesCount.bin", 0x88, 4),
            ("41TireSoundRelatedFlagsMaybe.bin", 0x94, 4),
            ("42Unk_0x98.bin", 0x98, 4),
        ]

        for filename, offset, length in header_field_files:
            path = os.path.join(output_folder, filename)
            if not os.path.exists(path):
                raise FileNotFoundError(path)
            with open(path, "rb") as f:
                data = f.read(length)
                if len(data) != length:
                    # be defensive but still copy what is available
                    print(f"Warning: header field file {filename} has {len(data)} bytes, expected {length}")
                header[offset:offset + len(data)] = data

        # Open target file and write header + sections
        with open(runway + "_new", "wb") as out_f:

            out_f.write(header)
            cur_offset = header_size_bytes

            # Read original pointers from the source original file (so we preserve equalities)
            original_pointers = read_all_pointers_from_runway(runway, pointer_list)
            if original_pointers is None:
                raise RuntimeError("Failed to read original pointers from source runway file.")

            # Build list of (index, ptr) and sort by ptr (treat ptr==0 as no block)
            indexed = list(enumerate(original_pointers))
            sorted_entries = sorted([x for x in indexed if x[1] != 0], key=lambda x: x[1])

            # Distinct sorted pointer values in file-order
            distinct_sorted_ptrs = sorted({ptr for (_, ptr) in sorted_entries})

            # Map original pointer value -> new offset assigned (for reuse)
            origptr_to_newoffset = {}
            # Map original index -> new offset (for final header patch)
            pointer_values_new = [0] * len(original_pointers)

            # For each distinct pointer value in file order, find one representative index to read file data
            for ptr in distinct_sorted_ptrs:
                # Gather indices that used this original ptr
                indices = [idx for idx, p in indexed if p == ptr]
                # Representative index: take first in indices
                rep_idx = indices[0]

                # Corresponding extractor filename that holds this data (we wrote extractor output earlier)
                data_filename = pointer_list_outputted_files[rep_idx]
                data_path = os.path.join(output_folder, data_filename)
                if not os.path.exists(data_path):
                    raise FileNotFoundError(f"Missing extracted data file required for build: {data_path}")

                with open(data_path, "rb") as dfile:
                    data = dfile.read()

                # Write this block once
                out_f.write(data)
                assigned_offset = cur_offset
                print(f"Wrote block for orig ptr 0x{ptr:08X} from '{data_filename}' at new offset 0x{assigned_offset:08X} size={len(data)}")
                cur_offset += len(data)

                # Record mapping for all indices that referenced this original pointer
                origptr_to_newoffset[ptr] = assigned_offset
                for idx in indices:
                    pointer_values_new[idx] = assigned_offset

            # Handle indices where original pointer was 0 -> keep 0 (pointer_values_new already default 0)
            # Now pointer_values_new contains new offsets in the same order as pointer_list
            # Close out_f by leaving with-block

        # Now patch header fields in read+write mode
        with open(runway + "_new", "r+b") as out_f:
            # For safety ensure pointer_values_new length matches pointer_offsets_in_file
            if len(pointer_values_new) != len(pointer_offsets_in_file):
                raise RuntimeError("pointer_values_new length mismatch")

            for header_offset, section_offset in zip(pointer_offsets_in_file, pointer_values_new):
                out_f.seek(header_offset)
                out_f.write(struct.pack("<I", section_offset))
                print(f"Patched header offset 0x{header_offset:02X} -> 0x{section_offset:08X}")

            # Patch EOF
            out_f.seek(RelocateFileSize)
            out_f.write(struct.pack("<I", cur_offset))
            print(f"Patched EOF pointer at header {RelocateFileSize} -> {cur_offset}")

        print("RNW4 file building finished.")

    except FileNotFoundError as e:
        print("Some extracted file is missing:", e)
    except Exception as e:
        print("Unexpected error occurred during file building:", e)


# user action
def main():
    while True:
        print()
        user_command = input('Choose action: "B"=Build, "U"=Unpack, "E"=Exit: ')
        if user_command.lower() == "e":
            print("Exiting...")
            time.sleep(1.5)
            break
        elif user_command.lower() == "b":
            selected_runway = input("Input runway filename (without _new): ")
            create_runway_from_data(selected_runway)
        elif user_command.lower() == "u":
            selected_runway = input("Input runway filename: ")
            print()
            read_and_dump_data_from_runway(selected_runway)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
