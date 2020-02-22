# Offline-Signature-Verification-Feature-Extraction
Python code for feature extraction from a signature image in order to perform signature verification

I have coded a fetaure extractor in Python for the purpose of offline verification of signature images.
I split the image into 64 cells recursively before extracting the features
Following are the features I have extracted:

* Number of black to white transitions for each of the 64 cells
* Aspect ratio for each cell
* Centroid of the image and of each cell
* Number of black cells in image
* Angle of each cell from its bottom left corner to the image centroid
* Normalized sixe for each cell (cell size divided by number of black cells)
* Normalized angle of each cell from centroid (sum of angles divided by number of black cells)

Finally, I dump all of these values into their respective text files.

Essentially, these features enable one to distinguish between genuine signatures and those that are not authentic.

Note: This is not a machine learning code, it's merely a feature extractor
