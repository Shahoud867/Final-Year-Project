# Native-text Figma importer

The direct Figma editor remains blocked by the account's Starter-plan tool-call limit. This local importer was prepared and JavaScript syntax-checked; it **has not run or been visually verified in Figma**.

Open the original Granite file in Figma Desktop. Use Plugins → Development → Import plugin from manifest, select `manifest.json`, then run **Granite — Exhibition poster v3.0**. It creates the new poster beside earlier versions on the existing poster page. It retains the earlier versions and adds no page. It makes no network requests.

Install the supplied Inter and JetBrains Mono fonts first. It resolves actual available family/style names before making a frame, imports editable SVG artwork, and creates **67 native text nodes**. The existing university logo's image fill is reused. After running, check the complete composition, particularly text widths and line positions, before treating it as an approved Figma export. Undo the run if needed.

For a quick font-independent view, drag `granite_poster-figma-import_fyp1-final_v3.0.svg` into Figma. That version has outlined vector text, while the main SVG and PSD retain live text.
