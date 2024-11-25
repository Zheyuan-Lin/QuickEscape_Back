package com.example.quickescapes.dao;

import lombok.Getter;
import lombok.Setter;

import javax.persistence.*;

@Getter
@Setter
@Entity
@Table(name = "users")
public class User {
    @Column(nullable = false, unique = true)
    private String username;
    
    @Column(nullable = false)
    private String password;
}