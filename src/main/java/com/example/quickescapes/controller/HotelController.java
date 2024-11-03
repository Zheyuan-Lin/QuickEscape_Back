package com.example.quickescapes.controller;


import com.example.quickescapes.dao.HotelQueries;
import com.example.quickescapes.service.HotelsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@CrossOrigin()
@RequestMapping("/hotels")
public class HotelController {

    @Autowired
    HotelsService hotels;

    @GetMapping(value = "/search")
    public ResponseEntity<String> searchRoundWay(@RequestBody HotelQueries hotelQuery) {
        String result = hotels.searchHotels(hotelQuery);
        if (result != null) {
            return ResponseEntity.ok(result);
        } else {
            return new ResponseEntity<>("Error searching for hotels.", HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}
