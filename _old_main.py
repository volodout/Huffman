import argparse
from _old_funcs_decoding import *
from _old_funcs_encoding import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["encode", "decode"], help="Mode: encode or decode")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")

    args = parser.parse_args()

    if args.mode == "encode":
        with open(args.input, encoding="utf-8") as f:
            text = f.read()
        encoded_text, tree = huffman_encode(text)
        save_encoded_file(encoded_text, tree, args.output)

    elif args.mode == "decode":
        encoded_text, tree = load_encoded_file(args.input)
        decoded_text = huffman_decode(encoded_text, tree)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(decoded_text)


if __name__ == "__main__":
    main()
