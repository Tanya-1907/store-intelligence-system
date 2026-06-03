import cv2
import numpy as np

ZONES = {

    "LEFT_SHELF": np.array([
        [0, 150],
        [250, 150],
        [250, 700],
        [0, 700]
    ]),

    "CENTER_AREA": np.array([
        [250, 150],
        [700, 150],
        [700, 700],
        [250, 700]
    ]),

    "RIGHT_SHELF": np.array([
        [700, 150],
        [1100, 150],
        [1100, 700],
        [700, 700]
    ]),

    "BILLING": np.array([
        [450, 350],
        [700, 350],
        [700, 550],
        [450, 550]
    ])
}


def get_zone(cx, cy):

    for zone_name, polygon in ZONES.items():

        result = cv2.pointPolygonTest(
            polygon,
            (cx, cy),
            False
        )

        if result >= 0:
            return zone_name

    return None