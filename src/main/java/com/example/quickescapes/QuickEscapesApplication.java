package com.example.quickescapes;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
@MapperScan("com.example.mapper")

public class QuickEscapesApplication {

    public static void main(String[] args) {
        SpringApplication.run(QuickEscapesApplication.class, args);
    }

}
