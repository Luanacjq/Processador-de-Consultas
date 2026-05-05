def to_relational_algebra(parsed):
    select = parsed["select"]
    tables = parsed["tables"]
    conditions = parsed["where"]
    ops = parsed.get("logical_ops", [])

    join_expr = " |X| ".join(tables)

    if conditions:
        expr = conditions[0]
        for i, op in enumerate(ops):
            symbol = "∧" if op == "and" else "∨"
            expr += f" {symbol} {conditions[i+1]}"

        return f"π {select} ( σ ({expr}) ({join_expr}) )"
    else:
        return f"π {select} ({join_expr})"