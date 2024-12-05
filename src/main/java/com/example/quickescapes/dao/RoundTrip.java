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
    private String outboundFlightNumbers;
    private String outboundCabin;

    private LocalDateTime returnDepartureDate;
    private BigDecimal returnPrice;
    private String returnFlightNumbers;
    private String returnCabin;

    private BigDecimal flightTotalPrice;
}
