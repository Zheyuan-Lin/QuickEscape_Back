package com.example.quickescapes.service;

import com.example.quickescapes.dao.Segment;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface SegmentService {

    public List<Segment> getAllSegments();

    public Segment getSegmentById(Integer id);

    // Additional methods for saving, updating, and deleting segments
}

