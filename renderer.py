"""Deterministic PNG rendering from calibrated bitmap assets; no Office calls."""
from functools import lru_cache
import hashlib
import json
from importlib.metadata import version
from pathlib import Path

import numpy as np
from PIL import Image
from reportlab.graphics.barcode import qr

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets'


class PassRenderer:
    def __init__(self, assets=ASSETS, verify_assets=True):
        self.assets = Path(assets)
        self.manifest = json.loads((self.assets / 'manifest.json').read_text(encoding='utf-8'))
        if self.manifest.get('schema_version') != 2:
            raise ValueError('Unsupported calibrated asset version.')
        for package, required in self.manifest.get('dependency_versions', {}).items():
            if version(package) != required:
                raise ValueError(f'{package} must be version {required}. Install the versions in requirements.txt.')
        if verify_assets:
            for name, expected in self.manifest['files'].items():
                actual = hashlib.sha256((self.assets / name).read_bytes()).hexdigest()
                if actual != expected:
                    raise ValueError(f'Calibrated asset was changed: {name}')

    @lru_cache(maxsize=3)
    def _base(self, color):
        with Image.open(self.assets / self.manifest['colors'][color]['base']) as source:
            return source.convert('RGB')

    @lru_cache(maxsize=512)
    def _sprite(self, name):
        with Image.open(self.assets / name) as source:
            return source.convert('RGB')

    @lru_cache(maxsize=3)
    def _qr_sampling(self, color):
        with np.load(self.assets / color / 'qr-sampling.npz', allow_pickle=False) as data:
            samples, rows, columns = data['samples'], data['rows'], data['columns']
        yy, xx = np.indices(samples.shape[1:])
        return samples, rows, columns, yy, xx

    @staticmethod
    def qr_matrix(serial_text):
        widget = qr.QrCodeWidget('109-JT-' + serial_text, qrVersion=2, barLevel='M')
        widget.qr.make()
        matrix = np.asarray(widget.qr.modules, dtype=np.uint8)
        if matrix.shape != (25, 25):
            raise ValueError('Expected a 25 by 25 QR code.')
        return matrix

    def render(self, color, serial):
        if color not in self.manifest['colors']:
            raise ValueError('Color must be red, green, or blue.')
        if isinstance(serial, bool) or not isinstance(serial, int) or not 0 <= serial <= 9999999999:
            raise ValueError('Serial must be an integer from 0 to 9999999999.')
        serial_text = f'{serial:08d}'
        length = len(serial_text)
        info = self.manifest['colors'][color]
        output = self._base(color).copy()
        pairs = [i for i in range(length - 1) if serial_text[i:i + 2] == '11']
        prefix = info['prefixes'][f'{length}:{len(pairs)}']
        output.paste(self._sprite(prefix['file']), tuple(prefix['xy']))
        for position, digit in enumerate(serial_text):
            key = f'{length}:{len(pairs)}:{position}:{sum(i < position for i in pairs)}:{digit}'
            glyph = info['digits'][key]
            output.paste(self._sprite(glyph['file']), tuple(glyph['xy']))

        matrix = np.pad(self.qr_matrix(serial_text), 1)
        samples, rows, columns, yy, xx = self._qr_sampling(color)
        indices = np.zeros(samples.shape[1:], dtype=np.uint8)
        for r in [rows - 1, rows]:
            for c in [columns - 1, columns]:
                values = matrix[r[:, None] + 1, c[None, :] + 1]
                shift = ((r[:, None] % 2) * 2 + c[None, :] % 2).astype(np.uint8)
                indices |= values << shift
        patch = samples[indices, yy, xx]
        output.paste(Image.fromarray(patch).convert('RGB'), tuple(info['qr_patch'][:2]))
        return output
