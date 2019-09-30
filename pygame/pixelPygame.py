# Prerequisities: 
#     - Pygame needs to already been initialized
#     - Every row in pixelMatrix needs to have the same number of columns
#     - Every cell in pixelMatrix needs to be a RGB tuple
def drawPixelMatrix(surface, pixelMatrix):
    numberOfRows = len(pixelMatrix)
    numberOfColumns = len(pixelMatrix[0])

    maxPixelHeight = surface.get_height() // numberOfRows
    maxPixelWidth = surface.get_width() // numberOfColumns
    
    pxSideLen = min(maxPixelHeight, maxPixelWidth)
    
    for row in range(0, numberOfRows):
        for col in range(0, numberOfColumns):
            surface.fill(
                    pixelMatrix[row][col], 
                    (col*pxSideLen, row*pxSideLen, pxSideLen, pxSideLen)
            )
                    
    return surface
    