package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.dao.HotelQueries;
import com.example.quickescapes.mappers.HotelMapper;
import com.example.quickescapes.service.HotelsService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Service
public class HotelsServiceImpl implements HotelsService {

    private static final Logger logger = LoggerFactory.getLogger(HotelsServiceImpl.class);

    @Autowired
    HotelMapper mapper;


    @Override
    public List<Hotel> searchHotels(Integer budget, LocalDate checkIn, LocalDate checkOut) {
        logger.info("Searching hotels with budget: {}, checkIn: {}, checkOut: {}", 
            budget, checkIn, checkOut);
            
        List<Hotel> results = mapper.searchHotels(budget, checkIn, checkOut);
        
        logger.info("Found {} hotels matching criteria", results != null ? results.size() : 0);
        return results;
    }
}
