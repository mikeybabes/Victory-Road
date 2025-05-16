import sys

def split_file(input_file, output_file1, output_file2, byte_count):
    try:
        byte_count = int(byte_count)
    except ValueError:
        print("Byte count should be an integer.")
        return

    try:
        with open(input_file, 'rb') as inp, open(output_file1, 'wb') as out1, open(output_file2, 'wb') as out2:
            while True:
                chunk1 = inp.read(byte_count)
                if chunk1:
                    out1.write(chunk1)
                else:
                    break

                chunk2 = inp.read(byte_count)
                if chunk2:
                    out2.write(chunk2)
                else:
                    break

        print(f"File {input_file} split successfully into {output_file1} and {output_file2}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python splittwo.py input1.bin output1.bin output2.bin bytes")
    else:
        _, input_file, output_file1, output_file2, byte_count = sys.argv
        split_file(input_file, output_file1, output_file2, byte_count)
