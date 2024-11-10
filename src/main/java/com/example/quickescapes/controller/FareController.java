package com.example.quickescapes.controller;
import com.example.quickescapes.dao.Fare;
import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.service.FareService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.util.List;

@RestController
@RequestMapping("/api/fares")
public class FareController {
@Autowired
private FareService fareService;

@GetMapping("/from-atl")
public ResponseEntity<List<Fare>> getFaresFromAtlWithinBudget(@RequestParam BigDecimal budget) {
    List<Fare> results = fareService.getFaresFromAtlWithinBudget(budget);
    if (results.isEmpty()) {
        return ResponseEntity.noContent().build();
    }
    
    return ResponseEntity.ok(results);
    }
}
