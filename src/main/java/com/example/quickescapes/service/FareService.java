package com.example.quickescapes.service;

import com.example.quickescapes.dao.CityItineraryVO;
import com.example.quickescapes.dao.Fare;
import com.example.quickescapes.dao.RoundTrip;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

public interface FareService {
    List<Fare> getFaresFromAtlWithinBudget(BigDecimal budget);

    List<RoundTrip> getOneway(LocalDate arrival, BigDecimal budget);

    List<CityItineraryVO> getOneItinerary(LocalDate arrival, BigDecimal budget);

}
