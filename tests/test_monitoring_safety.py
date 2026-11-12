"""Safety checks for the monitoring-only fork (standard library only)."""

import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATION = ROOT / "custom_components" / "advanced_climate"


def method(path: str, class_name: str, method_name: str) -> ast.AsyncFunctionDef | ast.FunctionDef:
    tree = ast.parse((INTEGRATION / path).read_text(encoding="utf-8"))
    cls = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == class_name
    )
    return next(
        node for node in cls.body
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef))
        and node.name == method_name
    )


def calls_named(node: ast.AST, name: str) -> list[ast.Call]:
    return [
        child for child in ast.walk(node)
        if isinstance(child, ast.Call)
        and isinstance(child.func, ast.Attribute)
        and child.func.attr == name
    ]


class TestMonitoringSafety(unittest.TestCase):
    def test_room_service_helper_never_calls_home_assistant_services(self) -> None:
        call = method("room_devices.py", "RoomDevices", "_call")
        self.assertFalse(calls_named(call, "async_call"))
        self.assertTrue(
            any(
                isinstance(node, ast.Return)
                and isinstance(node.value, ast.Constant)
                and node.value.value is False
                for node in ast.walk(call)
            )
        )

    def test_room_target_application_is_a_noop(self) -> None:
        apply = method("room_devices.py", "RoomDevices", "_async_apply")
        self.assertFalse(calls_named(apply, "async_call"))
        called = {
            node.func.attr
            for node in ast.walk(apply)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        self.assertNotIn("_async_apply_relay", called)
        self.assertNotIn("_async_apply_climate", called)

    def test_calibration_is_read_only(self) -> None:
        calibrate = method("room_devices.py", "RoomDevices", "_async_calibrate")
        self.assertFalse(calls_named(calibrate, "async_call"))
        self.assertFalse(
            any(isinstance(node, ast.Call) for node in ast.walk(calibrate))
        )

    def test_boiler_method_only_calculates_and_observes(self) -> None:
        boiler = method("house.py", "House", "_async_control_boiler")
        self.assertFalse(calls_named(boiler, "async_call"))

    def test_room_heat_demand_reads_the_real_relay_state(self) -> None:
        demand = method("room.py", "Room", "_update_demand")
        called = {
            node.func.attr
            for node in ast.walk(demand)
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
        }
        self.assertIn("_relay_actual", called)
        self.assertIn("_note_relay_state", called)

    def test_keep_open_output_feature_is_disabled(self) -> None:
        keep_open = method("house.py", "House", "_update_keep_open")
        self.assertFalse(calls_named(keep_open, "async_call"))


if __name__ == "__main__":
    unittest.main()
