import argparse
import os
import hashlib
import struct

from huffman import huffman_encode, huffman_decode, save_codes, load_codes
from utils import read_file, write_file, get_file_metadata, restore_file_metadata


def calculate_checksum(data):
    return hashlib.sha256(data).digest()


def compress_file(input_file: str, output_encoded_file: str, verbose: bool):
    if output_encoded_file is None:
        output_encoded_file = input_file + '.huff'
    elif not output_encoded_file.endswith('.huff'):
        output_encoded_file += '.huff'

    data = read_file(input_file)
    checksum = calculate_checksum(data)

    encoded_data, codes = huffman_encode(data)

    encoded_int = int(encoded_data, 2)
    encoded_bytes = encoded_int.to_bytes((len(encoded_data) + 7) // 8, byteorder='big')

    with open(output_encoded_file, 'wb') as f:
        f.write(struct.pack('>I', len(encoded_data)))
        f.write(checksum)
        f.write(encoded_bytes)
        save_codes(codes, f)

    original_metadata = get_file_metadata(input_file)
    restore_file_metadata(original_metadata, output_encoded_file)

    print(f'Файл "{input_file}" успешно сжат в "{output_encoded_file}"')

    if verbose:
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_encoded_file)
        compression_ratio = 100 * (1 - compressed_size / original_size)
        print(f"Файл сжат на {compression_ratio:.2f}%")


def decompress_file(encoded_input_file: str, decoded_output_file: str):
    if not decoded_output_file:
        decoded_output_file = encoded_input_file.replace('.huff', '')
    decoded_output_file = create_filename_to_decompress(decoded_output_file)

    with open(encoded_input_file, 'rb') as f:
        bit_length = struct.unpack('>I', f.read(4))[0]  # Длина битов
        stored_checksum = f.read(32)  # Контрольная сумма

        encoded_bytes = f.read((bit_length + 7) // 8)
        encoded_int = int.from_bytes(encoded_bytes, byteorder='big')
        encoded_data = bin(encoded_int)[2:].zfill(bit_length)  # Преобразуем в строку бит

        codes = load_codes(f)

        decoded_data = huffman_decode(encoded_data, codes)

        calculated_checksum = calculate_checksum(decoded_data)
        if stored_checksum != calculated_checksum:
            raise ValueError("Ошибка: контрольная сумма не совпадает. Файл повреждён!")

        write_file(decoded_output_file, decoded_data)

        original_metadata = get_file_metadata(encoded_input_file)
        restore_file_metadata(original_metadata, decoded_output_file)

        print(f'Файл "{encoded_input_file}" успешно распакован в "{decoded_output_file}"')


def create_filename_to_decompress(filename: str):
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

    parser.add_argument('-v', '--verbose', action='store_true', help='Показать процент сжатия')

    args = parser.parse_args()

    if args.decompress and not args.decompress.endswith('.huff'):
        raise ValueError('Архивированный файл должен иметь расширение .huff')

    if args.compress:
        compress_file(args.compress, args.output, args.verbose)
    elif args.decompress:
        decompress_file(args.decompress, args.output)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
