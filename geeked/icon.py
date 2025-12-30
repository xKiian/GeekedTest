import random
from typing import Any, Dict, List, Optional, Union

import cv2
import numpy as np
import requests


class IconSolver:
    # Mapping of icon filenames to directions
    ICON_MAPPING = {
        '8da090c135ff029f3b5e19f4c44f73c8.png': 'u',
        'cb0eaa639b2117a69a81af3d8c1496a1.png': 'd',
        '315ce8665e781dabcd1eb09d3e604803.png': 'l',
        '38bd9dda695098c7dfad74c921923a7d.png': 'lu',
        '502e51dbabf411beba2dcd55fd38ebbd.png': 'ld',
        '2b2387f566f6a03ed594d4d7cfda471f.png': 'r',
        '78dc29045d587ad054c7353732df53c5.png': 'ru',
        '23ef93e6b0e0df0e15b66667c99a5fb4.png': 'rd'
    }

    def __init__(self, imgs: str, ques: List[str]):
        self.imgs = self.load_image(f'https://static.geetest.com/{imgs}')
        self.ques = ques

    @staticmethod
    def test() -> None:
        """Test method for the IconSolver class."""
        identifier = IconSolver(
            imgs="captcha_v4/policy/87d2c0d959/icon/163935/2025-04-20T17/3f99716d17324c9ba3eec402121eb1d9.jpg",
            ques=[
                "nerualpic/original_icon_pic/icon_20201215/315ce8665e781dabcd1eb09d3e604803.png",
                "nerualpic/original_icon_pic/icon_20201215/38bd9dda695098c7dfad74c921923a7d.png",
                "nerualpic/original_icon_pic/icon_20201215/cb0eaa639b2117a69a81af3d8c1496a1.png"
            ]
        )
        result = identifier.find_icon_position()
        print(f"Result: {result}")

    @staticmethod
    def load_image(url: str) -> bytes:
        """Load image from URL and return as bytes."""
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes
        return response.content

    def _get_directions(self) -> List[Dict[str, Any]]:
        """Extract directions from question icons using the predefined mapping."""
        return [{'direction': self.ICON_MAPPING.get(q.split('/')[-1], '')} for q in self.ques]

    def _process_bbox(self, bbox: List[int], im: np.ndarray) -> Optional[Dict[str, Union[str, List[float]]]]:
        """Process a single bounding box and return direction and coordinates if matched."""
        from .dddd_server import dddd_service
        x1, y1, x2, y2 = bbox
        img = im[y1:y2, x1:x2]
        _, img_bytes = cv2.imencode(".png", img)
        res = dddd_service.classification(img_bytes.tobytes())
        res = res.split('_')[1]
        return res if res in self.ICON_MAPPING.values() else None

    def find_icon_position(self) -> List[List[float]]:
        """
        Find icon positions based on the question directions.
        Returns a list of coordinates for each required direction.
        """
        from .dddd_server import dddd_service
        bboxes = dddd_service.detection(self.imgs)
        im = cv2.imdecode(np.frombuffer(self.imgs, dtype=np.uint8), cv2.IMREAD_COLOR)

        box_directions = self._get_directions()
        unused_boxes = []
        results = []

        for bbox in bboxes:
            processed = self._process_bbox(bbox, im)
            if not processed:
                continue

            x1, y1, x2, y2 = bbox
            center = [(x1 + (x2 - x1) / 2) * 33, (y1 + (y2 - y1) / 2) * 49]

            # Try to match with required directions
            matched = False
            for boxd in box_directions:
                if boxd['direction'] == processed and 'bbox' not in boxd:
                    boxd['bbox'] = center
                    matched = True
                    break

            if not matched:
                unused_boxes.append(center)

        # Prepare results, using unused boxes if needed
        for boxd in box_directions:
            if 'bbox' in boxd:
                results.append(boxd['bbox'])
            elif unused_boxes:
                results.append(unused_boxes.pop(random.randint(0, len(unused_boxes) - 1)))

        return results


if __name__ == '__main__':
    IconSolver.test()
