package com.example.quickescapes.dao;
import lombok.Getter;

import java.math.BigDecimal;

@Getter
public class Fare {
    private int fareId;
    private int tripId;
    private String airlineCd;
    private String departureCityCd;
    private String arrivalCityCd;
    private String fareCd;
    private String tag;
    private BigDecimal price;

}