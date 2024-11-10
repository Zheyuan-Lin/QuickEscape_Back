package com.example.quickescapes.controller;


import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.service.HotelsService;
import org.apache.ibatis.annotations.Param;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.List;

@RestController
@CrossOrigin()
@RequestMapping("/hotels")
public class HotelController {

@Autowired
HotelsService hotels;

@GetMapping(value = "/search")
public ResponseEntity<List<Hotel>> searchHotels(
    @RequestParam("budget") int budget,
    @RequestParam("checkIn") LocalDate checkIn,
    @RequestParam("checkOut") LocalDate checkOut) {
    
    List<Hotel> results = hotels.searchHotels(budget, checkIn, checkOut);
    
    if (results.isEmpty()) {
        return ResponseEntity.noContent().build();
    }
    
    return ResponseEntity.ok(results);
    }
}
