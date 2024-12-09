package com.example.quickescapes.dao;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
import java.sql.Timestamp;
import java.time.LocalDate;

@Getter
@Setter
public class Hotel {
    private String destination;
    private String hotelName;
    private BigDecimal totalPrice;
    private LocalDate finalCheckInDate;
    private LocalDate finalCheckOutDate;
    private String photoUrl;
//    private double longitude;
//    private double latitude;
//    private BigDecimal reviewScore;
//    private int reviewCount;
    private String attributes;

}