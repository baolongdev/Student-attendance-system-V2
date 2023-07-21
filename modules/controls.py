global control_reference
control_reference = {}


def add_to_control_reference(key, value):
    global control_reference
    try:
        # print("add:", key)
        control_reference[key] = value

    except KeyError as e:
        print(e)
    finally:
        pass
    pass


def return_control_reference():
    global control_reference
    return control_reference


def get_from_control_reference(key):
    global control_reference
    try:
        return control_reference[key]
    except KeyError as e:
        print("Error:", e)
        return None
