package com.example.quickescapes.dao;

import lombok.Getter;

import java.time.LocalDateTime;

@Getter
public class Segment {
    private Integer segmentId;
    private String airlineCd;
    private Integer flightNb;
    private String departureAirportCd;
    private String arrivalAirportCd;
    private LocalDateTime departureDt;
    private LocalDateTime arrivalDt;
    private String aircraft;
}
