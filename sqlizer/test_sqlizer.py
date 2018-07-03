from .sqlizer import DMLConstructor, ExprType


class TestDMLConstructor:

    def test_string_valued_inputs(self):
        target = """INSERT INTO database.table  VALUES('string1','string2');"""

        generated = DMLConstructor(target_database='database', target_table='table').insert_as_values(
            ["string1", "string2"]).get_sql()

        assert target == generated

    def test_inputs_with_column_definitions(self):
        target = """INSERT INTO database.table (col1,col2) VALUES('string1','string2');"""

        generated = DMLConstructor(target_database='database', target_table='table').insert_as_values(
            {"col1": "string1", "col2": "string2"}).get_sql()

        assert target == generated

    def test_expression_inputs(self):
        target = """INSERT INTO database.table  VALUES(table.myExpression(),'string2');"""

        generated = DMLConstructor(target_database='database', target_table='table').insert_as_values(
            [ExprType("table.myExpression()"), 'string2']).get_sql()

        assert target == generated
