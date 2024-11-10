package com.example.quickescapes.mappers;
import com.example.quickescapes.dao.Connection;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
@Mapper
public interface ConnectionMapper {
    List<Connection> findAll();
    Connection findById(Integer connectionId);
    // Other method declarations
}
