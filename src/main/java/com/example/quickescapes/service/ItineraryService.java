package com.example.quickescapes.service;

import com.example.quickescapes.dao.CityItineraryVO;
import com.example.quickescapes.dao.Itinerary;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

public interface ItineraryService {

    List<CityItineraryVO> findItinerary(LocalDate arrival, LocalDate departure, BigDecimal amount, List<String>attribute);
}
