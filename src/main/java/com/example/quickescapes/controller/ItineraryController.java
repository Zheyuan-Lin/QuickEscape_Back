package com.example.quickescapes.controller;

import com.example.quickescapes.dao.CityItineraryVO;
import com.example.quickescapes.dao.Itinerary;
import com.example.quickescapes.dao.RoundTrip;
import com.example.quickescapes.service.ItineraryService;
import com.example.quickescapes.service.RoundTripService;
import com.example.quickescapes.util.Exception.ErrorCode;
import com.example.quickescapes.util.ResponseEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
@RestController
@RequestMapping("itinerary")
public class ItineraryController {

        @Autowired
        ItineraryService service;

        @RequestMapping("/find")
        public ResponseEntity<List<CityItineraryVO>> findRoundTrip(@RequestParam LocalDate arrival,
                                                                   @RequestParam LocalDate departure,
                                                                   @RequestParam BigDecimal budget,
                                                                   @RequestParam List<String> attributes) {

            List<CityItineraryVO> results =  service.findItinerary(arrival, departure, budget, attributes);
            if (results.isEmpty()) {
                ErrorCode error = new ErrorCode(100,"No Itinerary");
                return com.example.quickescapes.util.ResponseEntity.error(error);
            }

            return ResponseEntity.success(results);
        }
    }

