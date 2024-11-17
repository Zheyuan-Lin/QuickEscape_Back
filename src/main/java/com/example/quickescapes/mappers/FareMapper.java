package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Fare;
import com.example.quickescapes.dao.Itinerary;
import com.example.quickescapes.dao.RoundTrip;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
@Mapper
public interface FareMapper {
    List<Fare> findDestinationsWithinBudget(BigDecimal budget);

    List<RoundTrip> findOneway(@Param("arrival") LocalDate arrival, @Param("budget") BigDecimal budget);

    List<Itinerary> getOneItinerary(@Param("arrival") LocalDate arrival, @Param("budget")BigDecimal budget);
}

