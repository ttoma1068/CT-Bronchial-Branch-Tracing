# BBT Slicer Skill

## Purpose

This skill guides reproduction and iterative development of a low-cost,
CT-based virtual bronchoscopy and bronchial branch-tracing (BBT)
workflow in 3D Slicer. It is intended for pre-procedural planning and
technical prototyping, not real-time bronchoscope localisation.

The workflow uses the patient's CT as the sole anatomical source of
truth. It combines 3D Slicer modules, TotalSegmentator airway
segmentation, clinician-defined landmarks, centreline extraction, and
Python-controlled virtual camera behaviour.

## Core safety rule: CT is the anatomical source of truth

Never invent distal airways.

Never silently bridge a segmentation gap.

Never imply that a bronchus exists if it cannot be demonstrated on the
source CT.

Never alter airway diameter, branch orientation, bifurcation position,
branch length, or geometry simply to create a convenient route.

Any interpolation or clinician-created correction must be stored
separately, visibly distinguished from CT-supported segmentation, and
recorded in the audit trail.

Every displayed airway or centreline segment must be traceable either to
the source CT or to a documented clinician correction.

Virtual bronchoscopy is a CT-derived pre-procedural representation.
Never describe it as real-time localisation or registration of the
bronchoscope to the patient.

## Current reference environment

The workflow has been developed principally in:

-   3D Slicer 5.12 on macOS.
-   Python 3.12 within Slicer.
-   TotalSegmentator for automated airway segmentation.
-   Markups for clinician-selected points and bifurcations.
-   Extract Centerline / centreline tools where functional.
-   Python for virtual camera control, bronchoscopic roll, bifurcation
    pauses, clock display, screenshots, and video export.

SlicerVMTK has previously shown compatibility problems in this
environment. Do not make the workflow dependent on VMTK unless the
installation has first been verified.

## Reproduction workflow

The working sequence is:

**Chest CT → clinician Markups → TotalSegmentator → airway
review/correction → centreline route → bifurcation Markups → Python
virtual bronchoscopy → BBT outputs**

### 1. Import the CT

Load the original chest CT DICOM examination into 3D Slicer.

Prefer the source CT rather than an AI-enhanced or resampled volume for
defining anatomy.

For the prototype dataset, a sharp reconstruction such as Br60 has
provided good airway edge visibility. A smoother reconstruction may be
reviewed as an adjunct, but resampling or enhancement must not be
treated as creation or recovery of anatomical information.

Review axial, coronal and sagittal images before segmentation.

### 2. Define clinician landmarks

Use Slicer Markups to identify the clinically relevant points directly
on the CT.

At minimum define:

-   tracheal starting point;
-   lesion/target;
-   final airway endpoint.

The final airway endpoint should be placed in the most distal
CT-supported segmented bronchus considered appropriate for the route. It
does not have to coincide with the lesion.

If the lesion lies beyond the last reliably visible airway, terminate
the route at the last demonstrable airway and preserve the remaining
target-to-airway distance as uncertainty.

Do not create a fictitious distal airway to reach the lesion.

### 3. Segment the airway tree

Use TotalSegmentator as the current preferred automated starting point.

The relevant airway segment may be named `lung_airways`, depending on
the TotalSegmentator task/version.

Treat the segmentation as an AI-generated candidate segmentation, not
ground truth.

Always compare it against the original CT, particularly along the
intended route and in distal bronchi.

Do not assume that a visually smooth 3D model is anatomically complete.

### 4. Review and manually correct segmentation

Inspect the proposed airway tree in synchronized multiplanar CT views
and 3D.

Manual correction is permitted when supported by the CT.

Document:

-   branches added or removed;
-   segmentation gaps;
-   uncertain distal lumina;
-   clinician-created corrections;
-   any interpolated connection;
-   unresolved uncertainty.

If a disconnected segment must be joined for experimental route
construction, keep the bridge in a separate segment such as
`Airway_INTERPOLATED` or `BBT_ManualCorrection`. Display it in a visibly
different colour and record that it is not CT-demonstrated anatomy.

### 5. Generate the route centreline

Generate a route from the tracheal start point through the segmented
airway toward the selected final airway.

The current working route may be stored as a Slicer Markups Curve, for
example:

`Centerline curve (0)`

Important Slicer 5.12 API detail:

`GetCurvePointsWorld()` takes no output argument and returns
`vtkPoints`.

Correct pattern:

``` python
curvePointsVTK = routeNode.GetCurvePointsWorld()
```

Do not use the older pattern that passes a `vtkPoints` object as an
argument.

A single centreline curve represents the selected route. It does not
contain enough information by itself to prove the geometry or identity
of sibling daughter branches.

Do not infer a complete bifurcation topology solely from a single
selected route.

### 6. Mark bifurcations

Create a Markups Fiducial node named:

`BBT_Bifurcations`

Place one point at each true CT-supported bifurcation along the selected
route.

The Python navigation script should project these points onto the route
and order them from trachea to target.

These clinician-confirmed points are used for:

-   automatic pauses;
-   bifurcation screenshots;
-   branch sequence numbering;
-   bronchoscope-style camera steering;
-   procedural route-card generation.

### 7. Virtual bronchoscopy camera model

The virtual camera travels along the selected centreline.

Use a minimal-twist or parallel-transported baseline camera frame to
prevent arbitrary image rotation caused merely by centreline curvature.

Then apply deliberate virtual bronchoscope roll when approaching a
marked bifurcation.

The reference clock is patient/trachea fixed:

-   12 o'clock = anterior;
-   3 o'clock = patient right;
-   6 o'clock = posterior;
-   9 o'clock = patient left.

The blue clock arrow represents the simulated bronchoscope/camera
orientation.

The fixed clock itself must not rotate.

The airway image should rotate according to the camera roll. Remember
that rotating the virtual camera produces the opposite apparent rotation
of the scene.

The simplified steering concept is:

**roll → deflect → advance**

This approximates how a flexible bronchoscope is oriented toward a
branch, but it is not a biomechanical model of the physical
bronchoscope.

CT cannot determine actual shaft torsion, operator hand rotation, scope
looping, airway-wall contact, or real procedural camera orientation.

Therefore label the displayed roll as simulated virtual steering.

### 8. Bifurcation behaviour

The preferred navigation behaviour is:

**PLAY → approach bifurcation → camera rolls toward selected route →
automatic pause before bifurcation → clinician inspects view → PLAY →
continue**

The current prototype uses approximately:

-   pause 5 mm before the marked bifurcation;
-   start deliberate roll about 10 mm before bifurcation;
-   sample the parent direction before the bifurcation;
-   sample the selected daughter route after the bifurcation;
-   lock camera roll between bifurcations.

These distances are engineering parameters and must not be presented as
validated clinical values.

### 9. Camera implementation

Use the same roll value for both:

1.  the blue clock arrow; and
2.  the complete virtual camera orientation.

Do not solve a camera-direction problem merely by reversing the HUD
arrow.

A robust implementation should:

1.  calculate camera position on the centreline;
2.  calculate the actual focal point/look-ahead direction;
3.  maintain a transported zero-roll `ViewUp` frame;
4.  apply deliberate roll around the actual viewing direction;
5.  orthogonalize `ViewUp` to the viewing direction;
6.  call `camera.SetViewUp(...)`;
7.  update the fixed clock HUD with the same simulated bronchoscope
    roll.

If the rendered image rotates in the wrong direction while the blue
arrow is correct, reverse only the sign/convention used for the camera
`ViewUp` roll. Do not change the anatomical branch calculation or fixed
clock.

### 10. Required navigation outputs

The prototype should be capable of producing:

-   synchronized multiplanar CT views;
-   3D airway segmentation;
-   selected route centreline;
-   virtual bronchoscopy fly-through;
-   fixed clock reference;
-   simulated bronchoscope orientation arrow;
-   numbered bifurcation sequence;
-   bifurcation screenshots;
-   manual branch-tracing table;
-   compact procedural route card;
-   confidence/uncertainty warnings;
-   audit record of manual corrections;
-   image, video, PDF and structured-data exports.

### 11. MP4 export

Video export should use the same camera function used for interactive
navigation.

Do not create a separate camera model solely for export.

Recommended sequence:

**trachea → route navigation → roll before bifurcation → short
bifurcation pause → continue → target**

Capture the actual Slicer 3D render, including the clock HUD, as
sequential PNG frames.

Use `ffmpeg` to encode the PNG sequence as H.264 MP4 when available.

Common macOS ffmpeg locations include:

-   `/opt/homebrew/bin/ffmpeg`
-   `/usr/local/bin/ffmpeg`

If ffmpeg is unavailable, preserve the PNG sequence rather than treating
the export as failed.

The exported video must remain labelled as CT-derived pre-procedural
virtual bronchoscopy.

## Known technical findings

### Classical threshold segmentation

Global connected thresholding of low-HU voxels has repeatedly leaked
from the bronchial lumen into lung parenchyma.

Do not assume that a connected low-density component represents the
airway tree.

Thresholding may remain useful locally or as part of a hybrid workflow
but is not currently the preferred whole-tree segmentation method.

### Hessian/objectness and vessel-style approaches

Experimental Hessian, objectness, vesselness and vessel-oriented
segmentation approaches have not provided sufficiently reliable airway
segmentation in the current workflow.

Do not represent them as established solutions.

### TotalSegmentator

TotalSegmentator has produced the best automated airway segmentation
observed in the project so far and is therefore the current preferred
starting point.

Its distal-airway performance still requires clinician review.

Segmentation quality remains the principal technical limitation of the
workflow.

### Distal airways

The source CT resolution determines what anatomy can reasonably be
demonstrated.

For CT with approximately 1.5 mm slice spacing, very small distal
bronchi may not be reliably represented.

Upsampling does not create missing anatomical information.

Do not generate probabilistic distal airway extensions as if they were
patient anatomy.

## Manual corrections and interpolation

Clinician corrections are permitted when directly supported by the CT.

Interpolation is fundamentally different from correction.

If an experimental bridge is explicitly requested between disconnected
segments:

-   preserve the original segmentation;
-   create the bridge as a separate segment;
-   label it clearly as interpolated/manual;
-   use a different display colour;
-   record its endpoints and dimensions;
-   keep it visible in the audit trail;
-   never describe it as a demonstrated bronchus.

## Uncertainty

Uncertainty must remain visible.

Examples include:

-   incomplete distal segmentation;
-   segmentation discontinuity;
-   ambiguous bronchial lumen;
-   target beyond visible airway;
-   manually corrected branch;
-   interpolated segment;
-   uncertain branch orientation;
-   mismatch between virtual and expected endoscopic appearance;
-   CT-to-body divergence.

Never hide uncertainty simply to make the route look cleaner.

## Clinical limitations

Pre-procedural CT does not reproduce procedural anatomy perfectly.

Explicitly consider:

-   inspiratory CT versus procedural lung volume;
-   respiratory motion;
-   anaesthesia/sedation-related atelectasis;
-   airway deformation;
-   patient positioning;
-   CT-to-body divergence;
-   secretion or bleeding obscuring endoscopic landmarks;
-   incomplete distal segmentation;
-   map-to-endoscopic-view mismatch.

The application is a planning and branch-tracing aid, not a substitute
for bronchoscopic judgement.

## Code-generation rules

When helping a user modify or debug the Slicer workflow:

1.  Provide a complete replacement Python script whenever a script is
    revised. Do not provide isolated patch blocks unless the user
    explicitly requests them.
2.  Clearly separate explanation from executable code.
3.  Label executable sections prominently, for example:
    `COPY INTO SLICER`.
4.  Do not put traceback text, commentary, Markdown instructions, or
    explanatory prose inside executable code.
5.  Assume Slicer 5.12 APIs unless the user specifies another version.
6.  Prefer standard Slicer, VTK, NumPy and PythonQt functionality.
7.  Avoid dependencies that are not known to be installed.
8.  Do not rely on OpenCV (`cv2`) unless installation has been verified.
9.  Do not rely on SlicerVMTK until compatibility has been verified.
10. Preserve existing clinician-defined Markups unless explicitly asked
    to replace them.
11. Never change anatomy merely to make code succeed.
12. On failure, stop with a clear error rather than silently fabricating
    a route.

## Useful node naming conventions

Where possible use stable, descriptive node names such as:

-   `RouteStart`
-   `RouteTarget`
-   `target`
-   `trachea`
-   `BBT_Bifurcations`
-   `Centerline curve (0)`
-   `Airway_INTERPOLATED`
-   `BBT_ManualCorrection`

Before running code, verify that the expected nodes actually exist
rather than silently creating anatomically meaningful points.

## Automation boundary

Most of the workflow can ultimately be automated in Python.

Clinician input should remain mandatory for anatomically or clinically
consequential decisions, particularly:

-   lesion identification;
-   tracheal start confirmation;
-   final airway endpoint confirmation;
-   segmentation correction;
-   bifurcation confirmation when topology is uncertain;
-   acceptance of the final route;
-   acknowledgement of unresolved uncertainty.

Automation should reduce repetitive Slicer interaction, not remove
clinician oversight.

## Development philosophy

3D Slicer is used as an open, scriptable medical-imaging platform rather
than merely as a collection of GUI modules.

Python can orchestrate:

-   node creation;
-   segmentation;
-   route extraction;
-   camera movement;
-   visualization;
-   screenshots;
-   bifurcation sequencing;
-   branch-tracing tables;
-   video generation;
-   structured exports.

Generative AI can assist with iterative Python development, allowing
clinicians to rapidly prototype different visualization and interaction
behaviours.

However, AI-generated code is an engineering aid. It does not validate
anatomical correctness.

Every clinically relevant output must be checked against the source CT.

## Current workflow summary

The reproducible prototype is:

1.  Import chest CT into 3D Slicer.
2.  Review source CT.
3.  Mark lesion.
4.  Mark tracheal starting point.
5.  Run TotalSegmentator airway segmentation.
6.  Review segmentation against CT.
7.  Correct CT-supported segmentation errors manually where required.
8.  Select the most distal reliable airway endpoint nearest the target.
9.  Generate/extract the selected centreline route.
10. Verify every part of the route against CT-supported airway anatomy.
11. Place `BBT_Bifurcations` markers at relevant true bifurcations.
12. Run the BBT Python navigation script.
13. Navigate from trachea toward the target airway.
14. Apply simulated bronchoscope roll before marked bifurcations.
15. Pause and capture each bifurcation.
16. Generate the branch-tracing sequence.
17. Export screenshots and MP4.
18. Record manual corrections, interpolation and unresolved uncertainty.
19. Retain the source CT as the definitive anatomical reference.

## Current development priority

The main technical priority is improved segmentation of smaller
CT-visible airways without increasing false-positive branches or
inventing anatomy.

The next priority is to derive branch-choice information from the actual
CT-supported segmented bifurcation topology rather than from a single
route curve alone.

Until sibling branch topology is explicitly analysed, the software may
display the selected route and simulated steering direction but must not
claim that it has independently identified the complete daughter-branch
anatomy.

## Intended status

This workflow is an experimental prototype for technical development,
pre-procedural planning and research.

Any clinical claims must remain within the scope of completed
validation.

Do not describe diagnostic yield improvement, navigation accuracy,
real-time localisation, procedural superiority, or patient benefit
unless these outcomes have been demonstrated in an appropriately
designed study.
