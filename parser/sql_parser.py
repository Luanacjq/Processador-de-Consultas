import re

def parse_sql(query):
    query = query.lower()
    query = re.sub(r"\s+", " ", query).strip()

    # SELECT
    select_match = re.search(r"select (.+?) from", query)
    if not select_match:
        raise ValueError("SELECT inválido")

    select_fields = [s.strip() for s in select_match.group(1).split(",")]

    # FROM + INNER JOIN
    from_match = re.search(r"from (.+?)( where|$)", query)
    if not from_match:
        raise ValueError("FROM inválido")

    from_part = from_match.group(1)

    join_pattern = r"inner join\s+(\w+)\s+on\s+([^ ]+ [=<>]+ [^ ]+)"
    joins = re.findall(join_pattern, from_part)

    first_table = re.split(r"inner join", from_part)[0].strip()

    tables = [first_table]
    join_conditions = []

    for table, condition in joins:
        tables.append(table.strip())
        join_conditions.append(condition.strip())

    # WHERE
    where_match = re.search(r"where (.+)", query)
    conditions = []

    if where_match:
        where_clause = where_match.group(1)

        conditions = re.split(r"\s+and\s+", where_clause)

        valid_ops = ["=", ">", "<", "<=", ">=", "<>"]

        for cond in conditions:
            if not any(op in cond for op in valid_ops):
                raise ValueError(f"Operador inválido na condição: {cond}")

    return {
        "select": select_fields,
        "tables": tables,
        "where": conditions,
        "joins": join_conditions
    }