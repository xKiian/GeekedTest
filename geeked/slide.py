#https://github.com/glizzykingdreko/Datadome-GeeTest-Captcha-Solver/blob/main/solver.py
"""
MIT LICENSE

Big thanks to glizzykingdreko for making amazing solver

i modified it a bit
"""
import numpy as np
from PIL import Image
import io, requests, cv2


class GeeTestIdentifier:
    def __init__(self, background, puzzle_piece):
        self.background = self._read_image(background)
        self.puzzle_piece = self._read_image(puzzle_piece)

    @staticmethod
    def test():
        identifier = GeeTestIdentifier(
            background=GeeTestIdentifier.load_image("https://static.geetest.com/captcha_v4/e70fbf1d77/slide/0af8d91d43/2022-04-21T09/bg/552119bd2af448b9a3af1ce95b887b90.png"),
            puzzle_piece=GeeTestIdentifier.load_image("https://static.geetest.com/captcha_v4/e70fbf1d77/slide/0af8d91d43/2022-04-21T09/slice/552119bd2af448b9a3af1ce95b887b90.png"),
        )
        result = identifier.find_puzzle_piece_position()
        print(f"Result: {result}")

    @staticmethod
    def load_image(url: str) -> np.ndarray:
        response = requests.get(url)
        return response.content

    @staticmethod
    def _read_image(image_source):
        """
        Read an image from a file or a requests response object.
        """
        if isinstance(image_source, bytes):
            return cv2.imdecode(np.frombuffer(image_source, np.uint8), cv2.IMREAD_ANYCOLOR)
        elif hasattr(image_source, 'read'):  # Checks if it's a file-like object
            return cv2.imdecode(np.frombuffer(image_source.read(), np.uint8), cv2.IMREAD_ANYCOLOR)
        else:
            raise TypeError("Invalid image source type. Must be bytes or a file-like object.")

    def find_puzzle_piece_position(self):
        """
        Find the matching position of a puzzle piece in a background image.
        """
        # Apply edge detection
        edge_puzzle_piece = cv2.Canny(self.puzzle_piece, 100, 200)
        edge_background = cv2.Canny(self.background, 100, 200)

        edge_puzzle_piece_rgb = cv2.cvtColor(edge_puzzle_piece, cv2.COLOR_GRAY2RGB)
        edge_background_rgb = cv2.cvtColor(edge_background, cv2.COLOR_GRAY2RGB)

        res = cv2.matchTemplate(edge_background_rgb, edge_puzzle_piece_rgb, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        h, w = edge_puzzle_piece.shape[:2]

        center_x = top_left[0] + w // 2
        return center_x  - 41 # -41 because we don't want the center but the start of the piece

    @staticmethod
    def get_puzzle_piece_box(img_bytes: bytes):
        """
        Identify the bounding box of the non-transparent part of an image.
        """
        image = Image.open(io.BytesIO(img_bytes))
        bbox = image.getbbox()
        cropped_image = image.crop(bbox)
        return cropped_image, bbox[0], bbox[1]


if __name__ == '__main__':
    GeeTestIdentifier.test()