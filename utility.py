def filter_dict(d, f):
    new_dict = dict()
    for key, value in d.items():
        if f(key, value):
            new_dict[key] = value
    return new_dict
