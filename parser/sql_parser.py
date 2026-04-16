import re

class SQLParser:
    def parse(self, query):
        query = query.strip()

        pattern = re.compile(
            r"SELECT (.+?) FROM (.+?)( WHERE (.+))?$",
            re.IGNORECASE
        )

        match = pattern.match(query)

        if not match:
            raise ValueError("Consulta SQL inválida")

        select_part = match.group(1)
        from_part = match.group(2)
        where_part = match.group(4)

        select_fields = [f.strip() for f in select_part.split(',')]
        tables = [t.strip() for t in from_part.split(',')]

        conditions = []
        if where_part:
            conditions = re.split(r" AND | OR ", where_part, flags=re.IGNORECASE)

        return {
            "select": select_fields,
            "from": tables,
            "where": conditions
        }