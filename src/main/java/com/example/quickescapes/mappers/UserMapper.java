package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface UserMapper {
    void registerUser(@Param("username") String username, 
                      @Param("password") String password, 
                      @Param("email") String email);

    User findUserByUsername(@Param("username") String username);

    User authenticateUser(@Param("username") String username, 
                          @Param("password") String password);
}
