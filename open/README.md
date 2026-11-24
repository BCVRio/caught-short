# Caught Short – Festive Edition · Open build (no Zappar)

Same app as the Festive Edition, with the Zappar SDK removed. Two AR paths, chosen automatically at Start:

1. **WebXR floor tracking** (Android Chrome and other browsers with `immersive-ar`): true 6DoF anchoring via the browser's own ARCore session, `local-floor` reference space (y = 0 is the real floor), HUD shown through `dom-overlay`. The rig locks to a spot ~2 m ahead and re-seats when you walk past it or more than 3.8 m away. Splash shows "WebXR floor tracking ready ✓" when this is available.
2. **Camera mode** (iPhone Safari and anything without WebXR AR): the rear camera feed as a background, with the A-Frame view driven by the phone's orientation (tilt from the gyro, yaw from the true-north compass). The rig glides ~2 m ahead on an assumed flat floor and the arrow points along the real bearing. No floor lock, but stable and works everywhere. Splash shows "Camera AR mode".

If neither the camera nor WebXR is available the 2D compass dial is used, as before.

Everything else (loo search, OSRM routing, mini map, sounds, Relief Points, snow) is unchanged from Festive v20.

## Deploy
Static files only, any HTTPS host: `index.html`, `aframe.min.js`, `assets/`. Upload the folder to Cloudflare Pages, Netlify, GitHub Pages, Vercel, or a subfolder on an existing site (e.g. bcvr.io/loo). HTTPS is required for the camera, geolocation and WebXR. No build step, no keys, no server. Data comes live from OpenStreetMap (Overpass + Nominatim), routing from OSRM, map tiles from OpenFreeMap; all keyless.

Nominatim's usage policy asks for an identifying Referer or User-Agent; a normal site origin satisfies that. If traffic grows, point `OVERPASS` and the Nominatim URL at your own instances.

## Test checklist (real devices)
- Android Chrome: tap Start → Chrome's AR prompt → camera passthrough with the arrow stuck to the pavement. Walk 5 m: the rig should stay put, then re-seat ahead. If the AR session fails or is dismissed, it should fall back to camera mode automatically.
- iPhone Safari: tap Start → camera permission → compass permission → live camera with the arrow floating ahead; turning the phone turns the world, the arrow keeps pointing along the route.
- Both: title jingle on first tap, GPS fix, loo list, mini map, Sweet Relief.

## Differences from the Zappar build to be aware of
- WebXR AR takes over the whole screen (immersive session); the browser's back gesture ends it, which drops the app to camera mode rather than the splash.
- Camera mode has no floor tracking: the arrow is anchored to your heading, not to the ground.
- No ZapWorks QR/short link or analytics; use your own QR (the promo's QR generator in the pack) and your own hosting.
