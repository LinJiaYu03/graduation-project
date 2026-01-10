package com.example.projectsystem.service.Impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.example.projectsystem.domain.User;
import com.example.projectsystem.dto.ProfileUpdateRequest;
import com.example.projectsystem.mapper.UserMapper;
import com.example.projectsystem.service.ClubMemberService;
import com.example.projectsystem.service.UserService;
import org.springframework.context.annotation.Lazy;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.client.RestTemplate;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.time.LocalDateTime;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.UUID;

@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements UserService {

    private final ClubMemberService clubMemberService;

    public UserServiceImpl(@Lazy ClubMemberService clubMemberService) {
        this.clubMemberService = clubMemberService;
    }

    @Override
    public User register(String username, String password) {
        if (!StringUtils.hasText(username) || !StringUtils.hasText(password)) {
            throw new IllegalArgumentException("账号和密码不能为空");
        }
        User exists = lambdaQuery().eq(User::getUsername, username).one();
        if (exists != null) {
            throw new IllegalArgumentException("账号已存在");
        }
        User user = new User();
        user.setUsername(username);
        user.setPassword(password);
        user.setIsCompleted(false);
        user.setIsManager(false);
        user.setIsBoss(false);
        user.setAvatarUrl("https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg");
        save(user);
        return user;
    }

    @Override
    public User login(String username, String password) {
        if (!StringUtils.hasText(username) || !StringUtils.hasText(password)) {
            throw new IllegalArgumentException("账号和密码不能为空");
        }
        User user = lambdaQuery().eq(User::getUsername, username).one();
        if (user == null || !Objects.equals(user.getPassword(), password)) {
            throw new IllegalArgumentException("账号或密码错误");
        }
        user.setToken(UUID.randomUUID().toString());
        updateById(user);
        return user;
    }

    @Override
    public User wxLogin(String code) {
        if (!StringUtils.hasText(code)) {
            throw new IllegalArgumentException("code不能为空");
        }

        // 微信小程序配置 (请替换为真实的AppID和Secret)
        String appId = "wx2caaaf47aead807a";
        String secret = "1e6dcbf6a9ccfc823a5447aa262adcc2";
        String url = "https://api.weixin.qq.com/sns/jscode2session?appid=" + appId + "&secret=" + secret + "&js_code=" + code + "&grant_type=authorization_code";

        RestTemplate restTemplate = new RestTemplate();
        String response = restTemplate.getForObject(url, String.class);

        ObjectMapper mapper = new ObjectMapper();
        String openid = null;
        try {
            JsonNode root = mapper.readTree(response);
            if (root.has("errcode") && root.get("errcode").asInt() != 0) {
                throw new IllegalArgumentException("微信登录失败: " + (root.has("errmsg") ? root.get("errmsg").asText() : "未知错误"));
            }
            if (root.has("openid")) {
                openid = root.get("openid").asText();
            }
        } catch (Exception e) {
            throw new IllegalArgumentException("微信登录失败: " + e.getMessage());
        }

        if (!StringUtils.hasText(openid)) {
            throw new IllegalArgumentException("无法获取OpenID");
        }

        User user = lambdaQuery().eq(User::getWxOpenid, openid).one();
        if (user == null) {
            // 新用户自动注册
            user = new User();
            user.setWxOpenid(openid);
            // 生成随机用户名
            user.setUsername("wx_" + UUID.randomUUID().toString().substring(0, 8));
            user.setPassword(UUID.randomUUID().toString()); // 随机密码
            user.setIsCompleted(false);
            user.setIsManager(false);
            user.setIsBoss(false);
            user.setAvatarUrl("https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg");
            save(user);
        }

        // 生成Token
        user.setToken(UUID.randomUUID().toString());
        updateById(user);
        
        return user;
    }

    @Override
    public User completeProfile(Long userId, ProfileUpdateRequest request) {
        User user = getById(userId);
        if (user == null) {
            throw new NoSuchElementException("用户不存在");
        }
        
        // 所有字段都是可选的，只有提供时才更新
        boolean realNameChanged = false;
        if (StringUtils.hasText(request.getRealName())) {
            String oldRealName = user.getRealName();
            user.setRealName(request.getRealName());
            // 如果姓名发生变化，同步更新club_member表中的user_name
            if (!Objects.equals(oldRealName, request.getRealName())) {
                realNameChanged = true;
            }
        }
        if (StringUtils.hasText(request.getStudentNo())) {
            user.setStudentNo(request.getStudentNo());
        }
        if (request.getGender() != null) {
            user.setGender(request.getGender());
        }
        if (StringUtils.hasText(request.getPhone())) {
            user.setPhone(request.getPhone());
        }
        if (StringUtils.hasText(request.getEmail())) {
            user.setEmail(request.getEmail());
        }
        if (StringUtils.hasText(request.getSchoolName())) {
            user.setSchoolName(request.getSchoolName());
        }
        if (StringUtils.hasText(request.getCollegeName())) {
            user.setCollegeName(request.getCollegeName());
        }
        if (StringUtils.hasText(request.getClassName())) {
            user.setClassName(request.getClassName());
        }
        if (StringUtils.hasText(request.getAvatarUrl())) {
            user.setAvatarUrl(request.getAvatarUrl());
        }
        if (request.getIsManager() != null) {
            user.setIsManager(request.getIsManager());
        }
        if (request.getIsBoss() != null) {
            user.setIsBoss(request.getIsBoss());
        }
        if (StringUtils.hasText(request.getPassword())) {
            user.setPassword(request.getPassword());
        }
        
        user.setIsCompleted(true);
        user.setCompleteTime(LocalDateTime.now());
        updateById(user);
        
        // 如果姓名发生变化，同步更新club_member表中的user_name
        if (realNameChanged) {
            String userName = StringUtils.hasText(user.getRealName()) ? user.getRealName() : user.getUsername();
            clubMemberService.updateUserName(userId, userName);
        }
        
        return user;
    }
}
