package com.example.quickescapes.service;

import com.example.quickescapes.dao.User;

public interface UserService {
    User findByUsername(String username);
    void registerUser(String username, String password);
    void loginUser(String username, String password);
}