VALID_TABLES = {
    "categoria": [
        "idcategoria", "descricao"
    ],
    "produto": [
        "idproduto", "nome", "descricao", "preco",
        "quantestoque", "categoria_idcategoria"
    ],
    "tipocliente": [
        "idtipocliente", "descricao"
    ],
    "cliente": [
        "idcliente", "nome", "email", "nascimento",
        "senha", "tipocliente_idtipocliente", "dataregistro"
    ],
    "tipoendereco": [
        "idtipoendereco", "descricao"
    ],
    "endereco": [
        "idendereco", "enderecopadrao", "logradouro",
        "numero", "complemento", "bairro", "cidade",
        "uf", "cep", "tipoendereco_idtipoendereco",
        "cliente_idcliente"
    ],
    "telefone": [
        "numero", "cliente_idcliente"
    ],
    "status": [
        "idstatus", "descricao"
    ],
    "pedido": [
        "idpedido", "status_idstatus", "datapedido",
        "valortotalpedido", "cliente_idcliente"
    ],
    "pedido_has_produto": [
        "idpedidoproduto", "pedido_idpedido",
        "produto_idproduto", "quantidade", "precounitario"
    ]
}
def validate(parsed):
    errors = []

    for table in parsed["tables"]:
        table_name = table.split()[0]
        if table_name not in VALID_TABLES:
            errors.append(f"Tabela inválida: {table_name}")

    for field in parsed["select"]:
        table = field.split(".")[0]
        attr = field.split(".")[1]

        if table in VALID_TABLES:
            if attr not in VALID_TABLES[table]:
                errors.append(f"Campo inválido: {field}")

    return errors