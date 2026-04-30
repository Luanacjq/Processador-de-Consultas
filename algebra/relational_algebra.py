def to_relational_algebra(parsed):
    select = parsed["select"]
    tables = parsed["tables"]
    conditions = parsed["where"]

    join_expr = " |X| ".join(tables)
    where_expr = " σ ".join(conditions)

    return f"π {select} ( σ {where_expr} (|X| {join_expr}) )"