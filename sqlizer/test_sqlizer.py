from .sqlizer import DMLConstructor


class TestDMLConstructor:

    def test_constructor_doesnt_throw_errors(self):
        DMLConstructor()
