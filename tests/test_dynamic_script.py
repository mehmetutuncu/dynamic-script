import os
import unittest

from main import main, remove_script, is_script_file_exists
from models import Script
from exceptions import *


class DynamicScriptTestCase(unittest.TestCase):
    def setUp(self) -> None:
        if not os.path.isdir('scripts'):
            os.mkdir('scripts')
        script_1_code = """from oop_test import BaseFirst, BaseSecond
class MyPrint(BaseFirst, BaseSecond):
    @staticmethod
    def my_print(text):
        print(f"My Print: {text}")
        return text
    def test_method(self, a, b):
        return a + b""".strip()
        self.script_1 = Script.create(name="Test Script", script=script_1_code,
                                      path="./scripts/test.py",
                                      importable_path="scripts.test.MyPrint",
                                      method_requirements={
                                          "method_name": "my_print", "kwargs": [
                                              {"text": {"required": True}}]})

        script_2_code = """from oop_test import BaseFirst, BaseSecond
class MyPrint(BaseFirst, BaseSecond):
    def __init__(self, first_param):
        self.first_param = first_param
    @staticmethod
    def my_print(text):
        print(f"My Print: {text}")
        return text
    def test_method(self, a, b):
        return a + b + self.first_param""".strip()

        self.script_2 = Script.create(name="Test Script 2",
                                      script=script_2_code,
                                      path="./scripts/test_2.py",
                                      importable_path="scripts.test_2.MyPrint",
                                      method_requirements={},
                                      initialization_params={"first_param": 30})

    def tearDown(self) -> None:
        path = self.script_1.path
        if is_script_file_exists(path):
            remove_script(path)
        self.script_1.delete_instance()
        self.script_2.delete_instance()

    def test_script_is_empty(self):
        result = main(script=None)
        self.assertIsNone(result)

    def test_method_type_error(self):
        with self.assertRaises(MethodTypeError):
            main(script=self.script_1)

    def test_import_error(self):
        self.script_1.importable_path = "scripts.test.MyPrint2"
        with self.assertRaises(KlassImportError):
            main(script=self.script_1)

    def test_dynamic_method_for_script_1(self):
        text = "test_dynamic_method"
        result = main(script=self.script_1, method_kwargs_data={"text": text})
        self.assertEqual(result, text)

    def test_base_class_method(self):
        self.script_1.method_requirements = {
            "method_name": "base_print", "kwargs": {}
        }
        result = main(script=self.script_1)
        self.assertEqual(result, "BaseFirst: Hello I am base class.")

    def test_use_klass_without_dynamic(self):
        klass = main(script=self.script_1, use_dynamic=False)
        result = klass.test_method(a=10, b=20)
        self.assertEqual(30, result)

    def test_initialize_klass_with_db_value(self):
        klass = main(script=self.script_2, use_dynamic=False)
        result = klass.test_method(a=10, b=20)
        self.assertEqual(60, result)

    def test_initialize_klass_with_value(self):
        klass_kwargs_data = {"first_param": 40}
        klass = main(script=self.script_2, use_dynamic=False,
                     klass_kwargs_data=klass_kwargs_data)
        result = klass.test_method(a=10, b=20)
        self.assertEqual(70, result)
