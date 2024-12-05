package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.User;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface UserMapper {
    void registerUser(@Param("id") Integer id,
<<<<<<< HEAD
                      @Param("username") String username,
                      @Param("password") String password,
=======
                      @Param("username") String username, 
                      @Param("password") String password, 
>>>>>>> origin/master
                      @Param("email") String email);

    User findUserByUsername(@Param("username") String username);

    void add(@Param("username") String username,
             @Param("hashedPassword") String hashedPassword);

<<<<<<< HEAD
    User authenticateUser(@Param("username") String username,
                          @Param("password") String password);
}
=======
    User authenticateUser(@Param("username") String username, 
                          @Param("password") String password);
}
>>>>>>> origin/master
