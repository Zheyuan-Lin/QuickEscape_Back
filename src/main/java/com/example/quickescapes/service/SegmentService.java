package com.example.quickescapes.service;

import com.example.quickescapes.dao.Segment;
import org.springframework.stereotype.Service;

import java.util.List;

public interface SegmentService {
    List<Segment> getAllSegments();

    Segment getSegmentById(Integer id);
}

