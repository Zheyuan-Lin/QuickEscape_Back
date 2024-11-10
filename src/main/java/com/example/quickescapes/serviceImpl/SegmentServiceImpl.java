package com.example.quickescapes.serviceImpl;

import com.example.quickescapes.dao.Segment;
import com.example.quickescapes.mappers.SegmentMapper;
import com.example.quickescapes.service.SegmentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class SegmentServiceImpl implements SegmentService {
    @Autowired
    private SegmentMapper segmentMapper;

    @Override
    public List<Segment> getAllSegments() {
        return segmentMapper.findAll();
    }

    @Override
    public Segment getSegmentById(Integer id) {
        return segmentMapper.findById(id);
    }
}
