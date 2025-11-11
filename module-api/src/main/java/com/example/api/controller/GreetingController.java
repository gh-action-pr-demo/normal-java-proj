package com.example.api.controller;

import com.example.common.model.Greeting;
import com.example.service.GreetingService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class GreetingController {

    private final GreetingService greetingService;

    public GreetingController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/api/greet")
    public ResponseEntity<Greeting> greet(@RequestParam(name = "name", required = false) String name) {
        Greeting greeting = greetingService.greet(name);
        return ResponseEntity.ok(greeting);
    }
}
