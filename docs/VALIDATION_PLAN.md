# MoonSight validation plan

This document distinguishes checks that should be performed from results that have actually been verified. Do not report a check as passed until a team member has run it and recorded the result.

## 1. Application checks

- [ ] Install dependencies from `requirements.txt` in a clean Python environment.
- [ ] Start the app with `streamlit run app.py`.
- [ ] Confirm all tabs render without errors.
- [ ] Confirm each study-region selection maps to the intended NASA archive identifier.
- [ ] Confirm invalid selections and network failures produce understandable messages.

## 2. NASA LOLA data checks

For at least one study region, test each available product:

- [ ] Elevation (`surf`)
- [ ] Slope (`slp`)
- [ ] Elevation uncertainty (`toterr`)
- [ ] Slope uncertainty (`slperr`)
- [ ] LOLA return count (`ldec`)

For every successful download:

- [ ] Record the exact source URL and retrieval date.
- [ ] Confirm the raster opens and has valid pixels.
- [ ] Confirm the displayed axes are projected X/Y coordinates in metres.
- [ ] Confirm the displayed statistics are calculated from the downsampled preview.
- [ ] Confirm the CSV export matches the displayed preview grid.

## 3. JPL Horizons checks

- [ ] Test a published NASA study-region center.
- [ ] Test a second region and a different date.
- [ ] Confirm both Sun and Earth requests return data.
- [ ] Check that timestamps are interpreted as UT.
- [ ] Check azimuth and elevation units and the geometric horizon reference.
- [ ] Record API errors or unavailable results rather than inventing values.

## 4. Scientific review

- [ ] Verify study-region identifiers and coordinates against the cited NASA sources.
- [ ] Verify data-product descriptions and units against NASA documentation.
- [ ] Keep uncertainty and LOLA return-count context visible when interpreting terrain.
- [ ] Do not call an archive-tile average a landing-ellipse result.
- [ ] Do not claim terrain-aware visibility until an obstruction model is implemented and validated.
- [ ] Do not label any region as safe or optimal based only on the current prototype.

## 5. Demo readiness

- [ ] Run the application on the intended presentation device and network.
- [ ] Capture genuine screenshots from the tested application.
- [ ] Record a short walkthrough using values returned by the live data sources.
- [ ] Explain the scientific limitations clearly.
- [ ] Verify the repository and deployment links before submission.

## Test record

Add dated entries here as checks are completed. Include the tester, environment, outcome, and any issue found.
