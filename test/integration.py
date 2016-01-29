import sys, os

if not os.environ.get("TINIFY_KEY"):
    sys.exit("Set the TINIFY_KEY environment variable.")

import tinify, unittest, tempfile

class ClientIntegrationTest(unittest.TestCase):
    tinify.key = os.environ.get("TINIFY_KEY")

    unoptimized_path = os.path.join(os.path.dirname(__file__), 'examples', 'voormedia.png')

    def test_should_compress_from_file(self):
        source = tinify.from_file(self.unoptimized_path)
        with tempfile.NamedTemporaryFile() as tmp:
            source.to_file(tmp.name)
            self.assertTrue(0 < os.path.getsize(tmp.name) < 1500)

    def test_should_compress_from_url(self):
        source = tinify.from_url('https://raw.githubusercontent.com/tinify/tinify-python/master/test/examples/voormedia.png')
        with tempfile.NamedTemporaryFile() as tmp:
            source.to_file(tmp.name)
            self.assertTrue(0 < os.path.getsize(tmp.name) < 1500)

    def test_should_resize(self):
        source = tinify.from_file(self.unoptimized_path)
        with tempfile.NamedTemporaryFile() as tmp:
            source.resize(method="fit", width=50, height=20).to_file(tmp.name)
            self.assertTrue(0 < os.path.getsize(tmp.name) < 800)
