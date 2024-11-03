package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.FlightsQueries;
import com.example.quickescapes.service.FlightsService;

import org.springframework.stereotype.Service;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@Service
public class FlightsServiceImpl implements FlightsService {


    private static String XRapidAPIKey = "4ca5b33aaamsh8b13abf5343c172p18d5e3jsn1c45965abdcf";
    private static final String RAPID_API_HOST = "rapidapi.com";
    private static final String SORT_ORDER = "ML_BEST_VALUE";
    private static final String ONE_WAY = "ONE_WAY";
    private static final String ROUND_WAY = "ROUND_TRIP";
    private static final int NUM_SENIORS = 0;
    private static final String CLASS_OF_SERVICE = "ECONOMY";
    private static final int PAGE_NUMBER_FLIGHTS = 1;
    private static final String NONSTOP = "yes";
    private static final String CURRENCY_CODE = "USD";

    public String searchFlightsOneWay(FlightsQueries flights) {
        String url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights" +
                "?sourceAirportCode=" + flights.getSourceAirportCode() +
                "&destinationAirportCode=" + flights.getDestinationAirportCode() +
                "&date=" + flights.getDate() +
                "&itineraryType=ONE_WAY"  +
                "&sortOrder=" + flights.getSortOrder() +
                "&numAdults=" + flights.getNumAdults() +
                "&numSeniors=" + flights.getNumSeniors() +
                "&classOfService=" + flights.getClassOfService() +
                "&pageNumber=" + flights.getPageNumber() +
                "&nonstop=" + flights.getNonstop() +
                "&currencyCode=" + flights.getCurrencyCode();

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("x-rapidapi-key", "4ca5b33aaamsh8b13abf5343cf72p18d5e3jsn1c45965abdcf")
                .header("x-rapidapi-host", "tripadvisor16.p.rapidapi.com")
                .method("GET", HttpRequest.BodyPublishers.noBody())
                .build();


        HttpResponse<String> response;
        try {
            response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
            return response.body();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return null;
        }
    }

    public String searchFlightsRoundTrip(FlightsQueries flights) {
            String url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights" +
                    "?sourceAirportCode=" + flights.getSourceAirportCode() +
                    "&destinationAirportCode=" + flights.getDestinationAirportCode() +
                    "&date=" + flights.getDate() +
                    "&itineraryType=" + ROUND_WAY +
                    "&sortOrder=" + flights.getSortOrder() +
                    "&numAdults=" + flights.getNumAdults() +
                    "&numSeniors=" + flights.getNumSeniors() +
                    "&classOfService=" + flights.getClassOfService() +
                    "&pageNumber=" + flights.getPageNumber() +
                    "&nonstop=" + flights.getNonstop() +
                    "&currencyCode=" + flights.getCurrencyCode() +
                    "&returnDate=" + flights.getReturnDate()+
                    "&region=USA";

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .header("x-rapidapi-key", XRapidAPIKey)
                    .header("x-rapidapi-host", "tripadvisor16.p.rapidapi.com")
                    .method("GET", HttpRequest.BodyPublishers.noBody())
                    .build();

        HttpResponse<String> response;
        try {
            response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
            return response.body();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return null;
        }
    }

    public String searchAirport(String airportCode) {
        String url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport" +
                "?query=" + airportCode;

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("x-rapidapi-key", "4ca5b33aaamsh8b13abf5343cf72p18d5e3jsn1c45965abdcf")
                .header("x-rapidapi-host", "tripadvisor16.p.rapidapi.com")
                .method("GET", HttpRequest.BodyPublishers.noBody())
                .build();

        HttpResponse<String> response;
        try {
            response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
            return response.body();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return null;
        }
    }

}
