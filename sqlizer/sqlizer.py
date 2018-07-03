from jinja2 import Template


class StringType:
    def __init__(self, value):
        self.val = value

    def __repr__(self):
        return """'{0}'""".format(self.val)

    def __str__(self):
        return """'{0}'""".format(self.val)


class ExprType:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class DMLConstructor:

    def __init__(self, **kwargs):
        """
        This class is a template generator for SQL DML statements.
        :param kwargs:
        """
        self._target_table = kwargs.get("target_table", None)  # Target table object.
        self._target_database = kwargs.get("target_database", None)  # Target database object.

        self.target_database_table_name = None  # Container for constructing the fully qualified target table name.
        self.target_columns = None  # Container for target columns string.
        self.value_statement = None  # Container for the value statement to carry out the DML.
        self.insert_template = Template(
            """INSERT INTO {{target_database_table_name}}{{target_columns or NONE}} {{value_statement}};""")

    # region private
    def __construct_database_table_name__(self):
        if not self._target_database:
            self.target_database_table_name = self._target_table
        else:
            self.target_database_table_name = "{0}.{1}".format(self._target_database, self._target_table)

    # endregion

    # region public

    def target_database(self, value=None):
        """
        Getter and setter method for the target database.
        :param value: (Optional)  Value of the target database if to be set, else None.
        :return: Target database if value None else self.
        """
        if not value:
            return self._target_database
        else:
            self._target_database = value
            return self

    def insert_as_select(self, **kwargs):
        raise NotImplementedError()

    def insert_as_values(self, values_to_insert):
        """
        This method implements the insert statement using values. An example is:
        INSERT INTO database.table (col1,col2) VALUES(val1,val2);
        :param values_to_insert: List or dictionary of values. if dictionary, the dictionary key should correspond to
                the target column name. { "col1" : val1,"col3":val3} is INSERT INTO ... (col1,col3) VALUES (val1,
                val3).l
        :return: Self
        """
        if isinstance(values_to_insert, dict):
            _t_cols = []
            _t_vals = []

            for k, v in values_to_insert.items():
                _t_cols.append(k)
                _t_vals.append(v)

            self.target_columns = "({0})".format(",".join(_t_cols))
            self.target_columns = " " + self.target_columns
            # Appropriately convert the string values to be wrapped with single quotes.
            self.value_statement = "VALUES({0})".format(
                ",".join([str(StringType(v)) if isinstance(v, str) else str(v) for v in _t_vals]))
        if isinstance(values_to_insert, list):
            # Appropriately convert the string values to be wrapped with single quotes.
            self.value_statement = "VALUES({0})".format(
                ",".join([str(StringType(v)) if isinstance(v, str) else str(v) for v in values_to_insert]))
            self.target_columns = None  # Blank because not specified.
        return self

    def get_sql(self):
        """
        Returns the rendered sql as string.
        :return: string
        """
        self.__construct_database_table_name__()
        return self.insert_template.render(target_database_table_name=self.target_database_table_name,
                                           target_columns=self.target_columns, value_statement=self.value_statement)

        # endregion


if __name__ == '__main__':
    print(DMLConstructor(target_table="batch", target_database="mydb").insert_as_values(
        {"mycol1": 1, "mycol2": "2"}).get_sql())
    print(DMLConstructor(target_table="batch").insert_as_values(["myString", 2]).get_sql())

    print(StringType("hello"))
