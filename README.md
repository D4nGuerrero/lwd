# Laredo Web Designs mockup reconstruction

Responsive, static website reconstructed from the three supplied JPEGs. Open `index.html` through a local server, for example:

```powershell
python -m http.server 9137
```

Then visit `http://127.0.0.1:9137/`.

## Project structure

- `index.html` — semantic page sections, navigation, cards, dialogs, and form.
- `styles.css` — entry point for the modular styles in `css/`.
- `css/base.css` — shared typography, page frame, navigation, and buttons.
- `css/sections.css` — hero, services, work, process, testimonials, CTA, footer, and dialogs.
- `css/responsive.css` — mobile layouts and reduced motion handling.
- `script.js` — menu, testimonial carousel, project details, and contact form.
- `assets/` — extracted imagery used as separate assets.
- `tools/extract_assets.py` — repeatable asset extraction from the supplied mockup files.
- `tools/build_pages.py` — copies only public site files into `docs/` and checks relative paths.
- `docs/` — ready-to-publish GitHub Pages output, including `.nojekyll`.
- `.gitignore` — excludes the attached reference files, preview image, and local tooling clutter. It intentionally keeps `docs/` trackable.
- `.gitattributes` — normalizes source line endings and treats artwork as binary.

## Publish as a GitHub Pages project site

1. After any site edit, run `python tools/build_pages.py` and commit the updated `docs/` folder.
2. Push this project to [D4nGuerrero/lwd](https://github.com/D4nGuerrero/lwd), which is configured as the `origin` remote.
3. In that repository, open **Settings → Pages**. Under **Build and deployment**, choose **Deploy from a branch**, select the branch containing this project, and choose **`/docs`** as the folder. Save.
4. The project site URL is expected to be `https://d4nguerrero.github.io/lwd/`. This site uses relative asset paths, so it works under that repository path without a hard-coded base URL.

The `docs/` folder deliberately omits the reference attachments, development scripts, README, and temporary preview images. GitHub Pages serves static files; the quote form continues to open the visitor's email app because there is no backend.

## Asset provenance

`laredo-bridge.jpg` and `underwater-catfish.jpg` are the separate original illustrations supplied with the mockup. The LWD mark, three portfolio previews, the river texture, and shoreline details were extracted from the page mockup. The small service and process icons were recreated as SVG markup because they were not provided as independent assets. The handwritten callout and decorative browser frame are CSS and live text. The portfolio previews are cropped screenshots of the depicted client sites, so their original lettering remains part of those preview images; page headings, descriptions, buttons, and links are live HTML.

## Interactions and launch details

Navigation links scroll to their sections. Portfolio cards open detail dialogs. The testimonial arrows cycle through reviews. The quote form validates required fields and prepares an email in the visitor's mail app.

Before publishing, verify the inferred `CONTACT_EMAIL` in `script.js` and replace the generic social network destinations with the business's actual accounts. The mockup did not provide these destinations. Footer Privacy and Terms labels currently lead to the contact section until approved policy pages are supplied.

The desktop composition was compared in the browser at the mockup's 720 × 1280 viewport. A 390 px mobile viewport was also reviewed, including its menu and dialogs.
