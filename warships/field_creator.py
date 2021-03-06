from random import randint

def create_table(size: int) -> list:
    table = []
    for row in range (0, size):
        table.append(row)
        table[row]=[]
        for col in range(0, size):
            table[row].append(0)
    return table


def positions(start_row: int, start_col: int, orientation: int, length: int) -> list:
    result = []
    if orientation == 0:
        for i in range(length):
            result.append([start_row + i, start_col])
    else:
        for i in range(length):
            result.append([start_row, start_col + i])
    return result


def check_left_side(positions: list, field: list) -> bool:
    for row in positions:
        check_row = row[0]
        check_col = row[1] - 1
        try:
            field[check_row][check_col]
        except:
            return True
        if field[check_row][check_col] == 1:
            return False
    return True


def check_right_side(positions: list, field: list) -> bool:
    for row in positions:
        check_row = row[0]
        check_col = row[1] + 1
        try:
            field[check_row][check_col]
        except:
            return True
        if field[check_row][check_col] == 1:
            return False
    return True


def check_top_side(positions: list, field: list) -> bool:
    for row in positions:
        check_row = row[0] - 1
        check_col = row[1]
        try:
            field[check_row][check_col]
        except:
            return True
        if field[check_row][check_col] == 1:
            return False
    return True


def check_bottom_side(positions: list, field: list) -> bool:
    for row in positions:
        check_row = row[0] + 1
        check_col = row[1]
        try:
            field[check_row][check_col]
        except:
            return True
        if field[check_row][check_col] == 1:
            return False
    return True


def is_inside(start_row: int, start_col: int, orientation: int, length: int, field_size: int) -> bool:
    if orientation == 0:
        last_row = start_row + length - 1
        last_col = start_col
    else:
        last_row = start_row
        last_col = start_col + length - 1

    if last_col >= field_size or last_row >= field_size:
        return False

    return True


def check_all_sides(positions: list, field: list) -> bool:
    if check_bottom_side(positions, field) and check_top_side(positions, field) and check_left_side(positions, field) and check_right_side(positions, field):
        return True
    return False


def create_ship(ship_size: int, field: list, amount: int) -> list:
    passed = False
    counter = 1
    while not passed:
        orientation = randint(0, 1)
        start_row = randint(0, len(field) - 1)
        start_col = randint(0, len(field) - 1)
        ship_position = positions(start_row, start_col, orientation, ship_size)
        if is_inside(start_row, start_col, orientation, ship_size, len(field)) and check_all_sides(ship_position, field):
            for pos in ship_position:
                field[pos[0]][pos[1]] = 1
            counter += 1
            if counter >= amount:
                passed = True
        else:
            passed = False
    return field


# ARRAY OF ARRAYS [ [AMOUNT OF SHIPS, HOW LONG] ]
def create_ships(arr: list, table: list) -> list:
    for i in range(len(arr)):
        table = create_ship(arr[i][1], table, arr[i][0])
    return table
