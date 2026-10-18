# Private Calibrated Assets

This repository publishes the application source only. No campus artwork, generated passes, completed local record, or calibration builder is distributed here.

## Required local layout

Supply an authorized matching bundle with this layout before following SETUP.md:

```text
assets/manifest.json
assets/green/base.png
assets/red/base.png
assets/blue/base.png
assets/<all other files listed in manifest.files>
examples/<three matching reference PNG images>
```

The bundle must include a schema version 2 manifest, pinned dependency versions, all digit sprites and prefix sprites for eight-, nine-, and ten-digit serials, and each color's QR sampling data. The renderer verifies every file listed in the manifest against its SHA-256.

The manifest must reference the matching zero-difference validation report in `docs/pixel-validation.json`. That report documents the owner's original calibrated bundle; it does not certify an arbitrary replacement bundle. If you recalibrate the artwork, supply and verify the corresponding report as well. This repository does not include the offline calibration workflow.

The Markdown configuration binds the selected local interpreter, installation path, output folder, asset checksums, dimensions, dependency versions, validation report, and last-used serials. Configure it as described in SETUP.md using the values for the local environment.

Private assets, examples, output, and completed records are excluded by .gitignore. Do not commit them to this public source repository. No license has been added.
