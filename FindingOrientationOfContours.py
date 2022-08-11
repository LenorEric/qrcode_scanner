# -*- coding: utf-8 -*-


import cv2 as cv
import numpy as np
from scipy.spatial.distance import pdist

ORIENTATION = None
NorthWest = 0
SouthEast = 1
SouthWest = 2
NorthEast = 3


class Quad(object):
    def __init__(self, top_left_point=None, top_right_point=None, bottom_right_point=None, bottom_left_point=None,
                 contour_a=None, contour_b=None, contour_c=None):
        self.tl = top_left_point
        self.tr = top_right_point
        self.br = bottom_right_point
        self.bl = bottom_left_point
        self.TopContour = contour_a
        self.RightContour = contour_b
        self.BottomContour = contour_c


class FindingOrientationOfContours(object):
    global ORIENTATION

    def FindOrientation(self, contourA, contourB, contourC):
        """Here famous Triangle Method is used to determine the Orientation
        of the three contours and identify which one is top, left and
        right contour.Here we find the distance between the centres of
        mass of these three contours and which ever is longest , base
        of # TO-DO: he triangle formed by three contours and then we find the
        position of remaining contour using this base line to know
        the orientation"""

        # calculating the centre of mass of three contours
        MomentA = cv.moments(contourA)
        MomentB = cv.moments(contourB)
        MomentC = cv.moments(contourC)

        # finding the centre of mass of three contours
        centreOfMassA_X = int(MomentA['m10'] / MomentA['m00'])
        centreOfMassA_Y = int(MomentA['m01'] / MomentA['m00'])
        point_a = np.float32([centreOfMassA_X, centreOfMassA_Y])
        pairA = Pair(point_a, contourA)

        centreOfMassB_X = int(MomentB['m10'] / MomentB['m00'])
        centreOfMassB_Y = int(MomentB['m01'] / MomentB['m00'])
        point_b = np.float32([centreOfMassB_X, centreOfMassB_Y])
        pairB = Pair(point_b, contourB)

        centreOfMassC_X = int(MomentC['m10'] / MomentC['m00'])
        centreOfMassC_Y = int(MomentC['m01'] / MomentC['m00'])
        point_c = np.float32([centreOfMassC_X, centreOfMassC_Y])
        pairC = Pair(point_c, contourC)

        # finding the distance of the distance between points
        distance_AB = pdist((point_a, point_b))
        distance_BC = pdist((point_b, point_c))
        distance_AC = pdist((point_a, point_c))

        largestLine = np.argmax(
            np.array([distance_AB, distance_BC, distance_AC]))

        if largestLine == 0:
            # largest line is between points A and B
            return (self.findOrientationBetweenPoints(pairC, pairA, pairB))

        if largestLine == 1:
            # LargestLine is Between B and C
            return (self.findOrientationBetweenPoints(pairA, pairB, pairC))

        if largestLine == 2:
            # LargestLine is between A and C
            return self.findOrientationBetweenPoints(pairB, pairA, pairC)

    def findOrientationBetweenPoints(self, DistancePair, PairA, PairB):
        slope, distance = self.CalculatePerpendicularDistance(DistancePair.point, PairA.point, PairB.point)
        massQuad = Quad()
        massQuad.tl = DistancePair.point
        massQuad.TopContour = DistancePair.contour
        # print("Slope:{},Distance:{}".format(slope, distance))
        if (slope >= 0) and (distance >= 0):
            # if slope and distance are positive A is bottom while B is right
            if PairA.point[0] > PairB.point[0]:
                massQuad.bl = PairA.point
                massQuad.tr = PairB.point
            else:
                massQuad.bl = PairB.point
                massQuad.tr = PairA.point
            # TopContour in the SouthWest of the picture
            orientation_2p = "SouthWest"
        elif (slope >= 0) and (distance <= 0):
            # if slope is positive and distance is negative then B is bottom
            # while A is right
            if PairA.point[1] > PairB.point[1]:
                massQuad.tr = PairA.point
                massQuad.bl = PairB.point
            else:
                massQuad.tr = PairB.point
                massQuad.bl = PairA.point
            orientation_2p = "NorthEast"
        elif (slope <= 0) and (distance >= 0):
            if PairA.point[0] > PairB.point[0]:
                massQuad.bl = PairA.point
                massQuad.tr = PairB.point
            else:
                massQuad.bl = PairB.point
                massQuad.tr = PairA.point
            orientation_2p = "SouthEast"
        elif (slope <= 0) and (distance <= 0):
            if PairA.point[0] > PairB.point[0]:
                massQuad.tr = PairA.point
                massQuad.bl = PairB.point
            else:
                massQuad.tr = PairB.point
                massQuad.bl = PairA.point
            orientation_2p = "NorthWest"
        else:
            return None

        # To determine the position of contours
        if (massQuad.tr == PairA.point).all():
            massQuad.RightContour = PairA.contour
            massQuad.BottomContour = PairB.contour
        else:
            massQuad.RightContour = PairB.contour
            massQuad.BottomContour = PairA.contour
        return massQuad, orientation_2p

    def CalculatePerpendicularDistance(self, DistancePoint, PointA, PointB):
        coeffA, coeffB, constant = self.__findCoefficientsOftheLine(PointA, PointB)
        slope = self.__findSlope(PointA, PointB)
        return (slope, (coeffA * DistancePoint[0] + coeffB * DistancePoint[1] + constant) / (
            np.sqrt(coeffA ** 2 + coeffB ** 2)))

    def __findCoefficientsOftheLine(self, pointA, pointB):
        slope = self.__findSlope(pointA, pointB)
        coefficientA = -slope
        coefficientB = 1
        constant = slope * pointA[0] - pointA[1]

        return (coefficientA, coefficientB, constant)

    def __findSlope(self, pointA, pointB):
        return (pointB[1] - pointA[1]) / (pointB[0] - pointA[0] + 1e-5)


class Pair(object):
    def __init__(self, messPoint, contour):
        self.point = messPoint
        self.contour = contour
