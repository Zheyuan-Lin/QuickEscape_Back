package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Segment;

import java.util.List;

public interface SegmentMapper {
    public List<Segment> findAll();

    public Segment findById(Integer id);
}
