package com.example.quickescapes.controller;

import com.example.quickescapes.service.FlightsService;
import com.example.quickescapes.dao.FlightsQueries;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/flights")
public class FlightsController {
    @Autowired
    FlightsService flights;
    @GetMapping(value = "/oneway")
    public ResponseEntity<String> searchOneWay(@RequestBody FlightsQueries flightsQueried) {
        String result = flights.searchFlightsOneWay(flightsQueried);
        if (result != null) {
            return ResponseEntity.ok(result);
        } else {
            return new ResponseEntity<>("Error searching for flights.", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    @GetMapping(value = "/roundway")
    public ResponseEntity<String> searchRoundWay(@RequestBody FlightsQueries flightsQueried) {
        String result = flights.searchFlightsRoundTrip(flightsQueried);
        if (result != null) {
            return ResponseEntity.ok(result);
        } else {
            return new ResponseEntity<>("Error searching for flights.", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("/airport")
    public ResponseEntity<String> searchAirport(@RequestParam(value = "query") String airportCode) {
        String result = flights.searchAirport(airportCode);
        if (result != null) {
            return ResponseEntity.ok(result);
        } else {
            return new ResponseEntity<>("Error searching for flights.", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}