package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.*;
import com.example.quickescapes.mappers.FareMapper;
import com.example.quickescapes.service.FareService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class FareServiceImpl implements FareService {
    @Autowired
    private FareMapper fareMapper;
    @Override
    public List<Fare> getFaresFromAtlWithinBudget(BigDecimal budget) {
        return fareMapper.findDestinationsWithinBudget(budget);
    }

    @Override
    public List<RoundTrip> getOneway(LocalDate arrival, BigDecimal budget) {
        return fareMapper.findOneway(arrival,budget);
    }

    @Override
    public List<CityItineraryVO> getOneItinerary(LocalDate arrival, BigDecimal budget) {
        return null;
    }




}