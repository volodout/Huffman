import pickle


def huffman_decode(encoded_text, tree):
    decoded_text = []
    node = tree
    for bit in encoded_text:
        node = node.left if bit == "0" else node.right
        if node.char is not None:
            decoded_text.append(node.char)
            node = tree
    return "".join(decoded_text)


def load_encoded_file(filepath):
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
        return data['encoded_text'], data['tree']
