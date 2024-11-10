package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.Fare;
import com.example.quickescapes.mappers.FareMapper;
import com.example.quickescapes.service.FareService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.util.List;

@Service
public class FareServiceImpl implements FareService {
    @Autowired
    private FareMapper fareMapper;
    @Override
    public List<Fare> getFaresFromAtlWithinBudget(BigDecimal budget) {
        return fareMapper.findDestinationsWithinBudget(budget);
    }
}
