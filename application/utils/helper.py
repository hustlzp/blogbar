def parse_int(integer):
    try:
        return int(integer)
    except Exception, e:
        return None
