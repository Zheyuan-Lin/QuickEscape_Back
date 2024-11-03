package com.example.quickescapes.controller;

import com.example.quickescapes.dao.Connection;
import com.example.quickescapes.service.ConnectionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/connections")
public class ConnectionController {

    @Autowired
    private ConnectionService connectionService;

    @GetMapping
    public List<Connection> getAllConnections() {
        return connectionService.getAllConnections();
    }

    @GetMapping("/{id}")
    public Connection getConnectionById(@PathVariable Integer id) {
        return connectionService.getConnectionById(id);
    }
}

