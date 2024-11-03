package com.example.quickescapes.service;

import com.example.quickescapes.dao.Connection;

import java.util.List;

public interface ConnectionService
{
    public List<Connection> getAllConnections();
    public Connection getConnectionById(Integer id);


}
