package com.example.quickescapes.service;

import com.example.quickescapes.dao.Fare;

import java.math.BigDecimal;
import java.util.List;

public interface FareService {
    List<Fare> getFaresFromAtlWithinBudget(BigDecimal budget);
}
