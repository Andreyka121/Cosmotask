import argparse
import json
from pathlib import Path

from maze import solve, trace_loop


def enclosed_tiles(grid, loop):
    boundary = set(loop)
    crossings = [[] for _ in grid]
    for i, (r, c) in enumerate(loop):
        nr, nc = loop[(i + 1) % len(loop)]
        if r != nr:
            crossings[min(r, nr)].append(c)

    inside = []
    for r, columns in enumerate(crossings):
        columns.sort()
        for left, right in zip(columns[::2], columns[1::2]):
            inside.extend((r, c) for c in range(left + 1, right)
                          if (r, c) not in boundary)
    return inside


def render_html(text, name="puzzle_input.txt"):
    grid = text.splitlines()
    loop = trace_loop(text)
    part1, part2 = solve(text)
    inside = enclosed_tiles(grid, loop)
    if len(inside) != part2:
        raise ValueError("Interior coordinates disagree with Pick's theorem.")
    data = dict(grid=grid, loop=loop, inside=inside,
                part1=part1, part2=part2, name=name)
    payload = json.dumps(data, ensure_ascii=True).replace("<", "\\u003c")
    template = Path(__file__).with_name("maze_viewer.html").read_text(encoding="utf-8")
    return template.replace("__MAZE_DATA__", payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, nargs="?",
                        default=Path(__file__).with_name("puzzle_input.txt"))
    parser.add_argument("-o", "--output", type=Path,
                        default=Path(__file__).with_name("maze_visualization.html"))
    args = parser.parse_args()
    if args.output.resolve() in {args.input.resolve(), Path(__file__).resolve(),
                                  Path(__file__).with_name("maze_viewer.html").resolve()}:
        parser.error("Choose an output path different from the input and source files.")
    html = render_html(args.input.read_text(), args.input.name)
    args.output.write_text(html, encoding="utf-8")
    print(f"HTML: {args.output.resolve()}")


if __name__ == "__main__":
    main()
