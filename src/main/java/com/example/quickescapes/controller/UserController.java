package com.example.quickescapes.controller;

import com.example.quickescapes.dao.User;
import com.example.quickescapes.service.UserService;
import com.example.quickescapes.util.Exception.ErrorCode;
import com.example.quickescapes.util.ResponseEntity;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import java.util.*;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @PostMapping("/register")
    public ResponseEntity<String> registerUser(@RequestBody User user) {
        if (user.getUsername() != null && user.getUsername().length() <= 16 
            && user.getPassword() != null && user.getPassword().length() <= 16){
            User u = userService.findByUsername(user.getUsername());
            // Check if username already exists
            if (u = null){
                userService.registerUser(user.getUsername(), user.getPassword());
                return ResponseEntity.success("User registered successfully!");
            }else{
                return ResponseEntity.error(new ErrorCode(101, "The username is already taken."));
            }
        }else{
            return ResponseEntity.error(new ErrorCode(102, "The username or password is illegal."));
        }
    }

    @PostMapping("/login")
    public ResponseEntity<String> loginUser(@RequestBody User user) {
        // Check if the user exists
        User loginUser = userService.findByUsername(user.getUsername());
        if (loginUser == null){
            return ResponseEntity.error(new ErrorCode(103, "The username is invalid."));
        }

        // Check if the password is correct
        if (!passwordEncoder.matches(user.getPassword(), loginUser.getPassword())){
            Map<String, Object> claims = new HashMap<>(); 
            claims.put("id", loginUser.getId());
            claims.put("username", loginUser.getUsername()); 
            String token = JwtUtil.genToken(claims); 
            return ResponseEntity.ok(token);
        }

        return ResponseEntity.error(new ErrorCode(104, "The password is incorrect."));
        }
}
