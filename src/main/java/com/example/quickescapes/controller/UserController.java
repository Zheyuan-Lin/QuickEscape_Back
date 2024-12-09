package com.example.quickescapes.controller;

import com.example.quickescapes.dao.User;
import com.example.quickescapes.service.UserService;
import com.example.quickescapes.util.Exception.ErrorCode;
import com.example.quickescapes.util.ResponseEntity;
import com.example.quickescapes.util.ThreadLocalUtil;

import org.apache.catalina.connector.Response;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import java.util.*;
import com.example.quickescapes.util.JwtUtil;

@RestController
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    @PostMapping("/register")
    public ResponseEntity<String> registerUser(@RequestBody User user) {
        if (user.getUsername() != null && user.getUsername().length() <= 16
                && user.getPassword() != null && user.getPassword().length() <= 20
                && user.getEmail() != null && user.getEmail().contains("@")){
            User u = userService.findByUsername(user.getUsername());
            // Check if username already exists
            if (u == null){
                userService.registerUser(user.getUsername(), user.getEmail(), user.getPassword());
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
        if (passwordEncoder.matches(user.getPassword(), loginUser.getPassword())){
            Map<String, Object> claims = new HashMap<>();
            claims.put("id", loginUser.getId());
            claims.put("username", loginUser.getUsername());
            // generate the token
            String token = JwtUtil.genToken(claims);
            System.out.println(token);
            return ResponseEntity.success(token);
        }

        return ResponseEntity.error(new ErrorCode(104, "The password is incorrect."));
    }

    
    @GetMapping("/userInfo")
    public ResponseEntity<User> userInfo() {
        Map<String, Object> claim =ThreadLocalUtil.get();
        String userName = (String) claim.get("email");
        User user = userService.findByUsername(userName);
        return ResponseEntity.success(user);

    }


    @PatchMapping("/updatepsw")
    public ResponseEntity<User> update(@RequestBody Map<String, String> params) {
        String oldPassword = params.get("oldPassword");
        String newPassword = params.get("newPassword");
        String rePassword = params.get("rePassword");

        if (StringUtils.isEmpty(oldPassword) || StringUtils.isEmpty(newPassword) || StringUtils.isEmpty(rePassword)) {
            return ResponseEntity.error(new ErrorCode(105, "Password cannot be empty."));
        }

        Map<String, Object> claim = ThreadLocalUtil.get();
        String name = (String) claim.get("username");
        User user = userService.findByUsername(name);

        if (!passwordEncoder.matches(oldPassword, user.getPassword())) {
            return ResponseEntity.error(new ErrorCode(106, "Old password is incorrect."));
        }

        if (!newPassword.equals(rePassword)) {
            return ResponseEntity.error(new ErrorCode(107, "New password and re-entered password do not match."));
        }

        userService.updatePassword(newPassword);
        return ResponseEntity.success(user);
    }
}




