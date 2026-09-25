import ast
import unittest
from pathlib import Path


def _load_estimate_functions():
    module_path = Path(__file__).resolve().parents[1] / "unreal_mcp_server_advanced.py"
    source = module_path.read_text(encoding="utf-8")
    parsed = ast.parse(source)

    selected = []
    target_names = {"_estimate_town_counts", "_estimate_maze_counts"}
    for node in parsed.body:
        if isinstance(node, ast.FunctionDef) and node.name in target_names:
            selected.append(node)

    namespace = {"Dict": dict, "Any": object}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(module_path), "exec"), namespace)
    return namespace["_estimate_town_counts"], namespace["_estimate_maze_counts"]


class PlanningEstimateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        estimate_town, estimate_maze = _load_estimate_functions()
        cls.estimate_town = staticmethod(estimate_town)
        cls.estimate_maze = staticmethod(estimate_maze)

    def test_town_estimate_contains_expected_metrics(self):
        estimate = self.estimate_town("medium", 0.8, True)
        self.assertEqual(estimate["town_size"], "medium")
        self.assertGreater(estimate["estimated_street_segments"], 0)
        self.assertGreaterEqual(estimate["estimated_buildings"], 0)
        self.assertGreaterEqual(estimate["estimated_infrastructure"], 0)
        self.assertEqual(
            estimate["estimated_total_actors"],
            estimate["estimated_street_segments"] + estimate["estimated_buildings"] + estimate["estimated_infrastructure"],
        )

    def test_town_estimate_clamps_density(self):
        zero_density = self.estimate_town("small", -1.0, False)
        high_density = self.estimate_town("small", 5.0, False)
        self.assertEqual(zero_density["estimated_buildings"], 0)
        self.assertGreaterEqual(high_density["estimated_buildings"], zero_density["estimated_buildings"])

    def test_maze_estimate_contains_expected_metrics(self):
        estimate = self.estimate_maze(8, 6, 3)
        self.assertEqual(estimate["rows"], 8)
        self.assertEqual(estimate["cols"], 6)
        self.assertEqual(estimate["wall_height"], 3)
        self.assertEqual(estimate["estimated_marker_actors"], 2)
        self.assertEqual(
            estimate["estimated_total_actors"],
            estimate["estimated_wall_actors"] + estimate["estimated_marker_actors"],
        )


if __name__ == "__main__":
    unittest.main()
