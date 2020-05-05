def rgb_i2f(int_rgb: int) -> float:
    """
    Converts a RGB int value to float representation,
    useful when using glColor.

    :param int_rgb:
    :return:
    """
    return round(1 / 255 * int_rgb, 3)
