package com.example.service;

import com.example.common.model.Greeting;
import com.example.common.util.MessageFormatter;
import org.springframework.stereotype.Service;

@Service
public class GreetingService {

    public Greeting greet(String name) {
        String normalized = MessageFormatter.normalize(name);
        return Greeting.builder()
                .message(String.format("Hello, %s!", normalized))
                .language("en")
                .build();
    }
}
