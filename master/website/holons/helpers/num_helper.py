def num(s):
    """
    Utility unction
    takes a string, returns int/zero

    :param s:
    :return:
    """
    s = s.split('.')[0]
    try:
        return int(s)
    except ValueError:
        return 0

