package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.User;

import java.time.LocalDateTime;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface UserMapper {
    void registerUser(@Param("username") String username,
                      @Param("email") String email,
                      @Param("hashedPassword") String password);

    User findUserByUsername(@Param("name") String name);

    void add(@Param("username") String username,
             @Param("hashedPassword") String hashedPassword);

    User authenticateUser(@Param("username") String username,
                          @Param("password") String password);

    void update(User user);

    void updatePassword(@Param("hashedPassword") String hashedPassword, @Param("id") Integer id, @Param("time") LocalDateTime time);

    User findUserByEmail(@Param("email")String email);

}

