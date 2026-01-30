/*
 Navicat Premium Dump SQL

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80044 (8.0.44)
 Source Host           : localhost:3306
 Source Schema         : ljy

 Target Server Type    : MySQL
 Target Server Version : 80044 (8.0.44)
 File Encoding         : 65001

 Date: 16/01/2026 20:08:32
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
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '活动表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of activity
-- ----------------------------
INSERT INTO `activity` VALUES (1, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/active/IMG_20251128_183140.jpg,https://env-00jxuc2o76k9.normal.cloudstatic.cn/active/IMG_20251128_183136.jpg,https://env-00jxuc2o76k9.normal.cloudstatic.cn/active/IMG_20251128_183131.jpg', '疯狂动物城', 10, '在《疯狂动物城2》中，故事紧接前作，兔子警官朱迪和狐狸尼克再次联手，面对动物城中出现的新危机。影片中，一条名为盖瑞的神秘蛇闯入动物城，造成了不小的混乱。为了调查此事，朱迪和尼克不得不深入动物城的偏远区域卧底。在追查过程中，他们发现事情并不像表面那么简单，最终帮助盖瑞逃跑后，他们也成为了“逃犯”。', 'A栋报告厅', '观看电影时请保持安静', '2025-12-17 15:59:18', '2025-12-18 15:59:18', '2025-12-21 15:59:21', '2025-12-22 15:59:21', 100, 0, 0, '电影鉴赏', '班级', '已结束', 1, '2025-12-26 22:36:54', 8, '2025-12-18 16:19:04', '2025-12-21 18:12:55', '0', 0);
INSERT INTO `activity` VALUES (2, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/active/IMG_20251128_183140.jpg,https://env-00jxuc2o76k9.normal.cloudstatic.cn/active/IMG_20251128_183136.jpg,https://env-00jxuc2o76k9.normal.cloudstatic.cn/active/IMG_20251128_183131.jpg', '疯狂动物城2', 10, '在《疯狂动物城2》中，故事紧接前作，兔子警官朱迪和狐狸尼克再次联手，面对动物城中出现的新危机。影片中，一条名为盖瑞的神秘蛇闯入动物城，造成了不小的混乱。为了调查此事，朱迪和尼克不得不深入动物城的偏远区域卧底。在追查过程中，他们发现事情并不像表面那么简单，最终帮助盖瑞逃跑后，他们也成为了“逃犯”。', 'B栋报告厅', '观看电影时请保持安静', '2025-12-18 15:59:18', '2025-12-18 17:00:00', '2025-12-18 17:01:00', '2025-12-31 17:05:00', 100, 1, 1, '电影鉴赏', '校级', '已结束', 1, '2025-12-26 22:37:19', 8, '2025-12-18 16:51:55', '2025-12-19 14:47:17', '0', 0);
INSERT INTO `activity` VALUES (3, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766147502102_0.jpg?expire_at=1766148135&er_sign=47ea38848fe444826204322435b9cc4c,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766147502102_1.jpg?expire_at=1766148135&er_sign=39616f39d0866f17795d1dfdeca149c4,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766147502102_2.jpg?expire_at=1766148135&er_sign=fe1f63687a3f47d49de530afd7e24341', '政治思想活动', 1, '学习新思想，争做新青年', '主楼报告厅', '共青团或中国共产党才能拿参与', '2025-12-19 20:30:42', '2025-12-20 20:31:26', '2025-12-20 20:31:26', '2025-12-21 20:31:30', 20, 1, 0, '思想成长', '院级', '已结束', 1, '2025-12-20 17:22:20', 8, '2025-12-19 20:32:15', '2025-12-21 18:12:51', '0', 0);
INSERT INTO `activity` VALUES (4, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766753634010_0.jpg?expire_at=1766754242&er_sign=345a9c1b20886838bcb781df1c5067f1,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766754372109_0.jpg?expire_at=1766754974&er_sign=2facd7613b603fbaa9a15eb9ac2c7be2,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766754372109_1.jpg?expire_at=1766754975&er_sign=a49ffa613eec38ab1ca2709befef4381,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766754372109_2.jpg?expire_at=1766754975&er_sign=a13f79d1178eb68b4b90a3caad46773e', 'We', 10, '记录一下', '户外场地', '测试测试', '2025-12-20 20:41:35', '2025-12-21 20:42:42', '2025-12-21 20:42:42', '2025-12-26 20:42:46', 10, 2, 1, '思想成长', '校级', '已结束', 1, '2025-12-27 15:56:47', 8, '2025-12-20 20:43:01', '2025-12-20 20:43:01', '5.0', 0);
INSERT INTO `activity` VALUES (5, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766234754547_0.jpg?expire_at=1766235358&er_sign=0c1c7381ab0e8f9518694e5fc940c992,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766234754547_1.jpg?expire_at=1766235358&er_sign=2d50c79e1e247bd2430bfa2ab8e6db46,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766234754547_2.jpg?expire_at=1766235358&er_sign=1408003484891faef44095d6bacc829e', '测试', 2, '1212', '体育馆', '12121', '2025-12-20 20:45:28', '2025-12-21 20:45:41', '2025-12-21 20:45:41', '2025-12-22 20:45:44', 10, 3, 0, '公益志愿', '院级', '已结束', 1, '2025-12-20 20:46:11', 8, '2025-12-20 20:45:58', '2025-12-21 18:12:45', '2.5', 0);
INSERT INTO `activity` VALUES (6, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766235336782_0.jpg?expire_at=1766235940&er_sign=fbf2b8ef95b313da235215a32baa1fda,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766235336782_1.jpg?expire_at=1766235940&er_sign=136b174741c4a94e2c60118813b5e8c5', '测试111', 2, '1111', '体育馆', '钱钱钱', '2025-12-20 20:55:05', '2025-12-21 20:55:21', '2025-12-21 20:55:21', '2025-12-22 20:55:24', 5, 3, 1, '公益志愿', '院级', '已结束', 1, '2025-12-20 20:55:53', 8, '2025-12-20 20:55:39', '2025-12-21 18:12:48', '2.5', 0);
INSERT INTO `activity` VALUES (7, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766497895683_0.png?expire_at=1766498499&er_sign=430c64570a350eb244e3ff3b3a18bd40', '测试1121', 2, '准备开始咯', '体育馆', '121212', '2025-12-23 21:51:02', '2025-12-24 21:51:23', '2025-12-24 21:51:23', '2025-12-25 21:51:27', 1, 1, 1, '公益志愿', '学院', '已结束', 1, '2025-12-23 21:52:48', 8, '2025-12-23 21:51:39', '2025-12-23 21:51:39', '0.0', 0);
INSERT INTO `activity` VALUES (8, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766499341846_0.jpg?expire_at=1766499944&er_sign=56456aa8d5fcd81dcc78868583e06bfa', '测试拒绝活动', 2, '11212', '图书馆', '1213123', '2025-12-23 22:15:10', '2025-12-24 22:15:30', '2025-12-24 22:15:30', '2025-12-25 22:15:33', 2, 0, 1, '实践实习', '学院', '已拒绝', 2, '2025-12-23 22:15:56', 8, '2025-12-23 22:15:44', '2025-12-23 22:15:44', '0', 0);
INSERT INTO `activity` VALUES (9, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766501035208_0.jpg?expire_at=1766501710&er_sign=a900823cc33f157fd7cfa127650230a0,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766501035208_1.jpg?expire_at=1766501710&er_sign=0440a89a5a6fa7779a2d1855bbfe43f3,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766501035208_2.jpg?expire_at=1766501710&er_sign=db855eacf208f58ab51cde44b086c32d,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766501035208_3.jpg?expire_at=1766501711&er_sign=ee1238e894ab9f061bbab52f43e74aaa', '熊出没', 10, '熊大 熊二 光头强', '户外场地', '注意熊出没！！！！', '2025-12-23 22:43:41', '2025-12-24 22:44:58', '2025-12-24 22:44:58', '2025-12-25 22:45:02', 5, 0, 1, '文化艺体', '校级', '已结束', 1, '2025-12-24 20:26:42', 8, '2025-12-23 22:45:10', '2025-12-23 22:45:10', '0', 0);
INSERT INTO `activity` VALUES (10, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766753906457_0.png?expire_at=1766754509&er_sign=1804f225cdd3f1c3b58249a01d29aa56', '测试121', 5, '12121', '教学楼', '2323', '2025-12-24 19:34:44', '2025-12-25 19:34:58', '2025-12-25 19:34:58', '2025-12-26 19:35:01', 2, 0, 1, '实践实习', '校级', '已结束', 1, '2025-12-26 20:58:48', 8, '2025-12-24 19:35:12', '2025-12-24 19:35:12', '0', 0);
INSERT INTO `activity` VALUES (11, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766579337125_0.jpg?expire_at=1766579939&er_sign=e999728b962e8cdf62b4b4a83a6aec88,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766579337125_1.jpg?expire_at=1766579939&er_sign=ab7e01bbab5fd20a0ac94a307a7efc03', '测试失败活动（重新审核版）', 1, '啊擦删除', '教学楼', '12121', '2025-12-24 20:26:55', '2025-12-25 20:28:44', '2025-12-25 20:28:44', '2025-12-26 20:28:47', 4, 0, 1, '公益志愿', '学院', '已结束', 1, '2025-12-26 21:20:29', 8, '2025-12-24 20:28:59', '2025-12-24 20:28:59', '0', 0);
INSERT INTO `activity` VALUES (12, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766754311722_0.jpg?expire_at=1766754924&er_sign=4fccea6e2926f50616a42245001c73f9,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766754311722_1.jpg?expire_at=1766754925&er_sign=11548ab90c770b010531278c64120386', '测试989', 2, '1111111钱钱钱', '主楼报告厅', '1213123123', '2025-12-25 17:51:56', '2025-12-26 17:52:18', '2025-12-26 17:52:18', '2025-12-31 17:52:21', 5, 3, 1, '公益志愿', '学院', '已结束', 1, '2025-12-27 15:24:17', 8, '2025-12-25 17:52:40', '2025-12-25 17:52:40', '0', 0);
INSERT INTO `activity` VALUES (13, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766749298917_0.jpg?expire_at=1766749901&er_sign=660259556cbfbc6c1762bb7453e8566a,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766749298917_1.jpg?expire_at=1766749901&er_sign=270653e0293ccab92f242c042998f841', '12.26', 2, 'asaas', '体育馆', '1213123', '2025-12-26 19:41:09', '2025-12-27 19:41:26', '2025-12-27 19:41:26', '2025-12-28 19:41:29', 1, 0, 1, '公益志愿', '学院', '已结束', 1, '2025-12-26 19:41:49', 8, '2025-12-26 19:41:41', '2025-12-26 19:41:41', '0', 0);
INSERT INTO `activity` VALUES (14, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766750871291_0.jpg?expire_at=1766751473&er_sign=13a15895225ab4a92a3208989de1aa6c', '12.26-02', 2, '擦速度', '体育馆', '去212121', '2025-12-26 20:07:23', '2025-12-27 20:07:42', '2025-12-27 20:07:42', '2025-12-28 20:07:44', 5, 1, 0, '公益志愿', '学院', '已结束', 1, '2025-12-26 20:08:05', 8, '2025-12-26 20:07:53', '2025-12-26 20:07:53', '0', 0);
INSERT INTO `activity` VALUES (15, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766996366492_0.png?expire_at=1766996970&er_sign=f48dc5eba178bd01b683c99da8971c7a,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766996366492_1.png?expire_at=1766996970&er_sign=dfe6730627b993feee2bca693526ccc5,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766996366492_2.png?expire_at=1766996970&er_sign=c5ffe2dc73d3a679aa01404f9ade3d11', '12.29-01', 2, '我去问驱蚊器为', '体育馆', '啊我的期待我期待', '2025-12-29 16:18:47', '2025-12-30 16:19:11', '2025-12-30 16:19:11', '2025-12-31 16:19:14', 5, 1, 1, '公益志愿', '学院', '已结束', 1, '2025-12-29 16:25:10', 8, '2025-12-29 16:19:30', '2025-12-29 16:19:30', '0', 0);
INSERT INTO `activity` VALUES (16, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766997627151_0.jpg?expire_at=1766998230&er_sign=1ca048cd3a10458fab466c72942aa806,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766997627151_1.jpg?expire_at=1766998230&er_sign=db946ceb937c754631cea2932691ce77,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766997627151_2.jpg?expire_at=1766998231&er_sign=a947375958f5cb6648483ce47614cdbd,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1766997627151_3.jpg?expire_at=1766998231&er_sign=b3ac2e629f001cc019100a93de9709fc', '12.29-02', 2, '啊擦擦删除', '图书馆', '飞洒擦撒擦擦', '2025-12-29 16:39:07', '2025-12-29 16:41:30', '2025-12-29 16:41:30', '2025-12-29 16:41:30', 5, 1, 1, '公益志愿', '学院', '已结束', 1, '2025-12-29 16:42:34', 8, '2025-12-29 16:40:31', '2025-12-29 16:40:31', '4.0', 0);
INSERT INTO `activity` VALUES (17, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1768035143877_0.jpg?expire_at=1768035745&er_sign=3b8e3b0a5ac5b2f880d4d5ec339e44b9,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1768035143877_1.jpg?expire_at=1768035745&er_sign=690586903aa66510ce77e940bfc9ee8f', '1.10-1', 2, 'qweqweqwe', '体育馆', 'qwwqeqweqwe', '2026-01-10 17:02:01', '2026-01-10 17:02:01', '2026-01-10 17:02:01', '2026-01-31 16:52:06', 5, 1, 1, '公益志愿', '学院', '进行中', 1, '2026-01-10 17:02:58', 8, '2026-01-10 16:52:26', '2026-01-10 16:52:26', '0', 1);
INSERT INTO `activity` VALUES (18, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1768039440908_0.jpg?expire_at=1768040044&er_sign=e1ad71fd6e218935641337d11b2f68ec,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1768039440909_1.png?expire_at=1768040044&er_sign=98554b622fe0ce4d306ae679dec8f22d,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1768039440909_2.jpg?expire_at=1768040044&er_sign=1c023ab2d6ecc04b00258494be976b5b', '演示1', 2, '123123123', '体育馆', '2312312312312313', '2026-01-10 18:06:44', '2026-01-10 18:06:44', '2026-01-10 18:06:44', '2026-01-10 18:06:44', 5, 1, 1, '创新创业', '学院', '已结束', 1, '2026-01-10 18:08:24', 8, '2026-01-10 18:04:05', '2026-01-10 18:04:05', '4.0', 1);
INSERT INTO `activity` VALUES (19, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/1768051923695_0.jpg?expire_at=1768052524&er_sign=1a5dcfc0acc3f9eac38ffcae57abeb68,https://env-00jxuc2o76k9.normal.cloudstatic.cn/1768051923695_1.jpg?expire_at=1768052525&er_sign=a716b0a2492c114aeda14a0b4127397e', '1.10-01', 2, '测试', '体育馆', '12123123', '2026-01-10 21:31:27', '2026-01-11 21:31:47', '2026-01-11 21:31:47', '2026-01-31 21:31:51', 5, 1, 0, '实践实习', '学院', '报名中', 1, '2026-01-10 21:32:21', 8, '2026-01-10 21:32:05', '2026-01-10 21:32:05', '0', 1);

-- ----------------------------
-- Table structure for activity_checkin
-- ----------------------------
DROP TABLE IF EXISTS `activity_checkin`;
CREATE TABLE `activity_checkin`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `activity_id` bigint NOT NULL COMMENT '活动ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `checkin_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '签到时间',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_activity_user`(`activity_id` ASC, `user_id` ASC) USING BTREE COMMENT '活动和用户唯一索引（防止重复签到）',
  INDEX `idx_activity_id`(`activity_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_checkin_time`(`checkin_time` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '活动签到表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of activity_checkin
-- ----------------------------
INSERT INTO `activity_checkin` VALUES (1, 7, 8, '2025-12-25 20:43:35', '2025-12-25 20:43:34', '2025-12-25 20:43:34');
INSERT INTO `activity_checkin` VALUES (2, 4, 8, '2025-12-26 21:12:38', '2025-12-26 21:12:38', '2025-12-26 21:12:38');
INSERT INTO `activity_checkin` VALUES (3, 16, 18, '2025-12-29 16:41:51', '2025-12-29 16:41:50', '2025-12-29 16:41:50');
INSERT INTO `activity_checkin` VALUES (4, 18, 25, '2026-01-10 18:07:51', '2026-01-10 18:07:51', '2026-01-10 18:07:51');

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
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_activity_user`(`activity_id` ASC, `user_id` ASC) USING BTREE COMMENT '活动和用户唯一索引',
  INDEX `idx_activity_id`(`activity_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_status`(`status` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '活动报名表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of activity_registration
-- ----------------------------
INSERT INTO `activity_registration` VALUES (1, 2, 9, '已通过', 4.50, '1213123', 8, '2025-12-18 17:02:56', '2025-12-18 16:52:44', '2025-12-18 16:52:43', '2025-12-27 15:55:18');
INSERT INTO `activity_registration` VALUES (2, 3, 9, '已通过', NULL, NULL, NULL, NULL, '2025-12-20 17:29:13', '2025-12-20 17:29:13', '2025-12-20 17:29:13');
INSERT INTO `activity_registration` VALUES (3, 4, 14, '已通过', NULL, NULL, NULL, NULL, '2025-12-20 20:45:05', '2025-12-20 20:45:05', '2025-12-20 20:45:05');
INSERT INTO `activity_registration` VALUES (4, 5, 14, '已通过', NULL, NULL, NULL, NULL, '2025-12-20 20:46:26', '2025-12-20 20:46:25', '2025-12-20 20:46:25');
INSERT INTO `activity_registration` VALUES (5, 6, 14, '已通过', NULL, NULL, 8, '2025-12-20 22:41:00', '2025-12-20 20:56:03', '2025-12-20 20:56:03', '2025-12-20 20:56:03');
INSERT INTO `activity_registration` VALUES (6, 6, 9, '已通过', NULL, NULL, 8, '2025-12-20 22:40:38', '2025-12-20 21:50:07', '2025-12-20 21:50:06', '2025-12-20 21:50:06');
INSERT INTO `activity_registration` VALUES (7, 6, 8, '已通过', 2.50, '121212', 8, '2025-12-23 21:49:36', '2025-12-21 17:53:55', '2025-12-21 17:53:55', '2025-12-27 15:55:19');
INSERT INTO `activity_registration` VALUES (8, 5, 8, '已通过', 2.50, '11212121', NULL, NULL, '2025-12-21 17:55:58', '2025-12-21 17:55:58', '2025-12-27 15:55:21');
INSERT INTO `activity_registration` VALUES (9, 4, 8, '已通过', 5.00, '喜欢喜欢~~~', NULL, NULL, '2025-12-21 17:56:11', '2025-12-21 17:56:10', '2025-12-27 15:57:31');
INSERT INTO `activity_registration` VALUES (10, 6, 16, '已拒绝', NULL, NULL, 8, '2025-12-21 17:59:36', '2025-12-21 17:58:24', '2025-12-21 17:58:23', '2025-12-21 17:58:23');
INSERT INTO `activity_registration` VALUES (11, 5, 16, '已通过', NULL, NULL, NULL, NULL, '2025-12-21 17:58:38', '2025-12-21 17:58:37', '2025-12-21 17:58:37');
INSERT INTO `activity_registration` VALUES (12, 7, 8, '已通过', NULL, NULL, 8, '2025-12-23 21:53:21', '2025-12-23 21:52:57', '2025-12-23 21:52:57', '2025-12-27 15:58:19');
INSERT INTO `activity_registration` VALUES (13, 12, 17, '已通过', NULL, NULL, 8, '2025-12-25 17:56:20', '2025-12-25 17:53:17', '2025-12-25 17:53:17', '2025-12-25 17:53:17');
INSERT INTO `activity_registration` VALUES (14, 12, 9, '已通过', NULL, NULL, 8, '2025-12-25 17:55:46', '2025-12-25 17:54:03', '2025-12-25 17:54:02', '2025-12-25 17:54:02');
INSERT INTO `activity_registration` VALUES (15, 12, 14, '已拒绝', NULL, NULL, 8, '2025-12-25 17:55:48', '2025-12-25 17:54:21', '2025-12-25 17:54:20', '2025-12-25 17:54:20');
INSERT INTO `activity_registration` VALUES (16, 12, 15, '已通过', NULL, NULL, 8, '2025-12-25 17:55:55', '2025-12-25 17:54:39', '2025-12-25 17:54:39', '2025-12-25 17:54:39');
INSERT INTO `activity_registration` VALUES (17, 12, 16, '已拒绝', NULL, NULL, 8, '2025-12-25 17:55:58', '2025-12-25 17:54:53', '2025-12-25 17:54:53', '2025-12-25 17:54:53');
INSERT INTO `activity_registration` VALUES (18, 14, 8, '已通过', NULL, NULL, NULL, NULL, '2025-12-27 16:08:25', '2025-12-27 16:08:25', '2025-12-27 16:08:25');
INSERT INTO `activity_registration` VALUES (19, 13, 8, '待审核', NULL, NULL, NULL, NULL, '2025-12-27 16:08:30', '2025-12-27 16:08:29', '2025-12-27 16:08:29');
INSERT INTO `activity_registration` VALUES (20, 15, 9, '已通过', NULL, NULL, 9, '2025-12-29 16:36:58', '2025-12-29 16:36:19', '2025-12-29 16:36:18', '2025-12-29 16:36:18');
INSERT INTO `activity_registration` VALUES (21, 16, 18, '已通过', 4.00, '还不错', 9, '2025-12-29 16:41:04', '2025-12-29 16:40:58', '2025-12-29 16:40:57', '2025-12-29 16:40:57');
INSERT INTO `activity_registration` VALUES (22, 17, 14, '已通过', NULL, NULL, 8, '2026-01-10 16:54:50', '2026-01-10 16:54:34', '2026-01-10 16:54:33', '2026-01-10 16:54:33');
INSERT INTO `activity_registration` VALUES (23, 18, 25, '已通过', 4.00, 'bcbc', 9, '2026-01-10 18:05:35', '2026-01-10 18:05:17', '2026-01-10 18:05:16', '2026-01-10 18:05:16');
INSERT INTO `activity_registration` VALUES (24, 19, 26, '已通过', NULL, NULL, NULL, NULL, '2026-01-10 21:32:58', '2026-01-10 21:32:57', '2026-01-10 21:32:57');

-- ----------------------------
-- Table structure for campus_info
-- ----------------------------
DROP TABLE IF EXISTS `campus_info`;
CREATE TABLE `campus_info`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `school_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '学校名称',
  `college_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学院名称（可为空，表示学校级别）',
  `class_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '班级名称（可为空，表示学校或学院级别）',
  `level` tinyint NOT NULL COMMENT '层级：1-学校，2-学院，3-班级',
  `parent_id` bigint NULL DEFAULT NULL COMMENT '父级ID',
  `sort` int NULL DEFAULT 0 COMMENT '排序',
  `status` tinyint(1) NULL DEFAULT 1 COMMENT '状态(1-启用,0-禁用)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_name_path`(`school_name` ASC, `college_name` ASC, `class_name` ASC) USING BTREE,
  INDEX `idx_parent_id`(`parent_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of campus_info
-- ----------------------------
INSERT INTO `campus_info` VALUES (1, '广西民族大学', NULL, NULL, 1, NULL, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (2, '广西民族大学', '计算机与信息工程学院', NULL, 2, 1, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (3, '广西民族大学', '商学院', NULL, 2, 1, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (4, '广西民族大学', '文学院', NULL, 2, 1, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (5, '广西民族大学', '计算机与信息工程学院', '计算机科学与技术2021级1班', 3, 2, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (6, '广西民族大学', '计算机与信息工程学院', '计算机科学与技术2021级2班', 3, 2, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (7, '广西民族大学', '计算机与信息工程学院', '软件工程2021级1班', 3, 2, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (8, '广西民族大学', '计算机与信息工程学院', '软件工程2021级2班', 3, 2, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (9, '广西民族大学', '商学院', '工商管理2021级1班', 3, 3, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (10, '广西民族大学', '商学院', '工商管理2021级2班', 3, 3, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (11, '广西民族大学', '商学院', '市场营销2021级1班', 3, 3, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (12, '广西民族大学', '文学院', '汉语言文学2021级1班', 3, 4, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (13, '广西民族大学', '文学院', '汉语言文学2021级2班', 3, 4, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (14, '广西民族大学', '文学院', '新闻学2021级1班', 3, 4, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (15, '广西大学', NULL, NULL, 1, NULL, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (16, '广西大学', '机械工程学院', NULL, 2, 15, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (17, '广西大学', '电气工程学院', NULL, 2, 15, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (18, '广西大学', '机械工程学院', '机械工程2021级1班', 3, 16, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (19, '广西大学', '机械工程学院', '机械工程2021级2班', 3, 16, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (20, '广西大学', '机械工程学院', '自动化2021级1班', 3, 16, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (21, '广西大学', '电气工程学院', '电气工程2021级1班', 3, 17, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (22, '广西大学', '电气工程学院', '电气工程2021级2班', 3, 17, 0, 1, '2025-12-11 21:29:02');
INSERT INTO `campus_info` VALUES (24, '广西工业职业技术学院', NULL, NULL, 1, NULL, 0, 1, '2025-12-12 13:49:21');
INSERT INTO `campus_info` VALUES (26, '广西工业职业技术学院', '电子信息学院', NULL, 2, 24, 0, 1, '2025-12-12 14:03:14');
INSERT INTO `campus_info` VALUES (27, '南宁师范大学', NULL, NULL, 1, NULL, 0, 1, '2025-12-12 14:47:57');
INSERT INTO `campus_info` VALUES (28, '北京大学', NULL, NULL, 1, NULL, 0, 1, '2025-12-12 14:49:11');
INSERT INTO `campus_info` VALUES (29, '清华大学', NULL, NULL, 1, NULL, 0, 1, '2025-12-14 14:40:52');
INSERT INTO `campus_info` VALUES (30, '清华大学', '电子信息学院', NULL, 2, 29, 0, 1, '2025-12-14 14:40:52');
INSERT INTO `campus_info` VALUES (31, '清华大学', '电子信息学院', '计科04班', 3, 30, 0, 1, '2025-12-14 14:40:52');
INSERT INTO `campus_info` VALUES (32, '广西工业职业技术学院', '电子信息学院', '计应2135班', 3, 26, 0, 1, '2025-12-14 14:51:07');
INSERT INTO `campus_info` VALUES (33, '广东大学', NULL, NULL, 1, NULL, 0, 1, '2025-12-14 15:07:30');
INSERT INTO `campus_info` VALUES (34, '广东大学', '军学院', NULL, 2, 33, 0, 1, '2025-12-14 15:07:30');
INSERT INTO `campus_info` VALUES (35, '广东大学', '军学院', '军事01班', 3, 34, 0, 1, '2025-12-14 15:07:30');

-- ----------------------------
-- Table structure for club
-- ----------------------------
DROP TABLE IF EXISTS `club`;
CREATE TABLE `club`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '社团ID',
  `icon_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '社团图标URL',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '社团名称',
  `tags` varchar(255) CHARACTER SET utf16 COLLATE utf16_general_ci NULL DEFAULT NULL COMMENT '社团标签（多个标签用逗号分隔）',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '社团简介',
  `status` tinyint(1) NULL DEFAULT 1 COMMENT '状态(0-禁用,1-启用)',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `level_tag` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '社团类型',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_name`(`name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '社团表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of club
-- ----------------------------
INSERT INTO `club` VALUES (1, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/buluo.png?expire_at=1765708747&er_sign=f30db4e3eb3a66a4c4cbb9ecd3103eb3', '计算机协会', '技术,编程,计算机', '致力于计算机技术交流与学习的社团', 1, '2025-12-14 18:09:45', '2025-12-17 20:23:17', '学院');
INSERT INTO `club` VALUES (2, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765728382458_dayingzhi.png', '测试', '社团与协会', '测试12211', 1, '2025-12-15 00:06:23', '2025-12-17 20:23:12', '学院');
INSERT INTO `club` VALUES (3, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765895733415_4k1YB9VSoosa91ae3ab32b7533fb2187e41100345222.png', '巧克力派对', '文艺,传媒', '分享你喜欢的巧克力，德芙~~', 1, '2025-12-16 22:35:34', '2025-12-17 20:23:58', '班级');
INSERT INTO `club` VALUES (4, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765895856131_tXoDVcd1pQbXd10e23de1afb5c87680a8a6f444a3ca9.png', '测试21', '公益志愿', '测2额1额2额2额', 1, '2025-12-16 22:37:37', '2025-12-17 20:43:21', '校级');
INSERT INTO `club` VALUES (5, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765895881058_90mIHC2E9k1y193a5891519e00bb2e78103f00693cd1.png', '测试4', '公益志愿', '1121212', 1, '2025-12-16 22:38:01', '2025-12-17 20:43:19', '校级');
INSERT INTO `club` VALUES (6, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765896097429_yu37kn5JghOqa92b30a98e641740efd9fc87416cc5ec.jpg', '奶牛奶牛', '公益志愿', '我是乃龙', 1, '2025-12-16 22:41:38', '2025-12-17 20:23:55', '班级');
INSERT INTO `club` VALUES (7, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765896183873_kdctXbXmbYp2e8693ab13544c9205fc2df2f4fc4da52.jpg', '帅哥部落', '公益志愿', '都是帅哥', 1, '2025-12-16 22:43:04', '2025-12-17 20:23:55', '班级');
INSERT INTO `club` VALUES (8, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765974907543_wyp.jpg', '美女部落', '团支部,公益志愿,文艺', '这里都是美女', 1, '2025-12-17 20:35:08', '2025-12-17 20:43:16', '校级');
INSERT INTO `club` VALUES (9, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1765975376014_baozhatou.jpg', '非主流社团', '公益志愿,团支部,文艺', '里面的都是非主流', 1, '2025-12-17 20:42:57', '2025-12-17 20:42:57', '院级');
INSERT INTO `club` VALUES (10, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/club/1766045269367_danggao.png', '动漫社团', '传媒,社团与协会,音乐,文艺', '欢迎你的加入~', 1, '2025-12-18 16:07:50', '2025-12-18 16:07:50', '校级');

-- ----------------------------
-- Table structure for club_member
-- ----------------------------
DROP TABLE IF EXISTS `club_member`;
CREATE TABLE `club_member`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `club_id` bigint NOT NULL COMMENT '社团ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '用户名称',
  `is_manager` tinyint(1) NULL DEFAULT 0 COMMENT '是否为管理员(0-否,1-是)',
  `join_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_club_user`(`club_id` ASC, `user_id` ASC) USING BTREE COMMENT '社团和用户唯一索引',
  INDEX `idx_club_id`(`club_id` ASC) USING BTREE,
  INDEX `idx_user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_user_name`(`user_name` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 20 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '社团人员表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of club_member
-- ----------------------------
INSERT INTO `club_member` VALUES (1, 1, 8, '超级管理员', 1, '2025-12-14 18:10:19', '2025-12-14 18:10:19', '2025-12-16 16:03:26');
INSERT INTO `club_member` VALUES (2, 2, 9, '测试01', 1, '2025-12-16 16:25:00', '2025-12-16 16:24:59', '2025-12-16 16:24:59');
INSERT INTO `club_member` VALUES (3, 2, 8, '超级管理员', 1, '2025-12-16 16:27:41', '2025-12-16 16:27:40', '2025-12-16 21:36:48');
INSERT INTO `club_member` VALUES (4, 3, 8, '超级管理员', 1, '2025-12-16 22:35:51', '2025-12-16 22:35:50', '2025-12-16 22:35:50');
INSERT INTO `club_member` VALUES (5, 4, 8, '超级管理员', 1, '2025-12-16 22:41:04', '2025-12-16 22:41:04', '2025-12-16 22:41:04');
INSERT INTO `club_member` VALUES (6, 6, 8, '超级管理员', 1, '2025-12-16 22:41:54', '2025-12-16 22:41:53', '2025-12-16 22:41:53');
INSERT INTO `club_member` VALUES (7, 7, 14, '弄囊贝', 0, '2025-12-17 19:50:09', '2025-12-17 19:50:08', '2025-12-17 19:50:08');
INSERT INTO `club_member` VALUES (8, 2, 14, '弄囊贝', 0, '2025-12-17 19:53:21', '2025-12-17 19:53:21', '2025-12-17 19:53:21');
INSERT INTO `club_member` VALUES (9, 10, 8, '超级管理员', 1, '2025-12-18 16:59:30', '2025-12-18 16:59:30', '2025-12-18 16:59:30');
INSERT INTO `club_member` VALUES (10, 2, 15, '测试3', 0, '2025-12-20 21:53:24', '2025-12-20 21:53:23', '2025-12-20 21:53:23');
INSERT INTO `club_member` VALUES (11, 2, 16, '测试4', 0, '2025-12-20 21:54:24', '2025-12-20 21:54:24', '2025-12-20 21:54:24');
INSERT INTO `club_member` VALUES (12, 8, 8, '超级管理员', 1, '2025-12-22 15:25:07', '2025-12-22 15:25:07', '2025-12-22 15:25:07');
INSERT INTO `club_member` VALUES (13, 9, 8, '超级管理员', 1, '2025-12-22 15:25:17', '2025-12-22 15:25:16', '2025-12-22 15:25:16');
INSERT INTO `club_member` VALUES (14, 5, 8, '超级管理员', 1, '2025-12-22 15:25:23', '2025-12-22 15:25:23', '2025-12-22 15:25:23');
INSERT INTO `club_member` VALUES (15, 7, 8, '超级管理员', 1, '2025-12-22 15:26:04', '2025-12-22 15:26:03', '2025-12-22 15:26:03');
INSERT INTO `club_member` VALUES (16, 10, 17, '测试5', 0, '2025-12-25 17:45:47', '2025-12-25 17:45:46', '2025-12-25 17:45:46');
INSERT INTO `club_member` VALUES (17, 9, 17, '测试5', 0, '2025-12-29 16:15:02', '2025-12-29 16:15:02', '2025-12-29 16:15:02');
INSERT INTO `club_member` VALUES (18, 2, 18, '测试06', 0, '2026-01-10 17:16:06', '2026-01-10 17:16:06', '2026-01-10 17:16:06');
INSERT INTO `club_member` VALUES (19, 7, 26, 'ljy', 0, '2026-01-10 21:27:42', '2026-01-10 21:27:42', '2026-01-10 21:27:42');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '账号',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码',
  `is_completed` tinyint(1) NULL DEFAULT 0 COMMENT '是否完善信息(0-否,1-是)',
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '姓名',
  `student_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学号',
  `gender` tinyint(1) NULL DEFAULT NULL COMMENT '性别(0-女,1-男)',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '邮箱',
  `school_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学校名称',
  `college_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '学院名称',
  `class_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '班级名称',
  `complete_time` datetime NULL DEFAULT NULL COMMENT '完善时间',
  `is_manager` tinyint(1) NULL DEFAULT 0 COMMENT '是否为管理者(0-否,1-是)',
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg' COMMENT '用户头像',
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '登录令牌',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_boss` tinyint UNSIGNED NULL DEFAULT 0 COMMENT '是否为超级管理者(0-否,1-是)',
  `wx_openid` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '微信OpenID',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `uk_student_no`(`student_no` ASC) USING BTREE,
  INDEX `idx_wx_openid`(`wx_openid` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (8, 'admin', '1111111', 1, '超级管理员', '202413143500187', 0, '15218786403', '2914288317@qq.com', '广西大学', '电气工程学院', '电气工程2021级1班', '2025-12-14 15:17:42', 1, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/1765692890867_wyp.jpg', 'b248503a-948a-4feb-98f8-e46042d33ab5', '2025-12-13 00:13:49', '2025-12-14 15:15:15', 1, NULL);
INSERT INTO `user` VALUES (9, 'test01', '1111111', 1, '管理员', '1212112', 1, '15293974687', '121212@qq.com', '广西民族大学', '文学院', '汉语言文学2021级1班', '2025-12-13 23:01:38', 1, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/1765629123191_xin.jpg', 'fe0776af-3d88-437d-b0c9-f8d3fb887231', '2025-12-13 20:27:42', '2026-01-10 16:56:19', 0, NULL);
INSERT INTO `user` VALUES (14, 'test02', '111111', 1, '弄囊贝', '123456789', 1, '15232323232', '1213123@qq.com', '广西工业职业技术学院', '电子信息学院', '计应2135班', '2025-12-17 19:49:48', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg', 'b39d7c80-bcb2-4c49-99c0-4d8e98ae0b4e', '2025-12-17 19:49:00', '2025-12-17 19:49:00', 0, NULL);
INSERT INTO `user` VALUES (15, 'test03', '111111', 1, '测试3', '11111', 0, '15233232323', '121212122@qq.com', '广西民族大学', '计算机与信息工程学院', '计算机科学与技术2021级1班', '2025-12-20 21:53:01', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg', '5cb34b98-5bc7-41df-8634-935e75b68866', '2025-12-20 21:52:12', '2025-12-20 21:52:34', 0, NULL);
INSERT INTO `user` VALUES (16, 'test04', '111111', 1, '测试4', '121212121', 1, '15212381313', '12121212@qq.com', '广西民族大学', '计算机与信息工程学院', '计算机科学与技术2021级1班', '2025-12-20 21:54:15', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg', '5f1f8423-5eb2-47b3-b9af-bb4f2c772d9b', '2025-12-20 21:53:45', '2025-12-20 21:53:45', 0, NULL);
INSERT INTO `user` VALUES (17, 'test05', '111111', 1, '测试5', '212121212121', 0, '15213232323', '1213@qq.com', '广西民族大学', '商学院', '市场营销2021级1班', '2026-01-11 00:11:02', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/1768061460303_huanghou.jpg', 'c8801ee9-4003-437e-b16d-ec6ad01e5aa7', '2025-12-25 17:43:26', '2025-12-25 17:43:26', 0, NULL);
INSERT INTO `user` VALUES (18, 'test06', '111111', 1, '测试06', '1231231231', 0, '16343434343', '23425424@qq.com', '广西大学', '机械工程学院', '自动化2021级1班', '2025-12-29 16:38:55', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg', '6706f128-9b90-41b7-b6d0-9b41bde50d39', '2025-12-29 16:38:20', '2025-12-29 16:38:20', 0, NULL);
INSERT INTO `user` VALUES (24, 'qwe', '111111', 1, 'asdasdas', '12314234', 1, '14232323232', '1212@qq.com', '广西民族大学', '计算机与信息工程学院', '计算机科学与技术2021级1班', '2026-01-10 18:01:13', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg', '8ba76cac-0f6d-4ae1-8abd-1665b7ef0e6b', '2026-01-10 18:00:49', '2026-01-10 18:00:49', 0, NULL);
INSERT INTO `user` VALUES (25, 'qwe1', '111111', 1, 'asdas', '123123131', 1, '17445454545', '12131@qq.com', '广西民族大学', '计算机与信息工程学院', '计算机科学与技术2021级1班', '2026-01-10 18:02:58', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/admin.jpg', '79086170-2970-4837-8588-135e5534a3ff', '2026-01-10 18:02:33', '2026-01-10 18:02:33', 0, NULL);
INSERT INTO `user` VALUES (26, 'wx_bdac2b05', '01d655cc-93b2-42a6-a0ff-801a4f80f361', 1, 'ljy', '202413143500183', 1, '15218786403', '2914288317@qq.com', '广西民族大学', '计算机与信息工程学院', '计算机科学与技术2021级2班', '2026-01-11 00:10:22', 0, 'https://env-00jxuc2o76k9.normal.cloudstatic.cn/avatar/1768061420738_undefined', 'ccdc4c9a-3970-4650-8ccc-392eba0e4cc8', '2026-01-10 21:23:30', '2026-01-10 21:23:30', 0, 'oNIim5bVfsSUzoyb2jdFbBC7CHGg');

SET FOREIGN_KEY_CHECKS = 1;
