package com.example.quickescapes.mappers;
import com.example.quickescapes.dao.Connection;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;

@Mapper
public interface ConnectionMapper {

    List<Connection> findAll();

    Connection findById(Integer connectionId);

    // Additional methods for inserting, updating, and deleting can go here
}

