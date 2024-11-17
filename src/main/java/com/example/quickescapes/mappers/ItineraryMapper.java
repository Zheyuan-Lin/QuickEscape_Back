package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.dao.Itinerary;
import com.example.quickescapes.dao.RoundTrip;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
@Mapper
public interface ItineraryMapper {

    // Method to build the final itinerary
    List<Itinerary> buildItinerary(@Param("checkInDate") LocalDate checkInDate,
                                   @Param("checkOutDate") LocalDate checkOutDate,
                                   @Param("budget") BigDecimal budget);
}
