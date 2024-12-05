package com.example.quickescapes.service;

import com.example.quickescapes.dao.User;

public interface UserService {
    User findByUsername(String username);
    User registerUser(String username, String password);
    User loginUser(String username, String password);
}