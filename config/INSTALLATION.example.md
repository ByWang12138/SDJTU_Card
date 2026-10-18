# Local Installation Record

Copy this file to INSTALLATION.local.md. Complete every REQUIRED value yourself.
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

## 6. Operator Review

Mark each item [x] only after completing the corresponding review yourself.

- [ ] I reviewed MANUAL_SETUP.md from beginning to end.
- [ ] I opened all three example images and checked their dimensions.
- [ ] I checked the QR payload rule and the last serial for each color.
- [ ] I understand that these checks cannot prove human-only setup.
