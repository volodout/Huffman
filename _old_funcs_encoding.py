import pickle
from _old_build_tree import build_tree


def build_codes(node, prefix="", codebook={}):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook


def huffman_encode(text):
    tree = build_tree(text)
    codebook = build_codes(tree)
    encoded_text = "".join(codebook[char] for char in text)
    return encoded_text, tree


def save_encoded_file(encoded_text, tree, filepath):
    with open(filepath, 'wb') as f:
        data = {
            'tree': tree,
            'encoded_text': encoded_text
        }
        pickle.dump(data, f)