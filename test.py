import random

assigned_ids_1 = [1]
assigned_ids_2 = [6]
assigned_ids_3 = [1, 5, 3]
assigned_ids_4 = [1,6,2]
assigned_ids_5 = [1,3,5,4,6]

def get_assignable_id(taken_id_list):
    assignable_id = [1, 2, 3, 4, 5, 6]
    for _id in taken_id_list:
        assignable_id.remove(_id)
    return assignable_id

test_1 = get_assignable_id(assigned_ids_1)

assert test_1 == [2, 3, 4, 5, 6], "Test 1 failed"

test_2 = get_assignable_id(assigned_ids_2)

assert test_2 == [1, 2, 3, 4, 5], "Test 2 failed"

test_3 = get_assignable_id(assigned_ids_3)

assert test_3 == [2, 4, 6], "Test 3 failed"

test_4 = get_assignable_id(assigned_ids_4)

assert test_4 == [3, 4, 5], "Test 4 failed"

test_5 = get_assignable_id(assigned_ids_5)

assert test_5 == [2], "Test 5 failed"


