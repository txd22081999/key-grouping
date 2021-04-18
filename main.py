import re
import json


def get_date_key(str):
    # pattern = "[]*."
    # pattern = "^(0[1-9]|[12][0-9]|3[01])[- /.]"
    # pattern = "\+d_\+d_\+d"
    pattern = "(\d{4})_(\d{2})_(\d{2})"
    match = re.findall(pattern, str)

    if match != None:
        matchStr = "".join("_".join(item) for item in match)
    return "." + matchStr


def dict_val(dict):
    for key, val in dict.items():
        return val


def dict_key(dict):
    for key, val in dict.items():
        return key


def set_at(set, index):
    return list(set)[index]


def get_set_diff(set1, set2):
    diff1 = set1.difference(set2)
    diff2 = set2.difference(set1)
    if diff1:
        return diff1
    if diff2:
        return diff2
    return set()


def get_key_set(file):
    key_set = {}
    main_keys = []
    sub_keys = []

    # DC Keys
    for line in file:
        length = line.split(".").__len__()

        if length >= 3:
            date_key = get_date_key(line)
            line = line.replace(date_key, "")

        line = line.replace("\n", "")
        keys = line.split(".")

        if len(keys) > 1:
            main_keys.append(keys[0])
            sub_keys.append({keys[0]: keys[1]})

    for i in range(len(main_keys)):
        item_key = main_keys[i]
        key_set[item_key] = set()

    for i in range(len(main_keys)):
        item_key = main_keys[i]
        item_val = dict_val(sub_keys[i])
        key_set[item_key].add(item_val)

    return key_set


def main():
    f1 = open("./data/dc_redis_key_value.txt", "r")
    f2 = open("./data/mx_redis_key_value.txt", "r")

    dc_key_set = get_key_set(f1)
    mx_key_set = get_key_set(f2)

    dc_main_keys = []
    mx_main_keys = []

    dc_sub_keys = []
    mx_sub_keys = []

    for main_key, val in dc_key_set.items():
        dc_main_keys.append(main_key)
        dc_sub_keys.append(val)

    for main_key, val in mx_key_set.items():
        mx_main_keys.append(main_key)
        mx_sub_keys.append(val)

    diff_main_keys = [item for item in dc_main_keys if item not in mx_main_keys]
    diff_sub_keys = [item for item in dc_sub_keys if item not in mx_sub_keys]

    for main_key in dc_key_set:
        if main_key in mx_key_set:
            diff = get_set_diff(mx_key_set[main_key], dc_key_set[main_key])
            if len(diff) > 0:
                print(f"Difference in {main_key}: {diff}")
            # else:
            #     print("EQUAL")
            # print(mx_key_set[main_key] - dc_key_set[main_key])

    # print(len(set1 - set2))
    # print(len(set1.difference(set2)))
    # Dict = {}
    # # Dict['Dict1'] = [1,2]
    # Dict['Dict1'].insert(0, 4)
    # # Dict['Dict1']['Sub1'] = 1
    # # Dict['Dict1'] = arr
    # Dict['Dict1'].append(3)
    # print(Dict)


if __name__ == "__main__":
    main()