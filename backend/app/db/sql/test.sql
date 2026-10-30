/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80046 (8.0.46)
 Source Host           : localhost:3306
 Source Schema         : test

 Target Server Type    : MySQL
 Target Server Version : 80046 (8.0.46)
 File Encoding         : 65001

 Date: 20/10/2026 14:17:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for activity
-- ----------------------------
DROP TABLE IF EXISTS `activity`;
CREATE TABLE `activity`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '活动ID',
  `image_urls` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '活动图片URL（多个URL用逗号分隔）',
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '活动名称',
  `club_id` bigint NOT NULL COMMENT '社团ID',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '活动介绍',
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '活动地点',
  `notice` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '参与须知',
  `registration_start_time` datetime NULL DEFAULT NULL COMMENT '活动报名开始时间',
  `registration_end_time` datetime NULL DEFAULT NULL COMMENT '活动报名结束时间',
  `start_time` datetime NULL DEFAULT NULL COMMENT '活动开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '活动结束时间',
  `max_participants` int NULL DEFAULT NULL COMMENT '最大报名人数',
  `current_participants` int NULL DEFAULT 0 COMMENT '当前报名人数',
  `need_audit` tinyint(1) NULL DEFAULT 0 COMMENT '人员是否要审核(0-否,1-是)',
  `activity_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '活动类型（例如：文体艺术、体育活动）',
  `activity_level` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '活动等级（例如：校级、院级、班级）',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '审核中' COMMENT '活动状态（审核中、报名中、等待中、进行中、已结束）',
  `audit_status` tinyint(1) NULL DEFAULT 0 COMMENT '审核状态(0-待审核,1-已通过,2-已拒绝)',
  `audit_time` datetime NULL DEFAULT NULL COMMENT '审核时间',
  `audit_user_id` bigint NULL DEFAULT NULL COMMENT '审核人ID',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `score` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '0' COMMENT '活动总分',
  `is_published` tinyint(1) NULL DEFAULT 1 COMMENT '是否上架(0-下架,1-上架)',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_club_id`(`club_id` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE,
  INDEX `idx_activity_type`(`activity_type` ASC) USING BTREE,
  INDEX `idx_activity_level`(`activity_level` ASC) USING BTREE,
  INDEX `idx_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '活动表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for activity_registration
-- ----------------------------
DROP TABLE IF EXISTS `activity_registration`;
CREATE TABLE `activity_registration`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `activity_id` bigint NOT NULL COMMENT '活动ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT '待审核' COMMENT '报名状态（待审核、已通过、已拒绝）',
  `score` decimal(5, 2) NULL DEFAULT NULL COMMENT '评分（0-100）',
  `comment` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '文字评价',
  `audit_user_id` bigint NULL DEFAULT NULL COMMENT '审核人ID',
  `audit_time` datetime NULL DEFAULT NULL COMMENT '审核时间',
  `registration_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '报名时间',
  `checkin_time` datetime NULL DEFAULT NULL COMMENT '签到时间，NULL 表示未签到',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_activity_user`(`activity_id` ASC, `user_id` ASC) USING BTREE COMMENT '活动和用户唯一索引',
  INDEX `idx_activity_id`(`activity_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '活动报名表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for club
-- ----------------------------
DROP TABLE IF EXISTS `club`;
CREATE TABLE `club`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '社团ID',
  `icon_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '社团图标URL',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '社团名称',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '社团简介',
  `status` tinyint(1) NULL DEFAULT 1 COMMENT '状态(0-禁用,1-启用)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '社团表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for club_member
-- ----------------------------
DROP TABLE IF EXISTS `club_member`;
CREATE TABLE `club_member`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '关系ID',
  `club_id` bigint NOT NULL COMMENT '社团ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `status` tinyint NOT NULL DEFAULT 0 COMMENT '状态(0-待审核,1-正常,2-已拒绝)',
  `apply_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '申请时间',
  `join_time` datetime NULL DEFAULT NULL COMMENT '通过审核时间',
  `audit_user_id` bigint NULL DEFAULT NULL COMMENT '审核人ID',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_club_user`(`club_id` ASC, `user_id` ASC) USING BTREE COMMENT '社团和用户唯一索引',
  INDEX `idx_user_status`(`user_id` ASC, `status` ASC) USING BTREE,
  INDEX `idx_club_status`(`club_id` ASC, `status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '社团成员关系表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码哈希',
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '姓名',
  `student_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学号',
  `gender` tinyint(1) NULL DEFAULT NULL COMMENT '性别(0-女,1-男)',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '邮箱',
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg' COMMENT '用户头像',
  `token_version` int NOT NULL DEFAULT 0 COMMENT '令牌版本号',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `uk_student_no`(`student_no` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 28 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
