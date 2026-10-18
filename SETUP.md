# Installation and Configuration

## Public source prerequisite

The public repository excludes private artwork and example images. Obtain a matching authorized calibrated asset bundle and reference PNGs separately before Stage 1. Review [Private asset requirements](docs/PRIVATE_ASSETS.md). The repository does not build or download that bundle automatically. Without it, the application and renderer tests cannot complete successfully.

Application settings are stored in `config/INSTALLATION.local.md`. The following sections describe the runtime, assets, output location, and serial settings.

## Stage 1: Choose the permanent installation location

1. Extract the archive completely. Do not run the application from inside the ZIP viewer.
2. Move the `image-generator` directory to its permanent location.
3. Record its full absolute path. Do not move it after completing configuration; update the installation path in the record after moving the folder.
4. Create a separate directory for generated files. The program does not create this initial directory for you. Do not use the installation root or a directory inside `assets` as the output directory.

Installation paths and runtime values are specific to each environment. Update them when changing computers or installation locations.

## Stage 2: Install and inventory Python

Install Python 3.11 or later, including Tk support. Choose the interpreter you will actually use. A virtual environment can be used to keep the pinned dependencies separate from other projects.

Open PowerShell. Replace the example interpreter path below with your own real path before running a command. The example path is not a supplied installation.

```powershell
& 'C:\YOUR-PYTHON\python.exe' --version
```

Record the exact three-part version, such as `3.12.10`, using the actual result from your interpreter. Record the full interpreter path without surrounding quotation marks in the Markdown configuration.

Inspect its SHA-256:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'C:\YOUR-PYTHON\python.exe'
```

Copy only the complete `Hash` value into the record. Do not copy the column heading, command, or path into the hash field.

## Stage 3: Install and inventory the pinned libraries

In the installation directory, use the interpreter you selected above to install `requirements.txt`:

```powershell
& 'C:\YOUR-PYTHON\python.exe' -m pip install -r requirements.txt
```

Then inspect the installed libraries with the same interpreter:

```powershell
& 'C:\YOUR-PYTHON\python.exe' -m pip show Pillow
& 'C:\YOUR-PYTHON\python.exe' -m pip show numpy
& 'C:\YOUR-PYTHON\python.exe' -m pip show reportlab
```

Record each `Version` value. Compare all three results with `requirements.txt`. Using a different interpreter for installation and launch will fail validation. The installed versions must match the pinned requirements.

## Stage 4: Review the calibrated artwork

Open all three files in `examples`. Check the pass boundary, artwork, number position, QR position, and image dimensions.

Read `docs/VALIDATION.md`. Open `docs/pixel-validation.json` and `assets/manifest.json` in a text editor. Locate:

- The reference case count and the zero-difference result.
- The width and height for each color under `colors` in the manifest.
- The `base` path for each color.

The width and height fields in the local record must be transcribed from this asset set. They are checked against the manifest. Do not assume that all colors have the same height.

Calculate each required file hash individually from the installation directory:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\assets\manifest.json
Get-FileHash -Algorithm SHA256 -LiteralPath .\assets\green\base.png
Get-FileHash -Algorithm SHA256 -LiteralPath .\assets\red\base.png
Get-FileHash -Algorithm SHA256 -LiteralPath .\assets\blue\base.png
Get-FileHash -Algorithm SHA256 -LiteralPath .\docs\pixel-validation.json
```

Record the five hashes separately in their matching fields. The renderer also verifies every asset listed in the manifest. Do not replace images, resize the artwork, or edit the manifest to silence an error: doing so invalidates the recorded pixel comparison.

## Stage 5: Prepare the serial register

Enter the last serial already used for each color from the relevant serial register.

Generation begins at the next serial. For example, a last-used value of `100` starts the next batch at `JT-00000101` with QR payload `109-JT-00000101`.

Enter the last-used serial as digits only. Do not include `JT-`, a QR prefix, commas, quotation marks, or spaces. Accepted values range from 0 to 9999999999; an actual batch must still fit within that maximum.

## Stage 6: Configure the installation record

Using File Explorer, copy:

`config/INSTALLATION.example.md`

Rename the copy to:

`config/INSTALLATION.local.md`

The `.local.md` filename matters. Check that Windows did not append `.txt` or `.md.md`. Save the document as UTF-8 plain text using a text editor, not Word or a rich-text editor.

The application reads this Markdown record at startup. This release uses the Markdown format in place of `config/local.json`.

Each field must retain this exact syntax:

```text
- `field_name`: `your value`
```

Use straight ASCII backticks, a colon, and the original field names. Do not wrap the configuration document in a code fence. Do not duplicate or invent field names. Values cannot contain backticks or newlines. Windows backslashes are written literally; no JSON escaping is needed.

## Field reference

| Field | Setting |
| --- | --- |
| `schema_version` | Keep `2` for this Markdown format |
| `python_executable` | Full absolute path to the chosen interpreter |
| `python_executable_sha256` | SHA-256 of that executable, from Stage 2 |
| `python_version` | Exact active three-part Python version |
| `pillow_version` | Installed Pillow version, checked against the pinned requirement |
| `numpy_version` | Installed numpy version, checked against the pinned requirement |
| `reportlab_version` | Installed reportlab version, checked against the pinned requirement |
| `installation_root` | Absolute path to this extracted `image-generator` directory |
| `output_directory` | Absolute path to the separate directory created in Stage 1 |
| `asset_manifest_sha256` | SHA-256 of `assets/manifest.json` |
| `green_base_sha256` | SHA-256 of the green base image |
| `red_base_sha256` | SHA-256 of the red base image |
| `blue_base_sha256` | SHA-256 of the blue base image |
| `validation_report_sha256` | SHA-256 of `docs/pixel-validation.json` |
| `reference_cases` | Case count read from the validation report |
| `green_width`, `green_height` | Green dimensions read from the manifest and reviewed image |
| `red_width`, `red_height` | Red dimensions read from the manifest and reviewed image |
| `blue_width`, `blue_height` | Blue dimensions read from the manifest and reviewed image |
| `red_last_serial` | Last red serial already used |
| `green_last_serial` | Last green serial already used |
| `blue_last_serial` | Last blue serial already used |

Complete all 24 fields. No field may remain `REQUIRED`, blank, or a placeholder. After completing the work, change all four review checkboxes from `[ ]` to `[x]`. Preserve their wording.

## Stage 7: Launch and inspect the first output

Double-click `Launch.cmd`. The launcher first checks the Markdown interpreter path, executable hash, installation root, and schema. Python then checks the rest of the record. No GUI generation controls are available until validation succeeds.

If a setting fails validation, the error identifies the value to check. Correct the setting and launch the application again.

Select a color, inspect the current serial and next-serial preview, enter a small quantity, and generate. Open the PNG and check the number and QR content before creating a larger batch.

The output renderer is unchanged from the validated version. Configuration changes do not alter the calibrated image positions, font pixels, QR sampling, or fixed output dimensions.

## Maintenance

- Before closing the application, record the last serial used for each color. Update those three fields in your local Markdown record before the next session.
- After moving the folder, review and update the absolute installation path.
- After changing Python or its executable, review its path, version, executable hash, and installed libraries again.
- After a calibrated-asset update, obtain the corresponding validation report and review all asset hashes and dimensions again.
- Keep the completed record private. It contains local paths and serial history and is ignored by Git.
- Do not run multiple instances against the same serial history.

No license has been added.
