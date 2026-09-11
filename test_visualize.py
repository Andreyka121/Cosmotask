import json
import unittest
from unittest.mock import patch

import test_maze
from maze import solve, trace_loop
from visualize import enclosed_tiles, render_html


class VisualizationTests(unittest.TestCase):
    def test_interior_matches_all_maze_examples(self):
        def check(text):
            answers = solve(text)
            loop = trace_loop(text)
            inside = enclosed_tiles(text.splitlines(), loop)
            self.assertEqual(len(inside), answers[1])
            self.assertEqual(len(inside), len(set(inside)))
            self.assertTrue(set(inside).isdisjoint(loop))
            self.assertEqual(set(inside), set(enclosed_tiles(text.splitlines(), loop[::-1])))
            return answers

        with patch.object(test_maze, "solve", side_effect=check):
            suite = unittest.defaultTestLoader.loadTestsFromTestCase(test_maze.MazeTests)
            result = unittest.TestResult()
            suite.run(result)
            self.assertTrue(result.wasSuccessful(), result.errors + result.failures)

    def test_square_coordinates(self):
        text = "S-7\n|F|\nL-J"
        self.assertEqual(enclosed_tiles(text.splitlines(), trace_loop(text)), [(1, 1)])

    def test_embedded_data(self):
        name = '</script><script>alert("x")</script>'
        html = render_html("S7\nLJ", name)
        payload = html.split('<script id="maze-data" type="application/json">')[1].split('</script>')[0]
        data = json.loads(payload)
        self.assertEqual(data["name"], name)
        self.assertEqual(data["loop"], [[0, 0], [1, 0], [1, 1], [0, 1]])
        self.assertEqual(data["part1"], 2)
        self.assertEqual(data["inside"], [])
        self.assertNotIn(name, html)
        self.assertNotIn('__MAZE_DATA__', html)


if __name__ == "__main__":
    unittest.main()
