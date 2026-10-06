# CT-based Bronchial Branch Tracing (BBT)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23190857.svg)](https://doi.org/10.5281/zenodo.23190857)

**Research prototype for CT-derived virtual bronchoscopy and bronchial branch tracing**

Version 1.0.0 | Initial public repository package | 2026

## Purpose

BBT is an open research workflow for converting a chest CT into a clinician-reviewed airway model, a CT-supported route towards a peripheral target, and a virtual bronchoscopic sequence for bronchial branch tracing.

It is intended for **research, education and pre-procedural planning**. It does **not** provide real-time bronchoscope localisation, electromagnetic navigation, robotic guidance or autonomous navigation.

## Anatomical rule

**The CT is the source of anatomical truth.**

The workflow must not invent distal airways, silently bridge segmentation gaps, alter airway geometry to create a convenient route, or imply that a non-visible bronchus exists. Every accepted branch and route decision should remain traceable to the source CT or to a documented clinician correction supported by the CT.

## Workflow

1. Import a thin-section chest CT into 3D Slicer.
2. Select the appropriate CT reconstruction.
3. Mark the lesion as `Lesion`.
4. Segment the airways using SlicerTotalSegmentator.
5. Review the segmentation on axial, coronal and sagittal CT.
6. Correct it manually only where CT anatomy supports the correction.
7. Place `RouteStart` in the trachea.
8. Place `RouteTarget` in the most distal CT-supported connected airway selected for approach.
9. Generate and inspect the 3D airway model.
10. Generate the centreline route.
11. Verify the complete route against the source CT.
12. Generate CT-derived virtual bronchoscopy.
13. Review successive bifurcations and create the branch-tracing sequence.
14. Save outputs, versions, corrections and unresolved uncertainty.

`Lesion` and `RouteTarget` are deliberately separate. The lesion is the clinical target; `RouteTarget` is the endpoint of the airway route demonstrable from the CT.

## Scripts expected

- `scripts/01_BBT_CT_Series_Selector_v1_0.py`
- `scripts/02_BBT_Make_3D_Visible.py`
- `scripts/03_BBT_Continuous_Smooth_Route_v4_0.py`
- `scripts/04_BBT_Virtual_Bronch_v7_0.py`

The route script can create clinician-authorised geometric bridges across disconnected segmentation components. Every such bridge is stored separately as `Airway_INTERPOLATED` and is **not CT-derived anatomy**. A route that crosses an interpolated segment must be treated as containing explicit uncertainty and checked against the source CT. Interpolation must never be interpreted as evidence that a bronchus exists.

## Reproduction

See the reproduction and safety documentation under `docs/`. The source CT remains authoritative at every review step.

## Citation

The archived v1.0.0 release has the persistent DOI **10.5281/zenodo.23190857**.

Toma T. *CT-based Bronchial Branch Tracing (BBT): CT-derived virtual bronchoscopy and bronchial branch tracing workflow*. Version 1.0.0. 2026. Zenodo. https://doi.org/10.5281/zenodo.23190857

If you use, reproduce or adapt BBT in research, teaching, software development or publication, please cite the specific version used. See `CITATION.cff` and `CITATION.md`.

Modified versions should identify their changes and must not imply validation or endorsement by the original author.

## Contributions

Independent reproduction, documented failure cases, bug reports, validation work and technical improvements are encouraged. See `CONTRIBUTING.md`.

## Patient data

Do not commit identifiable DICOM examinations, screenshots containing identifiers, clinical documents or protected health information.

## Status

**Research prototype. Not a medical-device release. Not validated for independent clinical navigation.**
