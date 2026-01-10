package com.example.projectsystem.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.projectsystem.commons.PageResult;
import com.example.projectsystem.commons.Results;
import com.example.projectsystem.domain.User;
import com.example.projectsystem.dto.LoginRequest;
import com.example.projectsystem.dto.WxLoginRequest;
import com.example.projectsystem.dto.ProfileUpdateRequest;
import com.example.projectsystem.dto.RegisterRequest;
import com.example.projectsystem.service.UserService;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.util.Arrays;
import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping("/register")
    public Results register(@RequestBody RegisterRequest request) {
        try {
            User user = userService.register(request.getUsername(), request.getPassword());
            return Results.success()
                    .message("注册成功")
                    .data("userId", user.getId());
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        }
    }

    @PostMapping("/wx-login")
    public Results wxLogin(@RequestBody WxLoginRequest request) {
        try {
            User user = userService.wxLogin(request.getCode());
            return Results.success()
                    .message("登录成功")
                    .data("token", user.getToken())
                    .data("user", user);
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        }
    }

    @PostMapping("/login")
    public Results login(@RequestBody LoginRequest request) {
        try {
            User user = userService.login(request.getUsername(), request.getPassword());
            return Results.success()
                    .message("登录成功")
                    .data("token", user.getToken())
                    .data("user", user);
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        }
    }

    @GetMapping
    public Results getUserList(@RequestParam(defaultValue = "1") Integer currentPage,
                               @RequestParam(defaultValue = "10") Integer pageSize) {
        Page<User> page = new Page<>(currentPage, pageSize);
        IPage<User> pageResult = userService.page(page);
        
        PageResult<User> pageData = new PageResult<>(
                pageResult.getTotal(),
                (int) pageResult.getCurrent(),
                (int) pageResult.getSize(),
                pageResult.getRecords()
        );
        
        return Results.success()
                .message("查询成功")
                .data("page", pageData);
    }

    @GetMapping("/search")
    public Results searchUsers(@RequestParam(required = false) String keyword,
                               @RequestParam(defaultValue = "1") Integer currentPage,
                               @RequestParam(defaultValue = "10") Integer pageSize) {
        Page<User> page = new Page<>(currentPage, pageSize);
        LambdaQueryWrapper<User> queryWrapper = new LambdaQueryWrapper<>();
        
        if (StringUtils.hasText(keyword)) {
            queryWrapper.and(wrapper -> wrapper
                    .like(User::getUsername, keyword)
                    .or()
                    .like(User::getRealName, keyword)
                    .or()
                    .like(User::getStudentNo, keyword)
            );
        }
        
        IPage<User> pageResult = userService.page(page, queryWrapper);
        
        PageResult<User> pageData = new PageResult<>(
                pageResult.getTotal(),
                (int) pageResult.getCurrent(),
                (int) pageResult.getSize(),
                pageResult.getRecords()
        );
        
        return Results.success()
                .message("查询成功")
                .data("page", pageData);
    }

    @DeleteMapping("/{id}")
    public Results deleteUser(@PathVariable("id") Long id) {
        try {
            boolean result = userService.removeById(id);
            if (result) {
                return Results.success().message("删除成功");
            } else {
                return Results.fail().message("用户不存在");
            }
        } catch (Exception e) {
            return Results.fail().message("删除失败: " + e.getMessage());
        }
    }

    @DeleteMapping
    public Results deleteUsers(@RequestBody List<Long> ids) {
        try {
            if (ids == null || ids.isEmpty()) {
                return Results.fail().message("请提供要删除的用户ID列表");
            }
            boolean result = userService.removeByIds(ids);
            if (result) {
                return Results.success().message("批量删除成功");
            } else {
                return Results.fail().message("删除失败");
            }
        } catch (Exception e) {
            return Results.fail().message("批量删除失败: " + e.getMessage());
        }
    }

    @PutMapping("/{id}/profile")
    public Results completeProfile(@PathVariable("id") Long id, @RequestBody ProfileUpdateRequest request) {
        try {
            User user = userService.completeProfile(id, request);

            return Results.success()
                    .message("信息完善成功")
                    .data("user", user);
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        } catch (Exception e) {
            return Results.fail().message(e.getMessage());
        }
    }
}
