package com.seuprojeto.controller;

import com.seuprojeto.model.Query;
import com.seuprojeto.parser.Parser;
import com.seuprojeto.validator.Validador;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/query")
@CrossOrigin(origins = "*")
public class QueryController {

    @PostMapping
    public ResponseEntity<?> processar(@RequestBody String consulta) {

        try {
            Query q = Parser.parse(consulta);
            Validador.validar(q);

            return ResponseEntity.ok(q);

        } catch (RuntimeException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        }
    }
}