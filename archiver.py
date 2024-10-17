import argparse
import os
from huffman import huffman_encode, huffman_decode, save_codes, load_codes
from utils import read_file, write_file, get_file_metadata, restore_file_metadata


def bits_to_bytes(bits):
    """Конвертирует строку битов в байтовый массив."""
    byte_array = bytearray()
    for i in range(0, len(bits), 8):
        byte = bits[i:i + 8]
        if len(byte) < 8:
            byte = byte.ljust(8, '0')  # Дополняем до 8 бит
        byte_array.append(int(byte, 2))
    return byte_array


def bytes_to_bits(byte_data):
    """Конвертирует байтовый массив в строку битов."""
    bits = ''
    for byte in byte_data:
        bits += bin(byte)[2:].rjust(8, '0')  # Преобразуем в двоичное представление
    return bits


def compress_file(input_file, output_file):
    data = read_file(input_file)
    encoded_data, codes = huffman_encode(data.decode('utf-8', errors='ignore'))

    # Конвертируем биты в байты
    byte_data = bits_to_bytes(encoded_data)
    write_file(output_file, byte_data)

    # Сохранение кодов в отдельный файл
    codes_file = output_file + '.codes'
    save_codes(codes, codes_file)

    original_metadata = get_file_metadata(input_file)
    restore_file_metadata(original_metadata, output_file)

    print(f'Файл "{input_file}" успешно сжат в "{output_file}" с кодами в "{codes_file}"')


def decompress_file(input_file, output_file):
    byte_data = read_file(input_file)

    # Конвертируем байты в биты
    encoded_data = bytes_to_bits(byte_data)

    # Загрузка кодов из файла
    codes_file = input_file + '.codes'
    codes = load_codes(codes_file)

    decoded_data = huffman_decode(encoded_data, codes)
    write_file(output_file, decoded_data.encode('utf-8'))

    original_metadata = get_file_metadata(input_file)
    restore_file_metadata(original_metadata, output_file)

    print(f'Файл "{input_file}" успешно распакован в "{output_file}"')


def main():
    parser = argparse.ArgumentParser(description='Huffman Archiver')
    parser.add_argument('mode', choices=['compress', 'decompress'], help='Режим работы: compress или decompress')
    parser.add_argument('input', help='Входной файл')
    parser.add_argument('output', help='Выходной файл')

    args = parser.parse_args()

    if args.mode == 'compress':
        compress_file(args.input, args.output)
    elif args.mode == 'decompress':
        decompress_file(args.input, args.output)


if __name__ == '__main__':
    main()
