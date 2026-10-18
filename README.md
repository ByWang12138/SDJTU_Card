# Campus Pass Image Generator - Manual Setup Source Edition

Generate red, green, and blue campus pass PNG images without PowerPoint or WPS. This distribution intentionally requires the operator to prepare a local Markdown installation record before it can start.

## Source distribution and required private assets

This public repository contains source and blank configuration only. It does not contain institutional artwork, calibrated digit atlases, QR sampling assets, generated example images, or a completed local installation record. A fresh clone cannot generate passes.

Before following the manual setup guide, obtain an authorized, matching calibrated asset bundle separately. Place its `manifest.json` and all files listed in that manifest under `assets/`. Place its three reference PNGs under `examples/`. This source release does not include an asset builder or download assets automatically. Arbitrary replacement images will not reproduce the validated layout.

See [Private asset requirements](docs/PRIVATE_ASSETS.md). Keep those assets and generated files out of this public repository.

## Start here

Read [MANUAL_SETUP.md](MANUAL_SETUP.md) from beginning to end. Copy [config/INSTALLATION.example.md](config/INSTALLATION.example.md) to `config/INSTALLATION.local.md`, complete the 24 fields, and perform the four review items yourself.

There is no completed record in this package. It does not accept the previous `config/local.json`, automatically detect Python, install dependencies, generate configuration, or provide a setup wizard. A fresh download is expected to refuse startup until the operator finishes setup.

## Manual prerequisites

- Python 3.11 or later, with Tk support, installed by the operator.
- Exact versions from `requirements.txt`, installed into the selected interpreter manually.
- A permanent installation location and a separately created output directory.
- An inventory of interpreter path, version, executable hash, and installed library versions.
- Manually reviewed asset hashes, the validation report, and all three output dimensions.
- The last-used serial for each color, entered from the operator's own records.

All paths in the local Markdown record must be absolute. Moving the installation requires reviewing and updating the record. Run `Launch.cmd` only after completing the setup guide.

## Generation features

- Red, green, and blue styles.
- Matching `JT-` serials and `109-JT-` QR payloads.
- Sequential batches of 1 to 999 images.
- Eight-digit minimum padding and support for serials up to ten digits.
- Cropped PNG images and a ZIP containing only those images.
- An English desktop interface; no web server, HTTP generation API, or command-line generation switch.

The calibrated renderer, artwork, numeral pixels, spacing of adjacent `11` digits, QR sampling, and output sizes are unchanged. [Validation](docs/VALIDATION.md) records 63 exact native-reference comparisons with zero different pixels at the fixed reference resolution. Routine generation uses bitmap assets only and does not require Office, fonts, or an external rendering process.

## Manual-use preference and its limits

The author asks operators to complete installation, configuration, and final checks personally rather than delegating unattended setup to an AI tool. **These checks cannot prove human-only setup or reliably prevent AI assistance.** Public source code can be read and modified, and configuration can be understood by people or AI. The Markdown checklist is a declaration, not an AI detector or access-control mechanism.

## Distribution

This public source distribution excludes the owner's calibrated artwork, generated example images, and completed local records. Keep your private asset bundle and serial history local. No license has been added.

The completed `config/INSTALLATION.local.md` is private and ignored by Git. The configuration example contains no usable local paths, hashes, or serial defaults.

## Development checks

After manually installing the dependencies, renderer tests can be run with:

```powershell
python -B -m unittest discover -s tests -p "test_*.py"
```

These tests validate the renderer and use temporary output directories. They do not generate an installation record or configure the application.
