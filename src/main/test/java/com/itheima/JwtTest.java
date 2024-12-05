package com.itheima;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import org.junit.jupiter.api.Test;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class JwtTest {

    @Test
    public void testGen() {
        Map<String, Object> claims = new HashMap<>();
        claims.put("id", 1); // Add an "id" claim with value 1
        claims.put("username", "Emily"); // Add a "username" claim with value "Emily"

        // Generate the JWT token
        String token = JWT.create()
                .withClaim("user", claims) // Add the claims to the token under the "user" key
                .withExpiresAt(new Date(System.currentTimeMillis() + 1000 * 60 * 60 * 12)) // Set expiration time to 12 hours from now
                .sign(Algorithm.HMAC256("itheima")); // Sign the token using the HMAC256 algorithm and a secret key "itheima"

        System.out.println(token);
    }
}