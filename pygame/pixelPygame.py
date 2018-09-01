def drawPixelMatrix(surface, pixelMatrix):
    numberOfRows = len(pixelMatrix)
    numberOfColumns = len(pixelMatrix[0])

    maxPixelHeight = surface.get_height() // numberOfRows
    maxPixelWidth = surface.get_width() // numberOfColumns
    
    pxSideLen = min(maxPixelHeight, maxPixelWidth)
    
    for row in xrange(0, numberOfRows):
        for col in xrange(0, numberOfColumns):
            surface.fill(
                    pixelMatrix[row][col], 
                    (col*pxSideLen, row*pxSideLen, pxSideLen, pxSideLen)
            )
                    
    return surface
    