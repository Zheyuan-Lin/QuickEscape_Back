package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.Connection;
import com.example.quickescapes.mappers.ConnectionMapper;
import com.example.quickescapes.service.ConnectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
@Service
public class ConnectionServiceImpl implements ConnectionService {
    @Autowired
    private ConnectionMapper mapper;

    @Override
    public List<Connection> getAllConnections() {
        return mapper.findAll();
    }

    @Override
    public Connection getConnectionById(Integer id) {
        return mapper.findById(id);
    }
}
