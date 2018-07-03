# sqlizer
Creates sql templates based on programmatic inputs.
## Background
This essentially helps you to take inputs into SQL statements programmatically and then construct the SQL query.
for example:
Let's say you want to construct DML's from web-form. You can essentially get the column values as a list then construct the insert statement.
e.g.
`INSERT INTO database.table VALUES('staging','gdw');` You want to template the target database, the table and the values to be inserted.
With sqlizer you can do this by.
`DMConstructor(target_database='database', target_table='table').insert_as_values(["staging", "gdw"]).get_sql()`
