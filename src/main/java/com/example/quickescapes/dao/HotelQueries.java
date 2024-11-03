package com.example.quickescapes.dao;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class HotelQueries {
   public String location;
   public String checkIn;
    public String checkOut;
    public int pageNumber;
    public int adults;
    public String currencyCode;
    public int rooms;

}
