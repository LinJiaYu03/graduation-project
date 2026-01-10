package com.example.projectsystem.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.example.projectsystem.domain.User;
import com.example.projectsystem.dto.ProfileUpdateRequest;

public interface UserService extends IService<User> {
    /**
    * 用户注册
    */
    User register(String username, String password);

    /**
    * 用户登录
    */
    User login(String username, String password);

    /**
    * 微信登录
    */
    User wxLogin(String code);

    /**
    * 完善个人信息
    */
    User completeProfile(Long userId, ProfileUpdateRequest request);
}
