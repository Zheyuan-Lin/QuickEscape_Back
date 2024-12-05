package com.example.quickescapes.serviceimpl;

import com.example.quickescapes.dao.User;
import com.example.quickescapes.mappers.UserMapper;
import com.example.quickescapes.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public User findByUsername(String username){
        User u = userMapper.findByUsername(username);
        return u;
    }

    @Override
    public User registerUser(String username, String password) {
        // Hash the password using BCrypt
        String hashedPassword = passwordEncoder.encode(password);

        userMapper.add(username, hashedPassword);
    }

    @Override
    public User loginUser(String username, String password) {
        User user = userRepository.findByUsername(username);
        if (user == null || !passwordEncoder.matches(password, user.getPassword())) {
            throw new RuntimeException("Invalid username or password");
        }
        return user;
    }
}