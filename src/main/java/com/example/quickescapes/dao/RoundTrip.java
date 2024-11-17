package com.example.quickescapes.dao;

import lombok.Getter;
import lombok.Setter;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

@Getter
@Setter
public class RoundTrip {
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
}
