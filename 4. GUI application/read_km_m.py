import cv2
import pytesseract


def get_numbers_from_image(gray_image):
    text_1 = pytesseract.image_to_string(
        (gray_image < 250),
        lang="eng",
        config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789",
    )
    res = text_1.strip()
    if res == "":
        res = "0"
    return res


def get_coordinates_of_frame(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text_image_1 = gray[-50:-20, 24:75]
    text_image_2 = gray[-50:-20, 110:155]

    return (get_numbers_from_image(text_image_1), get_numbers_from_image(text_image_2))
