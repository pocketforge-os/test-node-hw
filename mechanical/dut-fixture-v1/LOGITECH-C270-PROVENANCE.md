# Logitech C270 HD webcam model provenance

The PocketForge webcam assembly is an original, repository-native OpenSCAD
reconstruction. No Logitech image, third-party mesh, STEP body, or printable
replacement shell is committed or embedded in the model.

## Installed identity and dimensional authority

- Product family: Logitech C270 HD Webcam, fixed-focus 720p camera with mono
  microphone, activity LED, attached USB-A cable, and articulated universal
  clip/base.
- Logitech's published overall envelope including the fixed clip is
  **72.91 × 31.91 × 66.64 mm**. The installed clip pose is articulated and
  therefore does not have to consume that complete depth.
- Logitech publishes a **55° diagonal field of view** for the current C270.
- The owner-fit fixture remains authoritative at **71.00 × 31.55 mm** for the
  installed face keep-out, with a **44.75 × 19.50 mm** minimum plate aperture.
  The rear housing that motivated that opening was measured at
  **37.00 × 14.69 mm** before clearance.
- The model keeps the body mechanically centred over that physical opening.
  The actual lens is left of the shell centre, so the chassis registers the
  model's lens—not the outer shell—to the DUT optical axis.

## Primary Logitech evidence

Retrieved 2026-07-25 from Logitech's public product/support hosts and preserved
outside Git under
`/home/matt/Downloads/pocketforge-reference/logitech/C270/`.
The files are reference-only and are not project artwork.

| Evidence | Primary URL | SHA-256 |
|---|---|---|
| Official gallery front/angle 1 | `https://resource.logitech.com/content/dam/products/logitech/webcams/c270-hd-webcam/gallery/c270-hd-webcam-1-0224.png` | `c86bc28778c52877a07cbd6ab03082dfe505215617180eb5064455f139a718ae` |
| Official gallery front view | `https://resource.logitech.com/content/dam/products/logitech/webcams/c270-hd-webcam/gallery/c270-hd-webcam-2-0224.png` | `9309527f3e090d9296deb0fb58df7b65e831daee4cd95e0a16fc29114e38944d` |
| Official gallery opposite angle | `https://resource.logitech.com/content/dam/products/logitech/webcams/c270-hd-webcam/gallery/c270-hd-webcam-3-0224.png` | `61d5f2d570b70e2db1ab9db3d9dc9bd0cc0bf20c8642b03bb0f985a2ee2c7` |
| Official gallery side/cable view | `https://resource.logitech.com/content/dam/products/logitech/webcams/c270-hd-webcam/gallery/c270-hd-webcam-4-0224.png` | `64d9391c0ab971159fafa31cc18c87583173dbb199cd5559214d0e1c8622a193` |
| Official quick-start guide | `https://www.logitech.com/assets/46735/hd-webcam-c270.pdf` | `ad802bc5705eceb6d75c2eb6ab4219e65e50c97678e1195910ac7b7566cd8d2b` |

The gallery establishes the asymmetric lens, recessed black bezel, 3 × 3
microphone perforations, lime activity indicator, `720p` and `logi` markings,
rear cable exit, twin pivots, arm, broad clip foot, and contact pad. The
quick-start guide independently identifies the microphone, lens, activity
light, and flexible clip/base.

## Online CAD candidates evaluated

1. **Fiction / VoronDesign C270 mount**, GPLv3, source commit
   `d5651692788228ce13bb57ea7327ec947543311c`:
   `https://github.com/VoronDesign/VoronUsers/tree/d5651692788228ce13bb57ea7327ec947543311c/printer_mods/Fiction/C270_mount`.
   Its `C270_assembly.step` hashes to
   `a69c4917c1f2964df2f6dc082827b46958a11e74ae3cda7a142e4d0bc9b4f3d8`.
   It models a modified C270 whose stock front is removed and whose original
   universal clip is absent. It was useful as a rear-shell/pivot shape
   cross-check but is not an exact stock assembly and is not redistributed.
2. **dbrogaard, “Logitech C270 & Wall mount”**, Cults design 2250684:
   `https://cults3d.com/en/3d-model/tool/logitech-c270-wall-mount`.
   The listing advertises a complete paid `logitech_c270.stp`, but no terms
   establish permission to republish its source geometry in this public
   repository. It was not purchased, downloaded, or imported.
3. Community searches also found many C270 mounts, privacy shutters, and
   replacement shells (including Pomaser's replacement cover), but no
   complete stock camera plus articulated clip with clear public-source
   redistribution terms.

## Reconstruction and uncertainty

- The physically fitted face, rear housing, and aperture dimensions control
  the installed interface. Logitech's overall dimensions are recorded rather
  than blindly scaling the installed assembly to a marketplace mesh.
- The compact clip pose is representative of the fixture installation: the
  camera body stays on the DUT side while the rear housing and arm pass
  through the existing opening and the foot parks on the operator side. Since
  the clip is articulated, its angle is presentation state rather than a
  manufacturing datum.
- Front feature positions were proportioned from the orthographic Logitech
  gallery view, then constrained to the owner-fit 71.00 × 31.55 mm face.
- The lens glass plane remains 15.00 mm toward the DUT from the fixture plane,
  preserving the accepted camera-distance/FOV contract. The negative
  orientation guard rejects a camera that looks away from the DUT.
- Source parameters remain readable in `logitech-c270.scad`; a future owner
  caliper pass can refine shell depth, pivot angle, or clip pose without
  importing opaque geometry.
