package com.example.quickescapes.dao;

import lombok.Getter;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Getter
public class Itinerary {
    private String cityCode;
    private LocalDateTime outboundDepartureDate;
    private BigDecimal outboundPrice;
    private String outboundAirline;
    private String outboundFlightNumber;
    private String outboundCabin;

    private LocalDateTime returnDepartureDate;
    private BigDecimal returnPrice;
    private String returnAirline;
    private String returnFlightNumber;
    private String returnCabin;

    private BigDecimal flightTotalPrice;
    private String hotelName;
    private BigDecimal hotelPrice;
    private LocalDate checkInDate;
    private LocalDate checkOutDate;
    private BigDecimal totalItineraryPrice;
    private String photoUrl;




}
