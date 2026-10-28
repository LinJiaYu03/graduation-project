-- RBAC 表结构、初始化数据与旧数据迁移（MySQL 8.0+，数据库 test）

CREATE TABLE IF NOT EXISTS `role` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `code` varchar(50) NOT NULL COMMENT '角色编码：USER/CLUB_MANAGER/ADMIN',
  `name` varchar(50) NOT NULL COMMENT '角色名称',
  `description` varchar(255) NULL DEFAULT NULL COMMENT '角色说明',
  `status` tinyint NOT NULL DEFAULT 1 COMMENT '1启用 0禁用',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_role_code`(`code` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `permission` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '权限ID',
  `code` varchar(80) NOT NULL COMMENT '权限编码，如 activity:create',
  `name` varchar(80) NOT NULL COMMENT '权限名称',
  `resource` varchar(50) NOT NULL COMMENT '资源，如 activity',
  `action` varchar(50) NOT NULL COMMENT '动作，如 create',
  `description` varchar(255) NULL DEFAULT NULL COMMENT '权限说明',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_permission_code`(`code` ASC) USING BTREE,
  INDEX `idx_permission_resource`(`resource` ASC, `action` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_role` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `club_id` bigint NOT NULL DEFAULT 0 COMMENT '0=全局角色；非0=角色只在对应社团内生效',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_user_role_scope`(`user_id` ASC, `role_id` ASC, `club_id` ASC) USING BTREE,
  INDEX `idx_user_role_role`(`role_id` ASC) USING BTREE,
  INDEX `idx_user_role_club`(`club_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `role_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `role_id` bigint NOT NULL COMMENT '角色ID',
  `permission_id` bigint NOT NULL COMMENT '权限ID',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_role_permission`(`role_id` ASC, `permission_id` ASC) USING BTREE,
  INDEX `idx_role_permission_permission`(`permission_id` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;

-- ---------------------------------------------------------------------------
-- 角色
-- ---------------------------------------------------------------------------
INSERT INTO `role` (`code`, `name`, `description`) VALUES
('USER', '普通用户', '登录用户的基础权限'),
('CLUB_MANAGER', '社团管理员', '指定社团内的管理权限'),
('ADMIN', '超级管理员', '平台全局管理权限')
ON DUPLICATE KEY UPDATE `name` = VALUES(`name`), `description` = VALUES(`description`);

-- ---------------------------------------------------------------------------
-- 权限点
-- ---------------------------------------------------------------------------
INSERT INTO `permission` (`code`, `name`, `resource`, `action`) VALUES
('user:update',            '修改本人资料',     'user',         'update'),
('user:view',              '查看用户列表',     'user',         'view'),
('user:delete',            '删除用户',         'user',         'delete'),
('user:role:assign',       '分配用户角色',     'user',         'role:assign'),
('user:manage',            '管理其他用户资料', 'user',         'manage'),

('club:view',              '查看社团',         'club',         'view'),
('club:create',            '创建社团',         'club',         'create'),
('club:update',            '修改社团',         'club',         'update'),
('club:join',              '加入社团',         'club',         'join'),
('club:member:view',       '查看社团成员',     'club',         'member:view'),
('club:manager:assign',    '设置社团管理员',   'club',         'manager:assign'),

('activity:view',          '查看活动',         'activity',     'view'),
('activity:create',        '创建活动',         'activity',     'create'),
('activity:update',        '编辑活动',         'activity',     'update'),
('activity:delete',        '删除活动',         'activity',     'delete'),
('activity:publish',       '上下架活动',       'activity',     'publish'),
('activity:review',        '平台审核活动',     'activity',     'review'),
('activity:qrcode',        '生成签到二维码',   'activity',     'qrcode'),
('activity:register',      '报名活动',         'activity',     'register'),
('activity:comment',       '评价活动',         'activity',     'comment'),
('activity:checkin',       '签到活动',         'activity',     'checkin'),
('activity:stats',         '查看活动统计',     'activity',     'stats'),
('activity:export',        '导出活动数据',     'activity',     'export'),

('registration:view',      '查看报名信息',     'registration', 'view'),
('registration:review',    '审核报名',         'registration', 'review'),

('rbac:manage',            '配置角色与权限',   'rbac',         'manage')
ON DUPLICATE KEY UPDATE
  `name` = VALUES(`name`),
  `resource` = VALUES(`resource`),
  `action` = VALUES(`action`);

-- ---------------------------------------------------------------------------
-- 角色权限绑定
-- ---------------------------------------------------------------------------
INSERT IGNORE INTO `role_permission` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `role` r
JOIN `permission` p ON p.code IN (
  'user:update', 'club:view', 'club:create', 'club:join', 'club:member:view',
  'activity:view', 'activity:register', 'activity:comment', 'activity:checkin'
)
WHERE r.code = 'USER';

INSERT IGNORE INTO `role_permission` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `role` r
JOIN `permission` p ON p.code IN (
  'user:update', 'club:view', 'club:create', 'club:join', 'club:member:view',
  'activity:view', 'activity:register', 'activity:comment', 'activity:checkin',
  'club:update', 'activity:create', 'activity:update', 'activity:delete',
  'activity:publish', 'activity:qrcode', 'activity:stats', 'activity:export',
  'registration:view', 'registration:review'
)
WHERE r.code = 'CLUB_MANAGER';

INSERT IGNORE INTO `role_permission` (`role_id`, `permission_id`)
SELECT r.id, p.id
FROM `role` r
JOIN `permission` p
WHERE r.code = 'ADMIN';

-- ---------------------------------------------------------------------------
-- 存量社团数据迁移
-- 原超级管理员已在上线时迁移为 ADMIN，user.is_boss / user.is_manager 字段已删除
-- ---------------------------------------------------------------------------
-- 社团管理员 -> 对应社团的 CLUB_MANAGER 角色
INSERT IGNORE INTO `user_role` (`user_id`, `role_id`, `club_id`)
SELECT cm.user_id, r.id, cm.club_id
FROM `club_member` cm
JOIN `role` r ON r.code = 'CLUB_MANAGER'
WHERE cm.is_manager = 1;

-- 所有用户补默认 USER 全局角色
INSERT IGNORE INTO `user_role` (`user_id`, `role_id`, `club_id`)
SELECT u.id, r.id, 0
FROM `user` u
JOIN `role` r ON r.code = 'USER';
