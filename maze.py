import argparse
from pathlib import Path


NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)
CONNECTIONS = {
    "|": (NORTH, SOUTH),
    "-": (WEST, EAST),
    "L": (NORTH, EAST),
    "J": (NORTH, WEST),
    "7": (SOUTH, WEST),
    "F": (SOUTH, EAST),
}


def trace_loop(text: str) -> list[tuple[int, int]]:
    grid = text.splitlines()
    height, width = len(grid), len(grid[0])
    start = next(
        (r, row.index("S"))
        for r, row in enumerate(grid)
        if "S" in row
    )

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < height and 0 <= c < width

    start_directions = []
    for dr, dc in (NORTH, SOUTH, WEST, EAST):
        r, c = start[0] + dr, start[1] + dc
        if in_bounds(r, c) and (-dr, -dc) in CONNECTIONS.get(grid[r][c], ()):
            start_directions.append((dr, dc))

    def neighbors(position: tuple[int, int]) -> list[tuple[int, int]]:
        r, c = position
        directions = start_directions if position == start else CONNECTIONS.get(grid[r][c], ())
        result = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not in_bounds(nr, nc):
                continue
            other = start_directions if (nr, nc) == start else CONNECTIONS.get(grid[nr][nc], ())
            if (-dr, -dc) in other:
                result.append((nr, nc))
        return result

    loop = [start]
    previous, current = start, neighbors(start)[0]
    while current != start:
        loop.append(current)
        adjacent = neighbors(current)
        following = adjacent[0] if adjacent[1] == previous else adjacent[1]
        previous, current = current, following
    return loop


def solve(text: str) -> tuple[int, int]:
    loop = trace_loop(text)
    length = len(loop)

    # площа * 2
    signed_area2 = 0
    for i, (row, col) in enumerate(loop):
        next_row, next_col = loop[(i + 1) % length]
        signed_area2 += col * next_row - next_col * row

    # теорема Піка для внутрішніх точок 
    inside = (abs(signed_area2) - length + 2) // 2
    return length // 2, inside


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipe maze")
    parser.add_argument(
        "input",
        type=Path,
        nargs="?",
        default=Path(__file__).resolve().with_name("puzzle_input.txt"),
        help="Maze file (default: puzzle_input.txt beside maze.py)",
    )
    args = parser.parse_args()
    try:
        part1, part2 = solve(args.input.read_text())
    except (OSError, UnicodeError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")


if __name__ == "__main__":
    main()
