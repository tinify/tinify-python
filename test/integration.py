import sys, os

if os.environ.get("TRAVIS_PULL_REQUEST") and os.environ.get("TRAVIS_PULL_REQUEST") != "false":
    sys.exit(0)

if not os.environ.get("TINIFY_KEY"):
    sys.exit("Set the TINIFY_KEY environment variable.")

import tinify, unittest, tempfile

class ClientIntegrationTest(unittest.TestCase):
    tinify.key = os.environ.get("TINIFY_KEY")

    unoptimized_path = os.path.join(os.path.dirname(__file__), 'examples', 'voormedia.png')
    optimized = tinify.from_file(unoptimized_path)

    def test_should_compress(self):
        with tempfile.NamedTemporaryFile() as tmp:
            self.optimized.to_file(tmp.name)
            self.assertTrue(os.path.getsize(tmp.name) < 1500)

    def test_should_resize(self):
        with tempfile.NamedTemporaryFile() as tmp:
            self.optimized.resize(method="fit", width=50, height=20).to_file(tmp.name)
            self.assertTrue(os.path.getsize(tmp.name) < 800)
