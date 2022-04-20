import glob
from collections import namedtuple

# =============================================================================
# Config - put the path of your data here
# =============================================================================

current_path = "C:\\Users\\shann\\OneDrive\\Documents\\deep-learning\\c\\docstrings\\"

# =============================================================================
# Process data
# =============================================================================


def find_duplicates(current_path: str) -> None:
    """ """
    _f_train = open(f"{current_path}javadoc_train.original", 'r', encoding='utf-8')
    _f_test = open(f"{current_path}javadoc_train.original", 'r', encoding='utf-8')
    _f_dev = open(f"{current_path}javadoc_dev.original", 'r', encoding='utf-8')
    _code_train = open(f"{current_path}code_train.original", 'r', encoding='utf-8')
    _code_test = open(f"{current_path}code_test.original", 'r', encoding='utf-8')
    _code_dev = open(f"{current_path}code_dev.original", 'r', encoding='utf-8')

    # Initial training data dictionary
    train_duplicate_count = {}
    for docstring, code_line in zip(_f_train, _code_train):
        if f"{docstring} {code_line}" not in train_duplicate_count:
            train_duplicate_count[f"{docstring} {code_line}"] = 0

    # Compare to test
    test_duplicate_count = train_duplicate_count.copy()
    for docstring, code_line in zip(_f_test, _code_test):
        if f"{docstring} {code_line}" not in test_duplicate_count:
            test_duplicate_count[f"{docstring} {code_line}"] = 0
        else:
            test_duplicate_count[f"{docstring} {code_line}"] += 1

    # Compare to dev
    dev_duplicate_count = train_duplicate_count.copy()
    for docstring, code_line in zip(_f_dev, _code_dev):
        if f"{docstring} {code_line}" not in dev_duplicate_count:
            dev_duplicate_count[f"{docstring} {code_line}"] = 0
        else:
            dev_duplicate_count[f"{docstring} {code_line}"] += 1

    test_lines_with_duplicate = 0
    test_total_duplicates = 0
    for key, value in test_duplicate_count.items():
        if value > 0:
            test_lines_with_duplicate += 1
            test_total_duplicates += value

    dev_lines_with_duplicate = 0
    dev_total_duplicates = 0
    for key, value in dev_duplicate_count.items():
        if value > 0:
            dev_lines_with_duplicate += 1
            dev_total_duplicates += value

    result = {"Test": {"lines_with_duplicate": test_lines_with_duplicate,
                       "total_duplicates": test_total_duplicates},
              "Dev": {"lines_with_duplicate": dev_lines_with_duplicate,
                      "total_duplicates": dev_total_duplicates}}

    return result, test_duplicate_count, dev_duplicate_count

results, test_duplicate_count, dev_duplicate_count = find_duplicates(current_path)
