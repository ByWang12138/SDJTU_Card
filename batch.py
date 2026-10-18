"""PNG-only batch generation; called by the desktop application."""
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import uuid
import zipfile

from renderer import PassRenderer


@dataclass(frozen=True)
class BatchResult:
    directory: Path
    archive: Path
    files: tuple[Path, ...]


def generate_batch(renderer: PassRenderer, color, current_serial, count, output_root, progress=None):
    if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= 999:
        raise ValueError('Quantity must be an integer from 1 to 999.')
    if isinstance(current_serial, bool) or not isinstance(current_serial, int) or current_serial < 0:
        raise ValueError('The current serial must be a nonnegative integer.')
    if current_serial + count > 9999999999:
        raise ValueError('The final serial must not exceed 9999999999.')
    if color not in renderer.manifest['colors']:
        raise ValueError('Color must be red, green, or blue.')
    root = Path(output_root)
    if not root.is_dir():
        raise ValueError('The configured output directory does not exist. Create it before generating images.')
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    directory = root / f'{color}_{current_serial + 1:08d}-{current_serial + count:08d}_{stamp}_{uuid.uuid4().hex[:6]}'
    directory.mkdir()
    files = []
    for offset in range(1, count + 1):
        serial = current_serial + offset
        image = renderer.render(color, serial)
        path = directory / f'JT-{serial:08d}.png'
        image.save(path, format='PNG')
        files.append(path)
        if progress is not None:
            progress(offset, count)
    archive = directory.with_suffix('.zip')
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as package:
        for path in files:
            package.write(path, path.name)
    return BatchResult(directory, archive, tuple(files))
