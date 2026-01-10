package com.example.projectsystem.domain;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serial;
import java.io.Serializable;
import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@TableName("user")
public class User implements Serializable {
    @Serial
    private static final long serialVersionUID = 1L;

    @TableId(type = IdType.AUTO)
    private Long id;

    private String username;

    @TableField("wx_openid")
    private String wxOpenid;

    private String password;

    @TableField("is_completed")
    private Boolean isCompleted;

    private String realName;

    private String studentNo;

    /**
     * 性别(0-女,1-男)
     */
    private Integer gender;

    private String phone;

    private String email;

    private String schoolName;

    private String collegeName;

    private String className;

    private LocalDateTime completeTime;

    @TableField("is_manager")
    private Boolean isManager;

    @TableField("is_boss")
    private Boolean isBoss;

    @TableField("avatar_url")
    private String avatarUrl;

    private String token;

    private LocalDateTime createTime;

    private LocalDateTime updateTime;
}
