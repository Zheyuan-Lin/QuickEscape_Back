package com.example.quickescapes.dao;

import lombok.Getter;

@Getter
public class Connection {
    private Integer connectionId;
    private Integer sliceId;
    private String airportCd;
    private Integer duration;
    private Boolean changeTerminal;
    private Boolean changeAirport;
    // Getters and setters
}