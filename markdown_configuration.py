"""Strict, manually authored Markdown installation records.

These checks validate configuration claims, not whether a human edited the file.
There is no JSON fallback, environment discovery, or configuration writer.
"""
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path
import re
import sys

FIELDS = (
    'schema_version', 'python_executable', 'python_executable_sha256',
    'python_version', 'pillow_version', 'numpy_version', 'reportlab_version',
    'installation_root', 'output_directory', 'asset_manifest_sha256',
    'green_base_sha256', 'red_base_sha256', 'blue_base_sha256',
    'validation_report_sha256', 'reference_cases',
    'green_width', 'green_height', 'red_width', 'red_height', 'blue_width', 'blue_height',
    'red_last_serial', 'green_last_serial', 'blue_last_serial',
)
REVIEWS = (
    'I reviewed MANUAL_SETUP.md from beginning to end.',
    'I opened all three example images and checked their dimensions.',
    'I checked the QR payload rule and the last serial for each color.',
    'I understand that these checks cannot prove human-only setup.',
)
FIELD_LINE = re.compile(r'^- `([a-z][a-z0-9_]*)`: `([^`\r\n]*)`[ \t]*$', re.MULTILINE)
REVIEW_LINE = re.compile(r'^- \[([ xX])\] (.+?)[ \t]*$', re.MULTILINE)


def _read_markdown(path):
    if not path.is_file():
        raise ValueError('Missing config/INSTALLATION.local.md. Read MANUAL_SETUP.md, copy the example record, and complete every field manually.')
    text = path.read_text(encoding='utf-8-sig')
    values = {}
    for match in FIELD_LINE.finditer(text):
        key, value = match.groups()
        if key not in FIELDS:
            raise ValueError(f'Unknown Markdown configuration field: {key}')
        if key in values:
            raise ValueError(f'Duplicate Markdown configuration field: {key}')
        values[key] = value.strip()
    for key in FIELDS:
        if key not in values:
            raise ValueError(f'Missing Markdown field: {key}. Preserve the exact bullet and backtick format.')
        if not values[key] or values[key].upper() in {'REQUIRED', 'TODO', 'CHANGEME', 'PLACEHOLDER'}:
            raise ValueError(f'Manually complete the Markdown field: {key}')
    reviews = {}
    for mark, label in REVIEW_LINE.findall(text):
        if label not in REVIEWS or label in reviews:
            raise ValueError('The review checklist contains an unknown or duplicate item. Preserve the example wording.')
        reviews[label] = mark.lower() == 'x'
    if set(reviews) != set(REVIEWS) or not all(reviews.values()):
        raise ValueError('Complete all four review items in config/INSTALLATION.local.md after performing the checks yourself.')
    return values


def _absolute_path(record, key, directory=False):
    path = Path(record[key])
    if not path.is_absolute():
        raise ValueError(f'{key} must be an absolute path entered manually.')
    if not (path.is_dir() if directory else path.is_file()):
        raise ValueError(f'{key} does not point to an existing {"directory" if directory else "file"}.')
    return path.resolve()


def _same_path(left, right):
    return os.path.normcase(str(left.resolve())) == os.path.normcase(str(right.resolve()))


def _check_hash(path, entered, key):
    if not re.fullmatch(r'[0-9a-fA-F]{64}', entered):
        raise ValueError(f'{key} must contain a manually recorded 64-character SHA-256 hash.')
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != entered.lower():
        raise ValueError(f'{key} does not match the local file. Review the file before manually updating the record.')


def _integer(record, key, maximum):
    value = record[key]
    if not re.fullmatch(r'[0-9]+', value) or int(value) > maximum:
        raise ValueError(f'{key} must be an integer from 0 to {maximum}.')
    return int(value)


def read_configuration(root):
    root = Path(root).resolve()
    record = _read_markdown(root / 'config/INSTALLATION.local.md')
    if record['schema_version'] != '2':
        raise ValueError('schema_version must be 2 for the Markdown configuration format.')
    installation = _absolute_path(record, 'installation_root', directory=True)
    if not _same_path(installation, root):
        raise ValueError('installation_root does not match this installation. Manually review and update the record after moving the folder.')
    python = _absolute_path(record, 'python_executable')
    if not _same_path(python, Path(sys.executable)):
        raise ValueError('The active interpreter differs from python_executable. Start the application with Launch.cmd.')
    _check_hash(python, record['python_executable_sha256'], 'python_executable_sha256')
    actual_python = '.'.join(str(part) for part in sys.version_info[:3])
    if sys.version_info < (3, 11) or record['python_version'] != actual_python:
        raise ValueError('python_version must match the active interpreter exactly, and Python 3.11 or later is required.')
    output = _absolute_path(record, 'output_directory', directory=True)
    assets = (root / 'assets').resolve()
    if output == root or output == assets or assets in output.parents:
        raise ValueError('Choose a separate output directory outside the calibrated asset directory.')
    manifest_path = assets / 'manifest.json'
    _check_hash(manifest_path, record['asset_manifest_sha256'], 'asset_manifest_sha256')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    for package, key in [('Pillow', 'pillow_version'), ('numpy', 'numpy_version'), ('reportlab', 'reportlab_version')]:
        required = manifest.get('dependency_versions', {}).get(package)
        if not required or version(package) != required or record[key] != required:
            raise ValueError(f'{key} must match the installed and calibrated version exactly. Install the pinned requirements manually.')
    for color in ['green', 'red', 'blue']:
        info = manifest['colors'][color]
        _check_hash(assets / info['base'], record[f'{color}_base_sha256'], f'{color}_base_sha256')
        entered = [_integer(record, f'{color}_width', 100000), _integer(record, f'{color}_height', 100000)]
        if entered != info['size']:
            raise ValueError(f'The manually recorded {color} dimensions do not match the calibrated assets.')
    report_path = root / 'docs/pixel-validation.json'
    _check_hash(report_path, record['validation_report_sha256'], 'validation_report_sha256')
    validation = manifest.get('pixel_validation', {})
    report = json.loads(report_path.read_text(encoding='utf-8'))
    if not isinstance(validation, dict) or validation.get('status') != 'passed':
        raise ValueError('The supplied assets have not passed pixel comparison.')
    cases = _integer(record, 'reference_cases', 1000000)
    if cases != validation.get('reference_cases') or cases != report.get('case_count') or report.get('total_different_pixels') != 0:
        raise ValueError('The manually recorded validation result does not match the validation report.')
    if record['validation_report_sha256'].lower() != validation.get('report_sha256', '').lower():
        raise ValueError('The validation report is not the report associated with these calibrated assets.')
    return {
        'schema_version': 2,
        'python_executable': str(python),
        'output_directory': str(output),
        'initial_serials': {color: _integer(record, f'{color}_last_serial', 9999999999) for color in ['red', 'green', 'blue']},
    }
