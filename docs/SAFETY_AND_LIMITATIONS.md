# Safety and limitations

BBT creates a plan from a CT examination. It is not real-time localisation.

Every case should be checked for CT adequacy, segmentation leakage or incompleteness, disconnected components, endpoint placement, centreline continuity, route agreement with CT, branch orientation, virtual/endoscopic-view mismatch, distal-airway uncertainty and manual corrections.

Potential CT-to-body divergence includes respiratory phase, motion, patient positioning, sedation or anaesthesia-related atelectasis and airway deformation.

The segmentation is not ground truth merely because it is computer generated. If segmentation stops and CT does not confidently demonstrate continuation, the route should stop or the uncertainty should be explicitly documented.

Manual correction is acceptable only where supported by CT anatomy and should be recorded.

No claim of improved diagnostic yield, navigation success or procedural safety should be made without appropriate clinical validation.


## Interpolated navigation segments

The route-generation script can offer geometric bridging when the selected start and target lie in disconnected segmentation components. This is a computational navigation aid, not airway reconstruction. Each proposed bridge requires explicit user authorisation and is stored separately as `Airway_INTERPOLATED`; the source segmentation is not modified.

The current script permits an individual artificial bridge of up to 15 mm and up to 10 bridges. These are engineering limits, not clinically validated thresholds. Their presence must therefore remain visible in review and any derived route. A bridge must never be described or displayed as proof of a CT-visible bronchus. If the CT does not support continuation, the uncertainty remains unresolved even if a geometric route can be generated.

## Virtual bronchoscopy

Virtual bronchoscopy is generated from the pre-procedural CT-derived model and route. It must not be described as real-time localisation or as evidence of the bronchoscope's actual procedural position.
