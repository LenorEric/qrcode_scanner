# -*- coding: utf-8 -*-

from .PatternFinding import PatternFinding
from .FindingOrientationOfContours import FindingOrientationOfContours
from .AffineTransformation import AffineTransformation, PerspectiveTransformation

import cv2 as cv


class ImageHandler(object):
    # @profile_line
    def __init__(self, img):
        self.image_raw = img
        self.grayscale_image = cv.cvtColor(self.image_raw, cv.COLOR_BGR2GRAY)
        self.contour_image = cv.Canny(self.grayscale_image, 100, 200)
        self.transform_image = None

    def qr_code_in_image(self):
        patternFindingObj = PatternFinding(
            cv.findContours(self.contour_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE),
            self.image_raw
        )
        patterns = patternFindingObj.FindingQRPatterns(3)
        if len(patterns) != 3:
            # print('patterns unable to find')
            return None
        contourA = patterns[0]
        contourB = patterns[1]
        contourC = patterns[2]
        orientationObj = FindingOrientationOfContours()
        massQuad, ORIENTATION = orientationObj.FindOrientation(contourA, contourB, contourC)

        # affine transformation
        # tl = massQuad.tl
        # tr = massQuad.tr
        # bl = massQuad.bl
        # affineTransformObj = AffineTransformation(self.grayscale_image, ORIENTATION)
        # self.transform_image = affineTransformObj.transform(tl, tr, bl)

        # perspective transformation
        psp_trans_obj = PerspectiveTransformation(self.grayscale_image, ORIENTATION)
        self.transform_image = psp_trans_obj.transform(massQuad)

        self.transform_image = \
            cv.adaptiveThreshold(self.transform_image, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                 cv.THRESH_BINARY, 75, 0)
        return self.transform_image


if __name__ == '__main__':
    pass
