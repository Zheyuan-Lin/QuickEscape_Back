package com.example.quickescapes.dao;

public enum Attribute {
    CULTURE,
    CITY,
    RESORT,
    TECH,
    COASTAL,
    FOODIE,
    SHOPPING,
    HISTORY,
    NATURE;

    // Optional: Add a method to display attributes
    public static void displayAttributes() {
        for (Attribute attribute : Attribute.values()) {
            System.out.println(attribute);
        }
    }
}
