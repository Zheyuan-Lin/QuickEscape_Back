package com.example.quickescapes.service;

import com.example.quickescapes.dao.RoundTrip;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

public interface RoundTripService {
    List<RoundTrip> findRoundTrip(LocalDate arrival, LocalDate departure, BigDecimal budget);
}
