package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.dao.HotelQueries;
import org.apache.ibatis.annotations.Mapper;

import java.time.LocalDate;
import java.util.List;

@Mapper
public interface HotelMapper {

    List<Hotel> searchHotels(Integer budget, LocalDate checkIn, LocalDate checkOut);
}
