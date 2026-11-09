# Educore — redesigned website

Static site, no framework. Open `site/index.html` in a browser, or serve it:

    python3 -m http.server 5181 --directory site

## Structure
- `site/` — the deployable website (20 HTML pages + `assets/`)
- `site/assets/css/style.css` — design system (brand tokens at the top: navy #0B2240, cyan #00C0FE, purple #B43BEF, blue #007AFF, Poppins)
- `site/assets/js/main.js` — animations & interactions (vanilla JS, respects reduced-motion)
- `build.py` — generates every page from one shared header/footer. Edit content there, then run `python3 build.py`.

## Before going live
- Forms (Contact, Get a Quote, Setup School) are front-end only: they validate and show a confirmation but send nothing.
  Point each `<form>` `action` at your backend or form service and remove `data-demo`.
- Legal pages (`build.py` → `legal()`) read the original Terms/Privacy text from `../.edu-src/*.json`; the generated HTML already contains it.

## Hero video clips
`site/assets/video/` holds five classroom clips from Pexels (free licence, commercial use allowed, no attribution required):
pexels.com/video/8342238, 7999596, 8342240, 5200348, 5897650. To use your own footage, replace the `.mp4` (and matching `.jpg` poster)
files with the same names, or change the `clips` list in `build.py` → `home()`. Keep each clip short (5–15 s) and under ~3 MB.
