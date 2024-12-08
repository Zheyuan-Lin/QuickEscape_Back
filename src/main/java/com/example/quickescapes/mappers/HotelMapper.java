package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Hotel;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Mapper
public interface HotelMapper {
    List<Hotel> getHotelList(@Param("budget") BigDecimal budget,
                             @Param("checkIn")LocalDate checkIn,
                             @Param("checkOut")LocalDate checkOut,
                             @Param("attribute")List<String> attribute);
}
