package com.example.quickescapes.serviceImpl;
import com.example.quickescapes.mappers.UserMapper;
import com.example.quickescapes.service.UserService;
import com.example.quickescapes.util.ThreadLocalUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import com.example.quickescapes.dao.User;

import java.time.LocalDateTime;
import java.util.Map;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserMapper userMapper;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @Override
    public User findByUsername(String name){
        User u = userMapper.findUserByUsername(name);
        return u;
    }

    @Override
    public User registerUser(String username, String email, String password) {
        // Hash the password using BCrypt
        String hashedPassword = passwordEncoder.encode(password);

        userMapper.registerUser(username, email, hashedPassword);
        return userMapper.findUserByUsername(username);
    }

    @Override
    public User loginUser(String username, String password) {
        User user = userMapper.findUserByUsername(username);
        if (user == null || !passwordEncoder.matches(password, user.getPassword())) {
            throw new RuntimeException("Invalid username or password");
        }
        return user;
    }

    @Override
    public void update(User user) {
        userMapper.update(user);
    }

    @Override
    public void updatePassword(String newPassword) {
        String hashedPassword = passwordEncoder.encode(newPassword);
        Map<String, Object> claim = ThreadLocalUtil.get();
        
        // Ensure the ID is treated as an Integer
        Integer id = (Integer) claim.get("id"); // Cast to Integer if necessary
        LocalDateTime time = LocalDateTime.now();
        userMapper.updatePassword(hashedPassword, id, time); // Pass as Integer
    }

    @Override
    public User findByEmail(String email) {
        return userMapper.findUserByEmail(email);
    }
}