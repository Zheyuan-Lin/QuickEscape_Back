package com.example.quickescapes.controller;

import com.example.quickescapes.dao.Segment;
import com.example.quickescapes.service.SegmentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/segments")
public class SegmentController {

    @Autowired
    private SegmentService segmentService;

    @GetMapping
    public List<Segment> getAllSegments() {
        return segmentService.getAllSegments();
    }

    @GetMapping("/{id}")
    public Segment getSegmentById(@PathVariable Integer id) {
        return segmentService.getSegmentById(id);
    }
}
