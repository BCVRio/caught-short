# Caught Short 🎄 Festive Edition — AR loo finder

WebAR wayfinding game (A-Frame + Zappar Universal AR). Point your phone, follow the floor arrow and dots to the nearest publicly usable toilet, earn Relief Points before the Bladder-o-meter runs dry. Works anywhere in the world: it searches live map data around your GPS position.

## Deploy (ZapWorks, Universal AR)
Create a Universal AR project, open the Experience tab and upload this **whole folder as a zip**: `index.html`, `aframe.min.js`, `zappar-aframe.js`, the `.wasm`, and `assets/`. They must travel together (the Zappar library loads its wasm from the same folder). ZapWorks gives you an HTTPS link and QR code. Any other HTTPS static host also works. The splash shows the build number (Festive Edition v5); if you see an older number after uploading, the old upload is cached: re-upload and hard-refresh.

## Festive Edition (branched from v23 of the main app, which is untouched)
- Santa-hat running mascot, cocoa-sipping relief mascot, snow-capped wordmark with holly, "Festive Edition" sub-title, snowy London night background (Higgsfield), festive icon.
- Sleigh-bell jingle on start (replaces the flush), bell shake when a new loo is targeted, festive quips in the rotation.
- Snowfall canvas over the splash and relief screens, dimmed and behind the HUD during AR so the camera view stays readable.
- Red "Need the loo?" button; everything else (routing, map, data sources, sounds) identical to the main app.

## Data sources (all live, no keys)
- OpenStreetMap via Overpass: public toilets plus venues tagged as having toilets (pubs, cafés, shops, libraries, stations…). Three mirrors raced in parallel (overpass.osm.ch dropped in v33: it only covers Switzerland).
- OpenStreetMap via Nominatim: toilets, pubs, cafés, libraries, supermarkets in the same 1.5 km box (pubs/cafés flagged "ask nicely").
Refuge Restrooms was dropped in v28 (too many joke and misplaced entries). Results are merged, de-duplicated within 35 m, and shown as each source lands. The central-London emergency list only appears within 30 km of Trafalgar Square if every source fails.

## v16: faster loading
- GPS warms up while the splash is showing, so a fix is usually ready at the tap.
- All three sources run at once (previously: four Overpass mirrors in series at 12 s each, then Nominatim), Overpass mirrors race with a 7 s cap, Nominatim trimmed to 5 queries at 1 s.
- Progressive: the list and arrow appear with the first source to answer; later sources merge in.
- Last result cached for 24 h within 600 m, shown instantly on relaunch while live data refreshes.
- Measured headless: first results 1.7 s cold, 0.8 s with cache; previously 20–60 s when mirrors were slow.

## Routing and AR
Walking routes from the OSRM foot router (`routing.openstreetmap.de`); arrow and dots aim along the route, HUD shows turn-by-turn. The floor rig sits in a Zappar Instant World Tracking anchor ~1.5 m ahead, re-anchoring as you walk. Dots run 3 m ahead (Festive v20). 2D compass fallback if AR can't start.

## v18: better floor tracking
- Placement is now gravity-aware. The Instant World Tracking anchor is gravity-aligned, so its up vector tells us which way is down in camera space; during placement the rig is dropped 1.3 m below the phone and 1.6 m horizontally ahead *regardless of phone tilt* (previously a fixed camera-relative offset, so tilting the phone moved the "floor").
- Floor-drift re-seating: if the locked anchor drifts to less than 0.6 m or more than 2.3 m below the phone, or slides behind you / beyond 3.2 m, it re-places on the floor ahead. Conditions must persist 0.7 s so single bad frames don't make it jump.
- Compass yaw smoothing slowed (260 ms) so the arrow stops twitching with compass noise.
- Tune: `PHONE_HEIGHT` (1.3) and `AHEAD` (1.6) in `update()`.

## v20: lower rig + route overview map
- Rig placed 1.5 m below the phone and 2.0 m ahead (was 1.3 / 1.6) so the arrow sits lower in frame and reads more naturally while walking. `PHONE_HEIGHT` / `AHEAD` in `update()`.
- Route overview sheet (opened from the mini map since v35; previously a 🗺️ top-bar button): MapLibre GL + OpenFreeMap vector tiles (v21; loaded on first open from cdnjs; OpenFreeMap is keyless, unlimited and explicitly fine for production, so no provider change is needed at scale), the walking route drawn as a mint line, your position (blue dot), the target loo (🚽 pin), other nearby loos as pink dots (tap for name/distance), total distance and rough walking time, and the full turn list. Refreshes every 3 s while open; 📍 recentres on you. Before the route arrives it shows a dashed straight line.

## v22
- Route overview sheet restyled to the app palette (ink gradient, mint subtitle, pink rules, dark popups and zoom control).
- "Nice try" message now reports the real straight-line distance with units (was always "1.0m" beyond a kilometre).

## v23
- 2D fallback no longer crashes when the AR libraries fail to load (THREE guard).

## Splash layout fix (v24 / Festive v2)
- Splash now flows from the top with safe-area padding and scrolls if needed, and hero art scales with viewport height, so the mascot no longer hides under the browser address bar on short screens (checked at iPhone SE / iPhone 15 Safari and Android sizes).

## Audio v2 (v25 / Festive v3)
- Title jingles: two Suno V6 takes per edition (made through FlashBoards, original lyrics and style brief), trimmed to 11 s with a fade and mastered to -14 LUFS. One of the two plays at random on the first tap of the title card (browsers need a gesture before audio) or on Start. Main: "Caught short! Cross your legs and hold the fort!"; Festive: "Ho ho hold it".
- SFX regenerated with Higgsfield (Mirelo) at higher quality and mastered to matched loudness: three farts, toot, raspberry, flush, plop, fanfare, fail sting, Code Yellow alarm; festive adds sleigh bell and a festive fanfare. UI tap stays synthesised (the model rendered it silent). Total embedded audio ~0.7 MB.

## v26 / Festive v4
- Sound playback now queues until the clip has decoded (jingles decode first), instead of silently falling back to the synthesised sounds when a play was requested before decoding finished. Decoding also starts at page load where the browser allows it.

## Festive v5: festive UI palette
- Night purples replaced with deep pine greens (HUD glass, list sheet, map sheet, 2D compass), pink with Christmas red, yellow with gold, mint with holly mint; secondary buttons holly green; bladder meter holly → gold → red; turn pill red. Splash/relief backgrounds keep the purple-night artwork so the snow and lights still read.

## v27 / Festive v6: arrow redesign + UI polish
- New wayfinding arrow in both modes. AR floor arrow: rounded silhouette with a heavy ink outline (readable on busy real floors), gold-to-amber shaft and pink head gradients (festive: red/green palette via CSS vars), soft ground shadow, glossy highlights and a travelling pulse band; turns mint within two arrive-radii. 2D compass: the arrow now sits in a compass dial with a tick ring, cardinal marks, gradient fills and a drop shadow, with the mascot below it.
- Typography: Nunito for UI, Baloo 2 for display (headings, distance, score); loaded from Google Fonts with the previous system stack as fallback.
- Buttons get a 3D press (inset highlight + coloured base shadow), pills/cards get glass gradients, the distance readout is gradient text, chips and rows animate on tap, sheets and toasts have deeper shadows.

## v28 / Festive v7
- Refuge Restrooms removed as a source; the loo cache key changed so old Refuge entries vanish on first load.
- Title jingles now play in full (13.9–15.6 s, mastered to -14 LUFS with their natural ending) instead of an 11 s cut with a fade. The audio context also auto-resumes if the camera start or a phone interruption suspends it.
- UI sound set (Higgsfield Mirelo, normalised and trimmed, ~115 KB): bubble-pop tap on every button, xylophone key on filter chips, blip on picking a loo, whoosh open/close on the loo sheet and map, map-unfold ding on the route overview, boing on Next loo, sparkle-chime on Start / Try it now / Find another, plink on unmute. Keys `ui_*` in `CS_SFX`; `SFX.ui(name)` plays one.

## Festive v8: full Christmas retheme
- New Higgsfield splash/relief background: snowy Christmas Eve London in deep green, red and gold (no purple left), Santa-hat Big Ben, lit tree, red bus.
- Palette pushed to true Christmas colours: deep pine `--ink`, Christmas red `--pop`, gold `--sun`/`--gold`; gold hairlines on pills, cards and the compass dial; candy-cane bladder meter and loo-sheet stripe; red/green chips and rows; green secondary buttons.
- Snow is roughly 2.5× denser with larger flakes, a drifting side wind, one in eight drawn as ❄, and stays 85% visible over the AR/HUD view (was 55%).

## v29 / Festive v9
- Fix: v27/v28 (Festive v6–v8) threw `ReferenceError: ribbonTexture` when the AR scene built, so Start did nothing. The dotted-route texture builder was lost in the arrow redesign and is restored (glowing gold dots, tiled and scrolled toward the loo).

## v30 / Festive v10
- Title jingles re-rendered in Suno V6 with a 30 s budget and an explicit hard-stop ending (the earlier short renders had a baked-in fade). Main: two ~27 s takes; Festive: a 9 s stinger and a 28 s take. Mastered to -14 LUFS, lead/tail silence trimmed, no fade applied anywhere.

## v31 / Festive v11
- Jingles shortened to ~10–12 s: each 27 s take is cut on a bar downbeat near 10 s and spliced straight onto its own final brass hit and ring-out (8 ms crossfade), so they still end on a real button rather than a fade. Festive take 1 was already a 9 s stinger.

## Festive v12
- Festive take 2 re-edited: cut moved a bar later (10.81 s) so no vocal crosses the splice; 13.8 s total.

## Festive v13
- Santa ho-ho-ho's while navigating: five Higgsfield (Mirelo) laugh variants, first one 20–40 s after Start, then one every 60–90 s at random (never the same one twice running, slight pitch variation, short haptic buzz). Only while the HUD is up, not after arrival, not when the tab is hidden; respects mute. `scheduleHoHo()` / `SFX.hoho()`.

## Festive v14
- The walking cue is now two sung Suno jingles of "Ho ho ho! Hurry, the loo's not far now!" (deep Santa bass voice, sleigh bells, brass; 19.6 s and 9.6 s), alternating, replacing the laugh variants. Same 60–90 s timing.

## v32 / Festive v15: optimisation pass
- Embedded art re-encoded (PNG → WebP q85, backgrounds to 810×1440 progressive JPEG): index.html 2.9 MB → 1.1 MB (festive 4.0 → 1.7 MB). Jingles kept at the original stereo 96 kbps; short SFX mono 48 kbps. Visually identical at display size. The unused festiveSub art entry was dropped (the "Festive Edition" line is text).
- A-Frame and the Zappar library now load with `defer` and the `<a-scene>` is injected from a `<template>` once they're ready, so the splash paints before 1.7 MB of JS instead of after it. CDN fallback moved into `ensureLibs()`.
- Google Fonts loaded non-blocking (preload → stylesheet); unused Baloo 2 700 weight dropped. Favicon now a 64 px PNG (`assets/icon-64.png`).
- AR arrow: static layers (shadow, outline, gradients) rendered once per colour mode and reused each frame; only the pulse band and highlights redraw (measured 2.7 ms → 0.4 ms per frame, pixel-identical).
- Turn-by-turn: each manoeuvre's route index is precomputed when the route arrives instead of rescanning the whole polyline every frame.
- HUD text nodes only written when the value changes; loo list rows only rebuilt while the sheet is open; queued sound plays now expire correctly after 6 s.
- Festive: snow canvas capped at 2× DPR (same look, ~40% less fill).
- Backups of the previous builds: `index.v31.bak.html` / `index.v14.bak.html` (not included in the zip).

## v33 / Festive v16: back-end review fixes
- Fixed: after any data refresh (the refresh button, the automatic reload after walking >600 m, or the 45 s Overpass retry) the HUD kept a stale target object, so distance/bearing froze and GPS auto-arrive never fired. The target is now re-pointed at the fresh object and distance/bearing are computed live each frame.
- "No loos here" is now distinguished from "servers unreachable": an answered-but-empty search ends cleanly ("No loos within 1.5 km") instead of the 20 s retry loop with a wrong message.
- Cache no longer re-seeds the live result (stale entries expire after 24 h as intended); cached Overpass entries are kept only when Overpass itself fails this round.
- Nominatim: stops when a newer search supersedes it (no overlapping loops → no 403s), no wasted trailing wait, bails after two network failures; venues tagged `toilets=no` dropped, `toilets:fee`/`toilets:wheelchair` honoured, `access=customers` flagged, kind taken from the OSM tag (pubs returned by the café query are labelled pubs).
- Android compass: relative `deviceorientation` events are ignored once an absolute reading exists (was alternating between two headings every frame).
- Dedup: by OSM id first, then by proximity only for same-name or toilet/toilet pairs (was dropping e.g. two cafés 20 m apart).
- OSRM: a failed route request is retried after 30 s; re-route threshold scales with GPS accuracy so standing still indoors no longer re-routes every 20 s; map subtitle says "no walking route here" when routing failed.
- MapLibre load has a 12 s timeout; remaining Refuge Restrooms dead code removed.

## v34 / Festive v17
- Sound now plays with the iPhone ring switch on silent: on the first tap the app requests the `playback` audio session (iOS 17+) and keeps a silent looping `<audio>` element alive, which moves Web Audio out of the "ringer" category. Re-asserted when the app returns from the background.

## v35 / Festive v18: mini map
- The 🗺️ top-bar button is gone. A live circular mini map sits bottom-left of the HUD: heading-up (rotates with the compass, smoothed), centred on you with a position dot and facing cone, the walking route drawn from your current point, the target 🚽, auto-zoom by distance (17.2 → 14.6 as the loo gets further). Tapping it opens the full Route overview. Loads MapLibre 2.5 s after the HUD appears so loo data gets the network first; fades in when ready. `initMini()` / `drawMini()`; the circle is `#miniWrap`.

## v36 / Festive v19
- The quip line above the distance now fades out 4.5 s after it changes and reappears only for a new message (5 s on first load); the compass warning appears only after a 6 s grace period while no heading is available and hides as soon as one arrives.
- Tapping the 🫃 Bladder-o-meter or the ⭐ score opens a "How the game works" sheet: meter, Relief Points formula, streak, arrow/mini map, what "ask" means, and the coming-soon venue discounts.

## Festive v20
- Title music is now the single 9 s "Ho ho hold it" stinger (jingle1); the edited second take was removed because the splice clipped "Follow the arrow".

## Tuning
`SEARCH_RADIUS` (1500 m), `ARRIVE_RADIUS` (22 m), `anchorPoseOffset` (arrow placement), dot strip height (3 m) in the `.dots` plane, quips arrays for copy.

## Assets
`assets/` holds the loose artwork (Higgsfield-generated wordmarks, mascots, splash background) and the app icon for ZapWorks and store listings; the same artwork is embedded in `index.html` as base64.
