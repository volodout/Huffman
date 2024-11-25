import unittest
import os
from main import compress_file, decompress_file, calculate_checksum
from utils import read_file, get_file_metadata


class TestArchiver(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test.txt'
        self.compressed_file = 'test.txt.huff'
        self.decompressed_file = 'test_decompressed.txt'

        with open(self.test_file, 'w') as f:
            f.write('This is a test file for Huffman compression.')

    def tearDown(self):
        for file in [self.test_file, self.compressed_file, self.decompressed_file]:
            if os.path.exists(file):
                os.remove(file)

    def test_compress_file_creates_compressed_file(self):
        compress_file(self.test_file, self.compressed_file, verbose=False)
        self.assertTrue(os.path.exists(self.compressed_file))

    def test_decompress_file_creates_correct_output(self):
        compress_file(self.test_file, self.compressed_file, verbose=False)
        decompress_file(self.compressed_file, self.decompressed_file)

        with open(self.test_file, 'rb') as original, open(self.decompressed_file, 'rb') as decompressed:
            self.assertEqual(original.read(), decompressed.read())

    def test_checksum_integrity(self):
        data = read_file(self.test_file)
        checksum = calculate_checksum(data)
        compress_file(self.test_file, self.compressed_file, verbose=False)

        decompress_file(self.compressed_file, self.decompressed_file)
        decompressed_data = read_file(self.decompressed_file)

        self.assertEqual(checksum, calculate_checksum(decompressed_data))

    def test_compress_and_decompress_metadata(self):
        original_metadata = get_file_metadata(self.test_file)
        compress_file(self.test_file, self.compressed_file, verbose=False)
        decompress_file(self.compressed_file, self.decompressed_file)

        decompressed_metadata = get_file_metadata(self.decompressed_file)

        self.assertEqual(original_metadata.st_mode, decompressed_metadata.st_mode)
        self.assertAlmostEqual(original_metadata.st_mtime, decompressed_metadata.st_mtime, delta=1)

    def test_compress_with_verbose_flag(self):
        compress_file(self.test_file, self.compressed_file, verbose=True)

        original_size = os.path.getsize(self.test_file)
        compressed_size = os.path.getsize(self.compressed_file)
        compression_ratio = 100 * (1 - compressed_size / original_size)


        self.assertGreater(abs(compression_ratio), 0)

    def test_compress_and_decompress_empty_file(self):
        empty_file = 'empty.txt'
        compressed_empty_file = 'empty.txt.huff'
        decompressed_empty_file = 'empty_decompressed.txt'

        try:
            with open(empty_file, 'wb') as f:
                f.write(b'')

            compress_file(empty_file, compressed_empty_file, verbose=False)
            decompress_file(compressed_empty_file, decompressed_empty_file)

            with open(empty_file, 'rb') as original, open(decompressed_empty_file, 'rb') as decompressed:
                self.assertEqual(original.read(), decompressed.read())
        finally:
            for file in [empty_file, compressed_empty_file, decompressed_empty_file]:
                if os.path.exists(file):
                    os.remove(file)

if __name__ == '__main__':
    unittest.main()
