import re

def parse_sql(query):
    query = query.lower()
    query = re.sub(r"\s+", " ", query).strip()

    # SELECT
    select_match = re.search(r"select (.+?) from", query)
    if not select_match:
        raise ValueError("SELECT inválido")

    select_fields = [s.strip() for s in select_match.group(1).split(",")]


    # FROM + JOIN (com alias)
    from_match = re.search(r"from (.+?)( where|$)", query)
    if not from_match:
        raise ValueError("FROM inválido")

    from_part = from_match.group(1)

    table_pattern = r"(\w+)(?:\s+(\w+))?"

    join_pattern = r"(inner|left|right)?\s*join\s+(\w+)(?:\s+(\w+))?\s+on\s+([^ ]+ [=<>]+ [^ ]+)"

    joins = re.findall(join_pattern, from_part)

    first_table_part = re.split(r"\s+(inner|left|right)?\s*join\s+", from_part)[0].strip()

    first_table_match = re.match(table_pattern, first_table_part)

    base_table = first_table_match.group(1)
    base_alias = first_table_match.group(2) or base_table

    tables = [base_alias]
    alias_map = {base_alias: base_table}

    join_conditions = []
    join_types = []

    for join_type, table, alias, condition in joins:
        alias = alias or table

        tables.append(alias)
        alias_map[alias] = table

        join_conditions.append(condition.strip())
        join_types.append(join_type.upper() if join_type else "INNER")

    # WHERE (AND / OR)

    where_match = re.search(r"where (.+)", query)
    conditions = []
    logical_ops = []

    if where_match:
        where_clause = where_match.group(1)

        tokens = re.split(r"\s+(and|or)\s+", where_clause)

        conditions = tokens[::2]
        logical_ops = tokens[1::2]

        valid_ops = ["=", ">", "<", "<=", ">=", "<>"]

        for cond in conditions:
            if not any(op in cond for op in valid_ops):
                raise ValueError(f"Operador inválido na condição: {cond}")

    return {
        "select": select_fields,
        "tables": tables,
        "where": [c.strip() for c in conditions],
        "logical_ops": logical_ops,
        "joins": join_conditions,
        "join_types": join_types,
        "alias_map": alias_map
    }