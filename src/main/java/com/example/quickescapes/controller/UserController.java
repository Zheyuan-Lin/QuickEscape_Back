package com.example.quickescapes.controller;

import com.example.quickescapes.dao.User;
import com.example.quickescapes.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/register")
    public String registerUser(@RequestBody User user) {
        userService.registerUser(user.getUsername(), user.getPassword());
        return "User registered successfully!";
    }

    @PostMapping("/login")
    public String loginUser(@RequestBody User user) {
        userService.loginUser(user.getUsername(), user.getPassword());
        return "Login successful!";
    }
}
