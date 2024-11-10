package com.example.quickescapes.dao;

import lombok.Getter;

import java.math.BigDecimal;
import java.sql.Timestamp;
import java.time.LocalDate;

@Getter
public class Hotel {
    private int id;
    private int hotelId;
    private String hotelNm;
    private LocalDate ciDate;
    private LocalDate coDate;
    private BigDecimal price;
    private double longitude;
    private double latitude;
    private BigDecimal reviewScore;
    private int reviewCount;
    private String photoUrl;

    // Constructor
}