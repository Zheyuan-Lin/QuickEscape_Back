package com.example.quickescapes.controller;
import com.example.quickescapes.dao.CityItineraryVO;
import com.example.quickescapes.dao.Fare;
import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.dao.RoundTrip;
import com.example.quickescapes.service.FareService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("/oneway")
public class OnewayController {
    @Autowired
    private FareService fareService;

    @GetMapping("/atl")
    public ResponseEntity<List<RoundTrip>> getFaresFromAtlWithinBudget(@RequestParam LocalDate arrival,
                                                                       @RequestParam BigDecimal budget) {
        List<RoundTrip> results = fareService.getOneway(arrival,budget);
        if (results.isEmpty()) {
            return ResponseEntity.noContent().build();
        }

        return ResponseEntity.ok(results);
    }
}