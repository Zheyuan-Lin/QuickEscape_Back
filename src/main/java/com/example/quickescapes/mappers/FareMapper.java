package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Fare;
import org.apache.ibatis.annotations.Mapper;

import java.math.BigDecimal;
import java.util.List;
@Mapper
public interface FareMapper {
    List<Fare> findDestinationsWithinBudget(BigDecimal budget);
}

