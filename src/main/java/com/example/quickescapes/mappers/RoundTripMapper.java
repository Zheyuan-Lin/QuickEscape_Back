package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.dao.Itinerary;
import com.example.quickescapes.dao.RoundTrip;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.web.bind.annotation.RequestParam;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Mapper
public interface RoundTripMapper {
    List<RoundTrip> findRoundTrip(@Param("arrival")LocalDate arrival, 
                                 @Param("departure")LocalDate departure, 
                                 @Param("budget")BigDecimal budget,
                                  @Param("budget")String attribute);


}
