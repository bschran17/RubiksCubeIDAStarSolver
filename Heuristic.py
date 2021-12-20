from rubik.cube import Cube
import math

SOLVED_CUBE = Cube("WWWWWWWWWGGGRRRBBBOOOGGGRRRBBBOOOGGGRRRBBBOOOYYYYYYYYY")


def md_single(piece):
    colors = piece.colors
    solved_piece = SOLVED_CUBE.find_piece(colors)
    return (
        abs(piece.pos[0] - solved_piece.pos[0])
        + abs(piece.pos[1] - solved_piece.pos[1])
        + abs(piece.pos[2] - solved_piece.pos[2])
    )


def orientation_check(piece):
    lst = []
    colors = piece.colors
    pos = piece.pos
    if (
        pos[0] == -1
        and colors[0] == "G"
        or pos[0] == 0
        and colors[0] == None
        or pos[0] == 1
        and colors[0] == "B"
    ):
        lst.append(True)
    if (
        pos[1] == -1
        and colors[1] == "Y"
        or pos[1] == 0
        and colors[1] == None
        or pos[1] == 1
        and colors[1] == "W"
    ):
        lst.append(True)
    if (
        pos[2] == -1
        and colors[2] == "O"
        or pos[2] == 0
        and colors[2] == None
        or pos[2] == 1
        and colors[2] == "R"
    ):
        lst.append(True)
    return len(lst)


def edge_next_to_or_opposite(piece):
    lst = []
    colors = piece.colors
    pos = piece.pos
    solved_piece = SOLVED_CUBE.find_piece(colors)
    if pos[0] == solved_piece.pos[0]:
        lst.append(True)
    if pos[1] == solved_piece.pos[1]:
        lst.append(True)
    if pos[2] == solved_piece.pos[2]:
        lst.append(True)
    return len(lst)


def opposite_orientation_check(piece):
    lst = []
    colors = piece.colors
    pos = piece.pos
    solved_piece = SOLVED_CUBE.find_piece(colors)
    if colors[0] == solved_piece.colors[0]:
        lst.append(True)
    if colors[1] == solved_piece.colors[1]:
        lst.append(True)
    if colors[2] == solved_piece.colors[2]:
        lst.append(True)


def moves_to_solve_piece(piece, md):
    if md == 0:
        if orientation_check(piece) == 3:
            return 0
        else:
            return 3
    elif md == 2:
        if edge_next_to_or_opposite(piece) == 1:
            if orientation_check(piece) == 2:
                return 1
            else:
                return 2
        else:
            if orientation_check(piece) == 2:
                return 1
            else:
                return 3
    elif md == 4:
        return 2
    elif md == 6:
        if opposite_orientation_check(piece) == 3:
            return 2
        else:
            return 3
    else:
        print("md error: ", md)
        return


def moves_to_solve(cube):
    moves = 0
    for piece in cube.pieces:
        md = md_single(piece)
        moves += moves_to_solve_piece(piece, md)
    return moves


def heuristic(cube):
    moves = 0
    for piece in cube.edges:
        md = md_single(piece)
        moves += moves_to_solve_piece(piece, md)
    return math.ceil(moves / 4)
