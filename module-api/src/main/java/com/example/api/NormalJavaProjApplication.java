package com.example.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication(scanBasePackages = "com.example")
public class NormalJavaProjApplication {

    public static void main(String[] args) {
        SpringApplication.run(NormalJavaProjApplication.class, args);
    }
}
