# Pixel Validation

## Result

All **63 reference comparisons passed with zero different pixels**. This is an exact RGB pixel comparison, not a similarity score or a visual estimate.

| Coverage | Result |
| --- | --- |
| Native reference exports, 17 serials for each of three colors | 51 / 51 exact |
| Independently generated earlier green passes | 10 / 10 exact |
| Independently generated earlier red and blue passes | 2 / 2 exact |
| Total differing pixels | 0 |
| Text calibration captures | 2,658 |
| Numeric pair measurements | 300 |
| Runtime generation with external process creation blocked | Passed |

The text atlas covers every numeric layout state for eight-, nine-, and ten-digit serials, including overlapping adjacent `11` pairs. Repeated captures of the same state in different contexts were checked for consistency. QR samples preserve the reference image resampling response rather than applying a new image resize filter.

## Fixed output sizes

| Color | Cropped PNG dimensions |
| --- | --- |
| Green | 3017 x 2018 |
| Red | 3017 x 2019 |
| Blue | 3017 x 2019 |

The native reference canvas is 3600 x 2700. Cropping uses the exact recorded pass boundary for each color. The slight height difference between styles comes from the original template and is preserved.

## Scope

The zero-difference result applies to the supplied calibrated assets, recorded dimensions, matching serial and color, lossless PNG output, and the pinned dependency versions. It does not cover screenshots resized by a browser, another monitor's scaling, JPEG conversion, template changes, or a different Office export configuration.

The 63 comparisons are recorded in `pixel-validation.json`. A finite reference set is not a claim that every possible screenshot on every machine has been exhaustively tested. All supported text layout states are represented in the calibrated atlas and checked by the local tests.

Routine rendering does not require the original presentations, Office, WPS, COM, installed output fonts, or the offline calibration scripts. Those build-time tools and private reference presentations are not in the runtime package.
