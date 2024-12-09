package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.CityItineraryVO;
import com.example.quickescapes.dao.Hotel;
import com.example.quickescapes.dao.Itinerary;
import com.example.quickescapes.dao.RoundTrip;
import com.example.quickescapes.mappers.HotelMapper;
import com.example.quickescapes.mappers.ItineraryMapper;
import com.example.quickescapes.mappers.RoundTripMapper;
import com.example.quickescapes.service.ItineraryService;
import com.example.quickescapes.service.RoundTripService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class ItineraryServiceImpl implements ItineraryService {
    @Autowired
    ItineraryMapper mapper;

    @Autowired
    HotelMapper hotel;

    @Autowired
    RoundTripMapper round;


    @Override
    public List<CityItineraryVO> findItinerary(LocalDate arrival, LocalDate departure, BigDecimal budget, List<String> attribute) {
        List<Hotel> hotels = hotel.getHotelList(budget, arrival, departure, attribute);
        List<RoundTrip> rounds = round.findRoundTrip(arrival, departure, budget, attribute);
        // Group itineraries by city code
        Map<String, List<RoundTrip>> roundByCity = rounds.stream()
                .collect(Collectors.groupingBy(RoundTrip::getCityCode));

        Map<String, List<Hotel>> hotelsList = hotels.stream()
                .collect(Collectors.groupingBy(Hotel::getDestination));

        List<CityItineraryVO> cityItineraries = new ArrayList<>();
        for (String cityCode : roundByCity.keySet()) {
            CityItineraryVO cityItineraryVO = new CityItineraryVO();
            cityItineraryVO.setCityCode(cityCode);

            List<RoundTrip> cityRoundTrips = roundByCity.getOrDefault(cityCode, new ArrayList<>());
            cityItineraryVO.setRoundTrips(cityRoundTrips);

            // Add hotels for this city (if any exist)
            List<Hotel> cityHotels = hotelsList.getOrDefault(cityCode, new ArrayList<>());
            cityItineraryVO.setHotels(cityHotels);

            cityItineraries.add(cityItineraryVO);
        }
        return cityItineraries;
    }


}
