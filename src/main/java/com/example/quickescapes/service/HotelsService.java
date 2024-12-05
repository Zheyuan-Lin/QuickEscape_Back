package com.example.quickescapes.service;

import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.dao.HotelQueries;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;


public interface HotelsService {
     List<Hotel> searchHotels(BigDecimal budget, LocalDate checkIn, LocalDate checkOut, String attribute);
}
