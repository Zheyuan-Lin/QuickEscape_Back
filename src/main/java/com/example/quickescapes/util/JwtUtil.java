package com.example.quickescapes.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;

import java.util.Date;
import java.util.Map;

public class JwtUtil {

    private static final String KEY = "itheima"; // Secret key for HMAC signing

    // Method to generate a JWT token
    public static String genToken(Map<String, Object> claims) {
        return JWT.create()
                .withClaim("claims", claims) // Add the claims as a payload
                .withExpiresAt(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 12)) // Set expiration time to 12 hours
                .sign(Algorithm.HMAC256(KEY)); // Sign the token with HMAC256 and the secret key
    }

    // Method to parse and validate a JWT token
    public static Map<String, Object> parseToken(String token) {
        return JWT.require(Algorithm.HMAC256(KEY)) // Specify the algorithm and key for verification
                .build() // Build the JWT verifier
                .verify(token) // Verify the provided token
                .getClaim("claims") // Retrieve the "claims" payload
                .asMap(); // Convert the claims to a Map
    }
}