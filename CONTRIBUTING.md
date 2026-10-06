# Contributing

Contributions are welcome, particularly independent reproduction, reproducible bug reports, segmentation failure cases, route-extraction improvements, camera/bifurcation improvements, usability work and validation methods.

## Anatomical fidelity

The CT remains the anatomical source of truth. Contributions must not silently invent distal bronchi, bridge unsegmented gaps, alter branch geometry for convenience, label uncertain anatomy as certain, or present predicted anatomy as observed anatomy.

If interpolation, prediction or clinician correction is introduced, it must be visibly distinguishable and auditable.

## Pull requests

Please state:
1. the BBT version from which the work was derived;
2. the clinical or technical problem;
3. the change made;
4. new dependencies;
5. how it was tested;
6. known failure modes;
7. whether anatomical interpretation is affected;
8. confirmation that no identifiable patient information is included.

Do not claim improved diagnostic yield, navigation accuracy, safety or clinical effectiveness without an appropriately designed study.

Accepted contributors should be added to `CONTRIBUTORS.md`.
