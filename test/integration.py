import sys, os

if not os.environ.get("TINIFY_KEY"):
    sys.exit("Set the TINIFY_KEY environment variable.")

import tinify, unittest, tempfile

class ClientIntegrationTest(unittest.TestCase):
    tinify.key = os.environ.get("TINIFY_KEY")
    tinify.proxy = os.environ.get("TINIFY_PROXY")

    unoptimized_path = os.path.join(os.path.dirname(__file__), 'examples', 'voormedia.png')
    optimized = tinify.from_file(unoptimized_path)

    def test_should_compress_from_file(self):
        with tempfile.NamedTemporaryFile() as tmp:
            self.optimized.to_file(tmp.name)

            size = os.path.getsize(tmp.name)
            contents = tmp.read()

            self.assertTrue(1000 < size < 1500)

            # width == 137
            self.assertIn(b'\x00\x00\x00\x89', contents)
            self.assertNotIn(b'Copyright Voormedia', contents)

    def test_should_compress_from_url(self):
        source = tinify.from_url('https://raw.githubusercontent.com/tinify/tinify-python/master/test/examples/voormedia.png')
        with tempfile.NamedTemporaryFile() as tmp:
            source.to_file(tmp.name)

            size = os.path.getsize(tmp.name)
            contents = tmp.read()

            self.assertTrue(1000 < size < 1500)

            # width == 137
            self.assertIn(b'\x00\x00\x00\x89', contents)
            self.assertNotIn(b'Copyright Voormedia', contents)

    def test_should_resize(self):
        with tempfile.NamedTemporaryFile() as tmp:
            self.optimized.resize(method="fit", width=50, height=20).to_file(tmp.name)

            size = os.path.getsize(tmp.name)
            contents = tmp.read()

            self.assertTrue(500 < size < 1000)

            # width == 50
            self.assertIn(b'\x00\x00\x00\x32', contents)
            self.assertNotIn(b'Copyright Voormedia', contents)

    def test_should_preserve_metadata(self):
        with tempfile.NamedTemporaryFile() as tmp:
            self.optimized.preserve("copyright", "creation").to_file(tmp.name)

            size = os.path.getsize(tmp.name)
            contents = tmp.read()

            self.assertTrue(1000 < size < 2000)

            # width == 137
            self.assertIn(b'\x00\x00\x00\x89', contents)
            self.assertIn(b'Copyright Voormedia', contents)
