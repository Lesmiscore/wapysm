
def reflect_get(obj, key):
    if isinstance(obj, dict):
        return obj.get(key)
    else:
        return getattr(obj, key, None)

def reflect_set(obj, key, value):
    if isinstance(obj, dict):
        obj[key] = value
    else:
        setattr(obj, key, value)

def reflect_delete_prop(obj, key):
    if isinstance(obj, dict):
        obj.pop(key, None)
    else:
        delattr(obj, key)
