import slicer

segNodes = slicer.util.getNodesByClass("vtkMRMLSegmentationNode")

print("Segmentation nodes found:", len(segNodes))

for segNode in segNodes:

    print("")
    print("Segmentation:", segNode.GetName())

    segmentation = segNode.GetSegmentation()

    print("Segments:", segmentation.GetNumberOfSegments())

    # Generate 3D closed surfaces
    segNode.CreateClosedSurfaceRepresentation()

    displayNode = segNode.GetDisplayNode()

    if displayNode:
        displayNode.SetVisibility(True)
        displayNode.SetVisibility2D(True)
        displayNode.SetVisibility3D(True)

        for i in range(segmentation.GetNumberOfSegments()):
            segmentID = segmentation.GetNthSegmentID(i)

            displayNode.SetSegmentVisibility(
                segmentID,
                True
            )

            displayNode.SetSegmentVisibility3D(
                segmentID,
                True
            )

            print(
                "  Visible:",
                segmentation.GetSegment(segmentID).GetName()
            )

# Reset all 3D cameras
lm = slicer.app.layoutManager()

for i in range(lm.threeDViewCount):
    view = lm.threeDWidget(i).threeDView()
    view.resetFocalPoint()
    view.resetCamera()

slicer.app.processEvents()

print("")
print("3D surfaces generated and displayed.")
