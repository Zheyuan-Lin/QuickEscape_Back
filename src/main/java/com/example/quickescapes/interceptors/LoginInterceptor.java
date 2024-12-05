package com.example.quickescapes.interceptors;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class LoginInterceptor implements HandlerInterceptor {

    public boolean preHandle (HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        return false;
    }

}
