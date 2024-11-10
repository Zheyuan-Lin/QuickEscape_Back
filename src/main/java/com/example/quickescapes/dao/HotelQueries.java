package com.example.quickescapes.dao;

import lombok.Getter;
import lombok.Setter;

import java.time.LocalDate;

@Getter
@Setter
public class HotelQueries {
   public LocalDate checkIn;
    public LocalDate checkOut;
    public int budget;

}
