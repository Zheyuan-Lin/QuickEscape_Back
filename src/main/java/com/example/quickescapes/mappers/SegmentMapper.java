package com.example.quickescapes.mappers;

import com.example.quickescapes.dao.Segment;
import org.apache.ibatis.annotations.Mapper;

import java.util.List;
import org.apache.ibatis.annotations.Mapper;
@Mapper
public interface SegmentMapper {
    List<Segment> findAll();

    Segment findById(Integer id);
}
