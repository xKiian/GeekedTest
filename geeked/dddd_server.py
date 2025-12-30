import os
import pathlib

root_dir = pathlib.Path(__file__).resolve().parent.parent
onnx_path = os.path.join(root_dir, 'geeked', 'models', 'geetest_v4_icon.onnx')
charsets_path = os.path.join(root_dir, 'geeked', 'models', 'charsets.json')


class DdddService:
    def __init__(self):
        import ddddocr
        self.det = ddddocr.DdddOcr(det=True, show_ad=False)
        self.cnn = ddddocr.DdddOcr(det=False, ocr=False,
                                   show_ad=False,
                                   import_onnx_path=onnx_path,
                                   charsets_path=charsets_path)

    def detection(self, img):
        return self.det.detection(img)

    def classification(self, img):
        return self.cnn.classification(img)

