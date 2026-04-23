import re
from database.schema import SCHEMA

class SQLParser:
    def parse(self, query):
        query = query.strip().replace("\n", " ")
        query = re.sub(r"\s+", " ", query)

        pattern = re.compile(
            r"""
            SELECT\s+(?P<select>.+?)\s+
            FROM\s+(?P<from>.+?)
            (?:\s+WHERE\s+(?P<where>.+))?
            $
            """,
            re.IGNORECASE | re.VERBOSE
        )

        match = pattern.match(query)

        if not match:
            raise ValueError("Consulta SQL inválida")

        select_part = match.group("select")
        from_part = match.group("from")
        where_part = match.group("where")

        select_fields = [f.strip() for f in select_part.split(",")]

        # =========================
        # JOIN
        # =========================
        tables = []
        joins = []

        parts = re.split(r"INNER JOIN", from_part, flags=re.IGNORECASE)

        tables.append(parts[0].strip())

        for part in parts[1:]:
            join_match = re.search(r"(\w+)\s+ON\s+(.+)", part.strip(), re.IGNORECASE)
            if not join_match:
                raise ValueError("Erro no INNER JOIN")

            tables.append(join_match.group(1))
            joins.append(join_match.group(2))

        # =========================
        # VALIDAÇÃO TABELAS
        # =========================
        for table in tables:
            if table not in SCHEMA:
                raise ValueError(f"Tabela inválida: {table}")

        # =========================
        # VALIDAÇÃO CAMPOS
        # =========================
        def validate_field(field):
            if "." in field:
                t, c = field.split(".")
                return t in SCHEMA and c in SCHEMA[t]
            return any(field in SCHEMA[t] for t in tables)

        for field in select_fields:
            if field != "*" and not validate_field(field):
                raise ValueError(f"Campo inválido: {field}")

        # =========================
        # WHERE
        # =========================
        conditions = []
        if where_part:
            conditions = re.split(r"\s+AND\s+", where_part, flags=re.IGNORECASE)

            for cond in conditions:
                if not re.search(r"(=|>|<|<=|>=|<>)", cond):
                    raise ValueError(f"Condição inválida: {cond}")

        return {
            "select": select_fields,
            "from": tables,
            "joins": joins,
            "where": conditions
        }