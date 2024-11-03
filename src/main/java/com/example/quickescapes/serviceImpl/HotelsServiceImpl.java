package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.HotelQueries;
import com.example.quickescapes.service.HotelsService;
import org.springframework.stereotype.Service;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

@Service
public class HotelsServiceImpl implements HotelsService {

    public List<String> searchLocation(String location) {
        String url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/searchLocation?query=" +
                location;
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("x-rapidapi-key", "4ca5b33aaamsh8b13abf5343cf72p18d5e3jsn1c45965abdcf")
                .header("x-rapidapi-host", "tripadvisor16.p.rapidapi.com")
                .method("GET", HttpRequest.BodyPublishers.noBody())
                .build();
        HttpResponse<String> response;
        ArrayList<String> geoIds = new ArrayList<String>();
        try {
            response = HttpClient.newHttpClient().send(request, HttpResponse.BodyHandlers.ofString());
            JSONObject jsonResponse = new JSONObject(response.body());

            if (jsonResponse.getBoolean("status")) {
                JSONArray dataArray = jsonResponse.getJSONArray("data");

                for (int i = 0; i < dataArray.length(); i++) {
                    JSONObject locationData = dataArray.getJSONObject(i);
                    int geoId = locationData.getInt("geoId");

                    geoIds.add(String.valueOf(geoId));
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return geoIds;
    }


    @Override
    public String searchHotels(HotelQueries hotels) {

       List<String> locationId = searchLocation(hotels.location);

        String url = "https://tripadvisor16.p.rapidapi.com/api/v1/hotels/getHotelsFilter?geoId=" +
                locationId.get(0) +
                "&checkIn=" + hotels.getCheckIn() +
                "&checkOut=" + hotels.getCheckOut() +
                "&pageNumber=" + hotels.getPageNumber() +
                "&rooms=" + hotels.getRooms() +
                "&currencyCode=" + hotels.getCurrencyCode();

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
