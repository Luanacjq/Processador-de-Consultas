package com.seuprojeto.parser;

import com.seuprojeto.model.Query;

import java.util.*;
import java.util.regex.*;

public class Parser {

    private static final Pattern QUERY_PATTERN = Pattern.compile(
        "^SELECT\\s+(.*?)\\s+FROM\\s+(\\w+)(?:\\s+WHERE\\s+(.+))?$",
        Pattern.CASE_INSENSITIVE
    );

    public static Query parse(String input) {

        if (input == null || input.trim().isEmpty()) {
            throw new RuntimeException("Consulta vazia");
        }

        Matcher matcher = QUERY_PATTERN.matcher(input.trim());

        if (!matcher.matches()) {
            throw new RuntimeException("Formato de consulta inválido");
        }

        Query query = new Query();

        // Campos
        String camposStr = matcher.group(1);
        String[] camposArray = camposStr.split(",");

        List<String> campos = new ArrayList<>();

        for (String campo : camposArray) {
            campo = campo.trim();

            if (campo.isEmpty()) {
                throw new RuntimeException("Campo inválido no SELECT");
            }

            campos.add(campo);
        }

        query.campos = campos;

        // Tabela
        query.tabela = matcher.group(2);

        // Condição
        query.condicao = matcher.group(3);

        return query;
    }
}