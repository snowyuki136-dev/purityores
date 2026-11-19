package com.example.purityores;

public enum Tier {
    POOR("poor"), NORMAL("normal"), RICH("rich");

    public final String id;

    Tier(String id) {
        this.id = id;
    }
}
