package com.example.quickescapes.service;

import com.example.quickescapes.dao.HotelQueries;
import org.springframework.stereotype.Service;


public interface HotelsService {
     String searchHotels(HotelQueries hotels);
}
