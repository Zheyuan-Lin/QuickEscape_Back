package com.example.quickescapes.dao;

import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
public class CityItineraryVO {
    private String cityCode;
    private List<RoundTrip> roundTrips;
    private List<Hotel> hotels;

}
