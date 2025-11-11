package com.example.common.util;

import org.apache.commons.lang3.StringUtils;

public final class MessageFormatter {

    private MessageFormatter() {
    }

    public static String normalize(String message) {
        if (StringUtils.isBlank(message)) {
            return "Hello";
        }
        return StringUtils.capitalize(message.trim());
    }
}
