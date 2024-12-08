package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.RoundTrip;
import com.example.quickescapes.mappers.RoundTripMapper;
import com.example.quickescapes.service.RoundTripService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@Service
public class RoundTripServiceImpl implements RoundTripService {

    @Autowired
    private RoundTripMapper mapper;

    @Override
    public List<RoundTrip> findRoundTrip(LocalDate arrival, LocalDate departure, BigDecimal budget, List<String> attribute) {
        return mapper.findRoundTrip(arrival, departure, budget, attribute);
    }
}
