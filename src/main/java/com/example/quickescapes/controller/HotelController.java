package com.example.quickescapes.controller;

import com.example.quickescapes.dao.CityItineraryVO;
import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.service.HotelsService;

import com.example.quickescapes.util.Exception.ErrorCode;
import com.example.quickescapes.util.ResponseEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
@RestController
@RequestMapping("hotel")
public class HotelController {

    @Autowired
    HotelsService service;

    @RequestMapping("/find")
    public ResponseEntity<List<Hotel>> findRoundTrip(@RequestParam LocalDate checkin,
                                               @RequestParam LocalDate checkout,
                                               @RequestParam BigDecimal budget) {
        List<Hotel> results =  service.searchHotels(budget, checkin, checkout);
        if (results.isEmpty()) {
            ErrorCode error = new ErrorCode(100,"No hotel");
            return ResponseEntity.error(error);
        }

        return ResponseEntity.success(results);
    }
}

