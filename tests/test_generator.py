import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from renderer import PassRenderer
from batch import generate_batch


class GeneratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.renderer = PassRenderer()

    def test_all_digit_contexts_are_available(self):
        from itertools import product
        for color, info in self.renderer.manifest['colors'].items():
            for length in [8, 9, 10]:
                for pattern in product('01', repeat=length):
                    text = ''.join(pattern)
                    pairs = [i for i in range(length - 1) if text[i:i + 2] == '11']
                    self.assertIn(f'{length}:{len(pairs)}', info['prefixes'])
                    for position, char in enumerate(text):
                        for digit in ('1' if char == '1' else '023456789'):
                            key = f'{length}:{len(pairs)}:{position}:{sum(i < position for i in pairs)}:{digit}'
                            self.assertIn(key, info['digits'], (color, key))

    def test_generation_does_not_start_external_processes(self):
        with patch('subprocess.Popen', side_effect=AssertionError('External processes are forbidden')):
            for color in ['red', 'green', 'blue']:
                for serial in [0, 11111111, 12345678, 2022020311, 9999999999]:
                    with self.subTest(color=color, serial=serial):
                        image = self.renderer.render(color, serial)
                        self.assertEqual(list(image.size), self.renderer.manifest['colors'][color]['size'])
                        self.assertEqual(image.mode, 'RGB')

    def test_invalid_serials_are_rejected(self):
        for serial in [-1, 10000000000, True, 1.5, '12345678', None]:
            with self.subTest(serial=serial), self.assertRaises(ValueError):
                self.renderer.render('green', serial)
        with self.assertRaises(ValueError):
            self.renderer.render('purple', 1)

    def test_batch_serial_order_and_archive_pixels(self):
        with tempfile.TemporaryDirectory() as folder:
            progress = []
            result = generate_batch(self.renderer, 'green', 2022020310, 10, folder,
                                    lambda done, total: progress.append((done, total)))
            self.assertEqual([p.name for p in result.files], [f'JT-{s}.png' for s in range(2022020311, 2022020321)])
            self.assertEqual(progress[-1], (10, 10))
            with zipfile.ZipFile(result.archive) as archive:
                self.assertEqual(archive.namelist(), [p.name for p in result.files])
                self.assertIsNone(archive.testzip())
                for path in result.files:
                    self.assertEqual(archive.read(path.name), path.read_bytes())
            for path, serial in zip(result.files, range(2022020311, 2022020321)):
                expected = np.asarray(self.renderer.render('green', serial))
                with Image.open(path) as image:
                    self.assertTrue(np.array_equal(np.asarray(image), expected))

    def test_invalid_batch_is_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            for current, count in [(9999999999, 1), (-1, 1), (0, 0), (0, 1000), (0, True)]:
                with self.subTest(current=current, count=count), self.assertRaises(ValueError):
                    generate_batch(self.renderer, 'green', current, count, folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_asset_hashes_and_no_office_files(self):
        manifest = self.renderer.manifest
        for name, expected in manifest['files'].items():
            self.assertEqual(hashlib.sha256((ROOT / 'assets' / name).read_bytes()).hexdigest(), expected)
            self.assertNotIn(Path(name).suffix.lower(), ['.ppt', '.pptx', '.exe', '.dll', '.ttf', '.otf'])


if __name__ == '__main__':
    unittest.main()
