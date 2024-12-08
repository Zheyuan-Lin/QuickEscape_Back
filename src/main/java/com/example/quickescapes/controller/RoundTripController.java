package com.example.quickescapes.controller;

import com.example.quickescapes.dao.RoundTrip;
import com.example.quickescapes.service.RoundTripService;
import com.example.quickescapes.util.Exception.ErrorCode;
import com.example.quickescapes.util.ResponseEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@RestController
@RequestMapping("round")
public class RoundTripController {
    @Autowired
    RoundTripService service;

    @GetMapping("/find")
    public ResponseEntity<List<RoundTrip>> findRoundTrip(@RequestParam("arrival") LocalDate arrival,
                                                         @RequestParam("departure") LocalDate departure,
                                                         @RequestParam("budget") BigDecimal budget,
                                                         @RequestParam("attribute") List<String> attribute) {
        List<RoundTrip> results = service.findRoundTrip(arrival, departure, budget, attribute);
        if (results.isEmpty()) {
            ErrorCode error = new ErrorCode(100,"No RoundTrip");
            return ResponseEntity.error(error);
        }

        return ResponseEntity.success(results);
    }
}
