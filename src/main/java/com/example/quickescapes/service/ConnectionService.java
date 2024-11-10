package com.example.quickescapes.service;

import com.example.quickescapes.dao.Connection;
import org.springframework.stereotype.Service;

import java.util.List;


public interface ConnectionService
{
    List<Connection> getAllConnections();
    Connection getConnectionById(Integer id);


}
