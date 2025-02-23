#https://github.com/glizzykingdreko/Datadome-GeeTest-Captcha-Solver/blob/main/solver.py
"""
MIT LICENSE

Big thanks to glizzykingdreko for making amazing solver

i modified it a bit
"""
import numpy as np
import requests, cv2


class SlideSolver:
    def __init__(self, puzzle_piece, background):
        self.background = self._read_image(background)
        self.puzzle_piece = self._read_image(puzzle_piece)

    @staticmethod
    def test():
        identifier = SlideSolver(
            background=SlideSolver.load_image("https://static.geetest.com/captcha_v4/e70fbf1d77/slide/0af8d91d43/2022-04-21T09/bg/552119bd2af448b9a3af1ce95b887b90.png"),
            puzzle_piece=SlideSolver.load_image("https://static.geetest.com/captcha_v4/e70fbf1d77/slide/0af8d91d43/2022-04-21T09/slice/552119bd2af448b9a3af1ce95b887b90.png"),
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
        center_y = top_left[1] + h // 2
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(self.background, top_left, bottom_right, (0, 0, 255), 2)
        cv2.line(self.background, (center_x, 0), (center_x, edge_background_rgb.shape[0]), (0, 255, 0), 2)
        cv2.line(self.background, (0, center_y), (edge_background_rgb.shape[1], center_y), (0, 255, 0), 2)
        # cv2.imwrite('output.png', self.background)

        return center_x  - 41 # -41 because we need the start of the piece, not the center


if __name__ == '__main__':
    SlideSolver.test()