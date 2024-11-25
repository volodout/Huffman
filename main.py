import argparse
import os

from huffman import huffman_encode, huffman_decode, save_codes, load_codes
from utils import read_file, write_file, get_file_metadata, restore_file_metadata


def bits_to_bytes(bits):
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:
            byte = byte.ljust(8, '0')
        byte_array.append(int(byte, 2))
    return byte_array


def bytes_to_bits(byte_data):
    bits = ''
    for byte in byte_data:
        bits += bin(byte)[2:].rjust(8, '0')
    return bits


def compress_file(input_file, output_encoded_file):
    if output_encoded_file is None:
        output_encoded_file = input_file + '.huff'
    elif not output_encoded_file.endswith('.huff'):
        output_encoded_file += '.huff'
    data = read_file(input_file)
    encoded_data, codes = huffman_encode(data)

    byte_data = bits_to_bytes(encoded_data)

    with open(output_encoded_file, 'wb') as f:
        length = len(byte_data)
        f.write(length.to_bytes(4, byteorder='big'))
        f.write(byte_data)
        save_codes(codes, f)

    original_metadata = get_file_metadata(input_file)
    restore_file_metadata(original_metadata, output_encoded_file)

    print(f'Файл "{input_file}" успешно сжат в "{output_encoded_file}"')


def decompress_file(encoded_input_file, decoded_output_file):
    if not decoded_output_file:
        decoded_output_file = encoded_input_file.replace('.huff', '')
    decoded_output_file = create_filename_to_decompress(decoded_output_file)
    with open(encoded_input_file, 'rb') as f:
        length_bytes = f.read(4)
        length = int.from_bytes(length_bytes, byteorder='big')

        byte_data = f.read(length)

        encoded_data = bytes_to_bits(byte_data)

        codes = load_codes(f)

        decoded_data = huffman_decode(encoded_data, codes)
        write_file(decoded_output_file, decoded_data)

        original_metadata = get_file_metadata(encoded_input_file)
        restore_file_metadata(original_metadata, decoded_output_file)

        print(f'Файл "{encoded_input_file}" успешно распакован в "{decoded_output_file}"')


def create_filename_to_decompress(filename):
    count = 1
    root, ext = os.path.splitext(filename)
    new_filename = root
    while True:
        if os.path.exists(new_filename + ext):
            new_filename = f'{root}({count})'
            count += 1
            continue
        else:
            break
    return new_filename + ext


def main():
    parser = argparse.ArgumentParser(description='Архиватор файлов')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-c', '--compress', type=str, metavar='input', help='Сжать файл', required=False)
    group.add_argument('-d', '--decompress', type=str, metavar='input', help='Распаковать файл', required=False)

    parser.add_argument('output', type=str, nargs='?', default=None, help='Выходной файл для распаковки')

    args = parser.parse_args()

    if args.decompress and not args.decompress.endswith('.huff'):
        raise ValueError('Архивированный файл должен иметь расширение .huff')

    if args.compress:
        compress_file(args.compress, args.output)
    elif args.decompress:
        decompress_file(args.decompress, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()


# контроль целостности
# прогресс бары
# тесты
# архивировать несколько файлов
# директории
# -v процент сжатия