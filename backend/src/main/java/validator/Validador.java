package com.seuprojeto.validator;

import com.seuprojeto.model.Query;

import java.util.regex.Pattern;

public class Validador {

    private static final Pattern CAMPO_PATTERN =
        Pattern.compile("^[a-zA-Z_][a-zA-Z0-9_]*$");

    private static final Pattern CONDICAO_PATTERN =
        Pattern.compile("^[a-zA-Z_][a-zA-Z0-9_]*\\s*(=|>|<)\\s*.+$");

    public static void validar(Query query) {

        // 🔹 Campos
        if (query.campos == null || query.campos.isEmpty()) {
            throw new RuntimeException("SELECT sem campos");
        }

        for (String campo : query.campos) {
            if (!CAMPO_PATTERN.matcher(campo).matches()) {
                throw new RuntimeException("Campo inválido: " + campo);
            }
        }

        // 🔹 Tabela
        if (query.tabela == null || query.tabela.isEmpty()) {
            throw new RuntimeException("Tabela não informada");
        }

        if (!CAMPO_PATTERN.matcher(query.tabela).matches()) {
            throw new RuntimeException("Nome de tabela inválido");
        }

        // 🔹 Condição
        if (query.condicao != null) {

            if (!CONDICAO_PATTERN.matcher(query.condicao).matches()) {
                throw new RuntimeException("Condição WHERE inválida");
            }
        }
    }
}