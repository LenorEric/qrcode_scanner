import cv2
from pyzbar.pyzbar import decode
from .ImageHandler import ImageHandler

__all__ = ["decode_qrcode"]


def get_fixed_qrcode(img):
    obj = ImageHandler(img)
    transform_image = obj.qr_code_in_image()
    return transform_image


# @profile_line
def decode_qrcode(img):
    """
    Decode qrcode_scanner from image.
    :param img: opencv image
    :return: code string
    """
    if img.shape[0] != 600:
        w = 600 * img.shape[1] // img.shape[0]
        img = cv2.resize(img, (w, 600))
    """使用原始二维码图片解码"""
    raw = decode(img)
    decoded = list(map(lambda x: x.data.decode('utf-8'), raw))
    if decoded:
        return decoded[0]
    """原始二维码解码失败，获取视角修正过的二维码图片，并解码"""
    try:
        fixed_img = get_fixed_qrcode(img.copy())
        if fixed_img is not None:
            raw = decode(fixed_img)
            decoded = list(map(lambda x: x.data.decode('utf-8'), raw))
            return decoded[0] if decoded else None
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    pass
