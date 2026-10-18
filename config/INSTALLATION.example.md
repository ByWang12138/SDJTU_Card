# Local Installation Record

Copy this file to INSTALLATION.local.md. Replace every REQUIRED value with the corresponding local setting.
Keep the field names, bullet syntax, backticks, and review wording unchanged.
Do not place this record inside a code fence. Do not publish the completed file.

## 1. Runtime Inventory

- `schema_version`: `2`
- `python_executable`: `REQUIRED`
- `python_executable_sha256`: `REQUIRED`
- `python_version`: `REQUIRED`
- `pillow_version`: `REQUIRED`
- `numpy_version`: `REQUIRED`
- `reportlab_version`: `REQUIRED`

## 2. Local Folders

- `installation_root`: `REQUIRED`
- `output_directory`: `REQUIRED`

## 3. Calibrated Asset Audit

- `asset_manifest_sha256`: `REQUIRED`
- `green_base_sha256`: `REQUIRED`
- `red_base_sha256`: `REQUIRED`
- `blue_base_sha256`: `REQUIRED`
- `validation_report_sha256`: `REQUIRED`
- `reference_cases`: `REQUIRED`

## 4. Output Dimension Register

- `green_width`: `REQUIRED`
- `green_height`: `REQUIRED`
- `red_width`: `REQUIRED`
- `red_height`: `REQUIRED`
- `blue_width`: `REQUIRED`
- `blue_height`: `REQUIRED`

## 5. Last-Used Serial Register

- `red_last_serial`: `REQUIRED`
- `green_last_serial`: `REQUIRED`
- `blue_last_serial`: `REQUIRED`

## 6. Installation Checks

Mark each item [x] when the corresponding installation check is complete.

- [ ] The runtime paths and dependency versions match this installation.
- [ ] The example images match the recorded output dimensions.
- [ ] The QR payload format and last-used serials have been checked.
- [ ] The output directory and asset checksums match the local files.
