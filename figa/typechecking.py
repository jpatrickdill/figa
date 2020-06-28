# type checking

converters = [str, int, float]  # don't use list or float as converters, leads to weird results with respect to configs


def check(types: dict, values: dict, trace=None):
    # checks whether the values match types of types argument, or can be converted

    trace = trace or []

    for item, type_ in types.items():
        # check if item exists
        if item not in values:
            trace.append(item)
            raise ValueError("Missing item {}".format(".".join(trace)))

        val = values[item]

        if isinstance(type_, dict):  # is sub-dict
            check(type_, val, trace + [item])
        else:
            if not isinstance(val, type_):
                if type_ in converters and type(val) in converters:
                    try:
                        nv = type_(val)
                    except ValueError:
                        trace.append(item)
                        raise ValueError("item {} doesn't match type {!r}".format(".".join(trace), type_.__name__))
                else:
                    trace.append(item)
                    raise ValueError("item {} doesn't match type {!r}".format(".".join(trace), type_.__name__))
