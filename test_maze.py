import unittest

from maze import solve


class MazeTests(unittest.TestCase):
    def test_square_and_all_start_shapes(self):
        square = ["F-7", "|.|", "L-J"]
        for r, row in enumerate(square):
            for c, char in enumerate(row):
                if char == ".":
                    continue
                with self.subTest(start=(r, c)):
                    grid = square.copy()
                    grid[r] = row[:c] + "S" + row[c + 1:]
                    self.assertEqual(solve("\n".join(grid)), (4, 1))

    def test_complex_distance(self):
        self.assertEqual(solve("..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ..."), (8, 1))

    def test_enclosed_examples(self):
        cases = [
            (4, """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""),
            (4, """..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""),
            (8, """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""),
            (10, """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""),
        ]
        for expected, grid in cases:
            with self.subTest(expected=expected, grid=grid):
                self.assertEqual(solve(grid)[1], expected)

    def test_junk_pipes_inside_and_outside(self):
        self.assertEqual(solve("-L|F7\n7S-7|\nL|7||\n-L-J|\nL|-JF"), (4, 1))

    def test_smallest_loop(self):
        self.assertEqual(solve("S7\nLJ\n"), (2, 0))

if __name__ == "__main__":
    unittest.main()
