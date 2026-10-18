# Campus Pass Image Generator

Generate red, green, and blue campus pass PNG images without PowerPoint or WPS.

## Source distribution

This repository contains application source and a blank configuration record. Institutional artwork, calibrated digit atlases, QR sampling assets, reference PNGs, and completed local settings are supplied separately.

Place a matching authorized asset bundle under `assets/` and its three reference PNGs under `examples/`. Also restore the original `docs/pixel-validation.json` from that bundle with its exact bytes. The public JSON report is an informational copy; line endings or an added final newline can change its SHA-256. The runtime checks the original report against the bundle manifest.

See [Asset requirements](docs/PRIVATE_ASSETS.md) for the local directory layout. A fresh clone needs these files and environment settings before generation is available.

## Getting started

See [Installation and configuration](SETUP.md). Application settings are stored in `config/INSTALLATION.local.md`; copy [the example record](config/INSTALLATION.example.md) and enter the settings for the local installation.

## Requirements

- Python 3.11 or later with Tk support.
- The dependency versions listed in `requirements.txt`.
- A matching calibrated asset bundle and validation report.
- An existing output directory and the last-used serial for each color.

The record includes runtime paths, dependency versions, file checksums, output dimensions, and serial settings. Paths must be absolute. Update environment-specific values when moving the installation or changing Python.

## Features

- Red, green, and blue styles.
- Matching `JT-` serials and `109-JT-` QR payloads.
- Sequential batches of 1 to 999 images, with eight-digit minimum padding and support for up to ten digits.
- Cropped PNG images and a ZIP archive.
- An English desktop interface launched with `Launch.cmd`.

The renderer uses calibrated bitmap assets to preserve the reference image layout. [Validation](docs/VALIDATION.md) records 63 native-reference comparisons with zero different pixels for the supplied asset set. See the validation document for the supported resolution and comparison scope.

## Development checks

With dependencies and the matching local asset bundle available:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
```

## Local files

Completed configuration, private assets, and generated output are excluded by `.gitignore`. Keep local paths and serial history out of public commits. No license has been added.
