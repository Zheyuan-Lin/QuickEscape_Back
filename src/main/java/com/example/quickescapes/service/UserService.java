package com.example.quickescapes.service;

import com.example.quickescapes.dao.User;

public interface UserService {
    User findByUsername(String name);
    User registerUser(String username, String email, String password);
    User loginUser(String username, String password);

    void update(User user);

    void updatePassword(String newPassword);

    User findByEmail(String email);
}