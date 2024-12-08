package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.mappers.HotelMapper;
import com.example.quickescapes.mappers.ItineraryMapper;
import com.example.quickescapes.service.HotelsService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
@Service
public class HotelServiceImpl implements HotelsService {
    @Autowired
    HotelMapper mapper;
    @Override
    public List<Hotel> searchHotels(BigDecimal budget, LocalDate checkIn, LocalDate checkOut, List<String> attribute) {
        return mapper.getHotelList(budget, checkIn, checkOut, attribute);
    }
}
