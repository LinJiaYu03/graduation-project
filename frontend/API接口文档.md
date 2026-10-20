## API 接口文档

### 基础信息

- **基础URL**: `http://localhost:8080/api`
- **响应格式**: JSON
- **统一响应结构**:
```json
{
  "code": 200,
  "message": "响应消息",
  "success": true,
  "data": {}
}
```

---

## 一、用户相关接口

### 1. 用户注册

**接口**: `POST /api/users/register`

**请求参数**:
```json
{
  "username": "账号",
  "password": "密码"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "注册成功",
  "success": true,
  "data": {
    "userId": 1
  }
}
```

---

### 2. 用户登录

**接口**: `POST /api/users/login`

**请求参数**:
```json
{
  "username": "账号",
  "password": "密码"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "登录成功",
  "success": true,
  "data": {
    "token": "登录令牌",
    "user": {}
  }
}
```

---

### 3. 获取用户列表

**接口**: `GET /api/users`

**请求参数** (查询参数):
- `currentPage`: 当前页码，默认值为 1
- `pageSize`: 每页显示条数，默认值为 10

**请求示例**:
```
GET /api/users?currentPage=1&pageSize=10
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "page": {
      "total": 100,
      "currentPage": 1,
      "pageSize": 10,
      "totalPage": 10,
      "records": []
    }
  }
}
```

---

### 4. 模糊查询用户

**接口**: `GET /api/users/search`

**请求参数** (查询参数):
- `keyword`: 搜索关键词（可选），支持根据用户名、姓名或学号模糊查询
- `currentPage`: 当前页码，默认值为 1
- `pageSize`: 每页显示条数，默认值为 10

**请求示例**:
```
GET /api/users/search?keyword=张三&currentPage=1&pageSize=10
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "page": {
      "total": 5,
      "currentPage": 1,
      "pageSize": 10,
      "totalPage": 1,
      "records": [
        {
          "id": 1,
          "name": "计算机协会",
          "memberCount": 35
        }
      ]
    }
  }
}
```

---

### 5. 删除用户

**接口**: `DELETE /api/users/{id}`

**路径参数**:
- `id`: 用户ID

**响应示例**:
```json
{
  "code": 200,
  "message": "删除成功",
  "success": true,
  "data": {}
}
```

---

### 6. 批量删除用户

**接口**: `DELETE /api/users`

**请求参数**:
```json
[1, 2, 3]
```

**响应示例**:
```json
{
  "code": 200,
  "message": "批量删除成功",
  "success": true,
  "data": {}
}
```

---

### 7. 完善个人信息

**接口**: `PUT /api/users/{id}/profile`

**路径参数**:
- `id`: 用户ID

**请求参数** (所有字段均为可选):
- `realName`: 姓名
- `studentNo`: 学号
- `gender`: 性别(0-女,1-男)
- `phone`: 手机号
- `email`: 邮箱
- `schoolName`: 学校名称
- `collegeName`: 学院名称
- `className`: 班级名称
- `avatarUrl`: 用户头像URL
- `isManager`: 是否为管理者(true/false)
- `isBoss`: 是否为超级管理者(true/false)
- `password`: 密码

**请求示例**:
```json
{
  "realName": "张三",
  "studentNo": "2021001",
  "gender": 1,
  "schoolName": "XX大学",
  "collegeName": "计算机学院",
  "className": "计算机1班",
  "phone": "13800138000",
  "email": "zhangsan@example.com",
  "avatarUrl": "https://example.com/avatar.jpg",
  "isManager": false,
  "isBoss": false,
  "password": "newPassword123"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "信息完善成功",
  "success": true,
  "data": {
    "user": {}
  }
}
```

---

## 二、校园信息相关接口

### 1. 获取树形结构

**接口**: `GET /api/campus/tree`

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "items": []
  }
}
```

---

### 2. 创建校园信息

**接口**: `POST /api/campus`

**请求参数**:
- `schoolName`: 学校名称（必填）
- `collegeName`: 学院名称（可选）
- `className`: 班级名称（可选）
- `sort`: 排序（可选，默认0）
- `status`: 状态（可选，默认1）

**请求示例**:
```json
{
  "schoolName": "清华大学",
  "collegeName": "电子信息学院",
  "className": "计科04班"
}
```

**说明**:
- 如果三个字段都不存在，会创建三条数据：学校、学院、班级
- 如果学校已存在，其他不存在，则只创建学院和班级
- 如果学校和学院都已存在，班级不存在，则只创建班级
- 如果都已存在，则不创建任何数据

**响应示例**:
```json
{
  "code": 200,
  "message": "创建成功",
  "success": true,
  "data": {
    "createdIds": [1, 2, 3],
    "count": 3
  }
}
```

---

## 三、社团相关接口

### 1. 添加社团

**接口**: `POST /api/clubs`

**请求参数**:
- `iconUrl`: 社团图标URL（可选）
- `name`: 社团名称（必填）
- `tags`: 社团标签（可选，多个标签用逗号分隔）
- `description`: 社团简介（可选）

**请求示例**:
```json
{
  "iconUrl": "https://example.com/club-icon.jpg",
  "name": "计算机协会",
  "tags": "技术,编程,计算机",
  "description": "致力于计算机技术交流与学习的社团"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "创建社团成功",
  "success": true,
  "data": {
    "club": {},
    "clubId": 1
  }
}
```

---

### 2. 根据社团ID获取社团信息

**接口**: `GET /api/clubs/{id}`

**路径参数**:
- `id`: 社团ID（必填）

**请求示例**:
```
GET /api/clubs/1
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "club": {
      "id": 1,
      "iconUrl": "https://example.com/club-icon.jpg",
      "name": "计算机协会",
      "tags": "技术,编程,计算机",
      "description": "致力于计算机技术交流与学习的社团",
      "status": 1,
      "levelTag": "校级",
      "memberCount": 35,
      "createTime": "2024-01-01T10:00:00",
      "updateTime": "2024-01-01T10:00:00"
    }
  }
}
```

**说明**:
- 返回指定ID的社团详细信息
- 包含社团人数（`memberCount`）
- 如果社团不存在，返回错误信息

---

### 3. 模糊查询社团列表

**接口**: `POST /api/clubs/search`

**请求参数**:
- `keyword`: 搜索关键词（可选），支持根据社团名称、标签或简介模糊查询
- `currentPage`: 当前页码，默认值为 1
- `pageSize`: 每页显示条数，默认值为 10

**请求示例**:
```json
{
  "keyword": "计算机",
  "currentPage": 1,
  "pageSize": 10
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "page": {
      "total": 10,
      "currentPage": 1,
      "pageSize": 10,
      "totalPage": 1,
      "records": [
        {
          "id": 1,
          "name": "计算机协会",
          "tags": "技术,编程,计算机",
          "description": "...",
          "memberCount": 35
        }
      ]
    }
  }
}
```

---

### 4. 加入社团

**接口**: `POST /api/clubs/join`

**请求参数**:
- `clubId`: 社团ID（必填）
- `userId`: 用户ID（必填）

**请求示例**:
```json
{
  "clubId": 1,
  "userId": 1
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "加入社团成功",
  "success": true,
  "data": {
    "clubMember": {}
  }
}
```

**错误响应**:
- 如果已经加入该社团，返回："您已经加入该社团"
- 如果社团不存在，返回："社团不存在"
- 如果社团已禁用，返回："该社团已禁用"

---

### 5. 模糊查询已加入的社团列表

**接口**: `POST /api/clubs/joined`

**请求参数**:
- `userId`: 用户ID（必填）
- `keyword`: 搜索关键词（可选），支持根据社团名称、标签或简介模糊查询
- `currentPage`: 当前页码，默认值为 1
- `pageSize`: 每页显示条数，默认值为 10

**请求示例**:
```json
{
  "userId": 1,
  "keyword": "计算机",
  "type": "join",        // join：我加入的；management：我管理的
  "currentPage": 1,
  "pageSize": 10
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "page": {
      "total": 5,
      "currentPage": 1,
      "pageSize": 10,
      "totalPage": 1,
      "records": [
        {
          "id": 1,
          "name": "计算机协会",
          "memberCount": 35
        }
      ]
    }
  }
}
```

---

### 6. 获取用户管理的社团下拉列表

**接口**: `GET /api/clubs/managed`

**请求参数** (查询参数):
- `userId`: 用户ID（必填）

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "items": [
      {
        "text": "社团名称",
        "value": 1
      }
    ]
  }
}
```

---

### 7. 获取社团成员列表

**接口**: `GET /api/clubs/{clubId}/members`

**路径参数**:
- `clubId`: 社团ID（必填）

**响应示例**（已调整为返回完整的用户信息）:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "clubId": 1,
        "userId": 1,
        "isManager": true,
        "joinTime": "2025-01-01T10:00:00",
        "user": {
          "id": 1,
          "username": "zhangsan",
          "realName": "张三",
          "studentNo": "20250001",
          "gender": 1,
          "phone": "13800000000",
          "email": "zhangsan@example.com",
          "schoolName": "XX大学",
          "collegeName": "计算机学院",
          "className": "计科1班",
          "avatarUrl": "https://example.com/avatar.jpg",
          "isCompleted": true,
          "isManager": false,
          "isBoss": false,
          "createTime": "2025-01-01T09:00:00",
          "updateTime": "2025-01-02T09:00:00"
        }
      }
    ]
  }
}
```

---

### 8. 设置社团人员为管理员 / 取消管理员

**接口**: `POST /api/clubs/{clubId}/members/{userId}/manager`

**路径参数**:
- `clubId`: 社团ID（必填）
- `userId`: 用户ID（必填）

**请求参数** (查询参数):
- `isManager`: 是否设置为管理员（true：设置为管理员，false：取消管理员），默认 true

**请求示例**:
```
POST /api/clubs/1/members/1/manager?isManager=true
```

**成功响应示例**:
```json
{
  "code": 200,
  "message": "设置管理员成功",
  "success": true,
  "data": {}
}
```

**失败场景说明**:
- 当该用户未加入该社团时，返回：`"该用户未加入该社团"`
- 当将某成员设置为管理员且其已是该社团管理员时，返回：`"该成员已是该社团的管理员"`

**说明**:
- 当 `isManager=true` 时：将该用户在该社团中的 `isManager` 标记为 true
- 当 `isManager=false` 时：将该用户在该社团中的 `isManager` 标记为 false
- 如果该用户未加入该社团，将返回错误提示

---

## 四、活动相关接口

### 1. 创建活动

**接口**: `POST /api/activities`

**说明**: 活动状态默认设置为 **审核中**，活动等级由主办方社团的 `levelTag` 决定。

**请求参数**:
```json
{
  "name": "活动名称",
  "description": "活动介绍",
  "activityType": "活动类型",
  "location": "活动地点",
  "clubId": 1,
  "notice": "参与须知",
  "registrationStartTime": "2025-12-20T09:00:00",
  "registrationEndTime": "2025-12-25T18:00:00",
  "startTime": "2025-12-26T09:00:00",
  "endTime": "2025-12-26T18:00:00",
  "maxParticipants": 100,
  "needAudit": true,
  "imageUrls": [
    "http://123.com/a.jpg",
    "http://123.com/b.jpg"
  ]
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "创建活动成功",
  "success": true,
  "data": {
    "activity": {}
  }
}
```

---

### 2. 获取待审核活动列表（由 isBoss = true 的用户审核）

**接口**: `GET /api/activities/pending`

**请求参数** (查询参数):
- `bossUserId`: 审核人用户ID（必填，需要 `isBoss = true`）
- `currentPage`: 当前页码（可选，默认 1）
- `pageSize`: 每页条数（可选，默认 10）

**请求示例**:
```
GET /api/activities/pending?bossUserId=1&currentPage=1&pageSize=10
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "page": {
      "total": 5,
      "currentPage": 1,
      "pageSize": 10,
      "totalPage": 1,
      "records": []
    }
  }
}
```

---

### 3. 审核活动

**接口**: `POST /api/activities/review`

**说明**: 由 `user.isBoss = true` 的用户对活动进行通过/拒绝审核。

**请求参数**:
```json
{
  "activityId": 1,
  "auditUserId": 1,
  "pass": true,
  "remark": "审核通过"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "success": true,
  "data": {}
}
```

---

### 4. 获取待审核人员列表（由主办方管理者审核）

**接口**: `GET /api/activities/{activityId}/registrations/pending`

**路径参数**:
- `activityId`: 活动ID（必填）

**请求参数** (查询参数):
- `managerUserId`: 管理员用户ID（必填，需要是该活动主办社团的管理员）

**请求示例**:
```
GET /api/activities/1/registrations/pending?managerUserId=2
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "activityId": 1,
        "userId": 3,
        "status": "待审核",
        "registrationTime": "2025-12-20T10:00:00"
      }
    ]
  }
}
```

---

### 5. 审核报名人员

**接口**: `POST /api/activities/registrations/review`

**说明**: 由活动主办方社团的管理员对报名人员进行通过/拒绝审核。

**请求参数**:
```json
{
  "activityId": 1,
  "userId": 3,
  "managerUserId": 2,
  "pass": true,
  "remark": "通过审核"
}
```

**参数说明**:
- `activityId`: 活动ID（必填）
- `userId`: 参加人员的用户ID（必填）
- `managerUserId`: 社团管理者用户ID（必填，需要是该活动主办社团的管理员）
- `pass`: 是否通过（必填，true-通过，false-拒绝）
- `remark`: 审核备注（可选）

**响应示例**:
```json
{
  "code": 200,
  "message": "审核成功",
  "success": true,
  "data": {}
}
```

**说明**:
- 通过活动ID和用户ID查找对应的报名记录进行审核
- 审核通过后，活动的 `currentParticipants` 字段会自动更新
- 如果报名记录不存在，返回错误信息

---

### 6. 模糊查询活动列表

**接口**: `POST /api/activities/search`

**说明**: 所有参数均为可选，如果都为空则返回所有活动列表。

**请求参数**:
```json
{
  "keyword": "关键字",
  "status": "审核中",
  "category": "活动分类",
  "level": "活动级别",
  "currentPage": 1,
  "pageSize": 10
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "page": {
      "total": 10,
      "currentPage": 1,
      "pageSize": 10,
      "totalPage": 1,
      "records": []
    }
  }
}
```

---

### 7. 获取热门活动列表

**接口**: `GET /api/activities/hot`

**说明**: 根据活动报名人数排序，返回前4个热门活动。只返回已通过审核的活动。

**请求参数**: 无

**请求示例**:
```
GET /api/activities/hot
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "activities": [
      {
        "id": 1,
        "name": "活动名称",
        "description": "活动描述",
        "location": "活动地点",
        "activityType": "活动类型",
        "activityLevel": "活动级别",
        "status": "报名中",
        "maxParticipants": 100,
        "currentParticipants": 85,
        "needAudit": true,
        "score": 95.5,
        "auditStatus": 1,
        "clubId": 1,
        "registrationStartTime": 1703059200000,
        "registrationEndTime": 1703145600000,
        "startTime": 1703232000000,
        "endTime": 1703318400000,
        "imageUrls": [
          "http://123.com/a.jpg",
          "http://123.com/b.jpg"
        ],
        "createTime": "2025-12-20T09:00:00",
        "updateTime": "2025-12-20T09:00:00"
      }
    ]
  }
}
```

**说明**:
- 只返回已通过审核的活动（`auditStatus = 1`）
- 按报名人数（`currentParticipants`）降序排序
- 最多返回4个活动
- `currentParticipants`: 当前已通过的报名人数（实时统计状态为"已通过"的报名记录）
- 活动状态会根据当前时间自动刷新（报名中/等待中/进行中/已结束）
- 如果符合条件的活动少于4个，则返回实际数量

---

### 8. 根据社团ID获取该社团的活动列表

**接口**: `GET /api/activities/club/{clubId}`

**路径参数**:
- `clubId`: 社团ID（必填）

**请求参数** (查询参数):
- `currentPage`: 当前页码（可选，默认 1）
- `pageSize`: 每页条数（可选，默认 10）

**请求示例**:
```
GET /api/activities/club/1?currentPage=1&pageSize=10
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "page": {
      "total": 10,
      "currentPage": 1,
      "pageSize": 10,
      "totalPage": 1,
      "records": [
        {
          "id": 1,
          "name": "活动名称",
          "description": "活动描述",
          "location": "活动地点",
          "activityType": "活动类型",
          "activityLevel": "活动级别",
          "status": "报名中",
          "maxParticipants": 100,
          "currentParticipants": 35,
          "needAudit": true,
          "score": 95.5,
          "auditStatus": 1,
          "clubId": 1,
          "registrationStartTime": 1703059200000,
          "registrationEndTime": 1703145600000,
          "startTime": 1703232000000,
          "endTime": 1703318400000,
          "imageUrls": [
            "http://123.com/a.jpg",
            "http://123.com/b.jpg"
          ],
          "createTime": "2025-12-20T09:00:00",
          "updateTime": "2025-12-20T09:00:00"
        }
      ]
    }
  }
}
```

**说明**:
- 返回指定社团的所有活动列表
- 按创建时间降序排序（最新的在前）
- 支持分页查询
- `currentParticipants`: 当前已通过的报名人数（实时统计状态为"已通过"的报名记录）
- 活动状态会根据当前时间自动刷新（报名中/等待中/进行中/已结束）
- 如果社团不存在，返回错误信息

---

### 9. 根据活动ID查看活动详情

**接口**: `GET /api/activities/{id}`

**路径参数**:
- `id`: 活动ID

**说明**: 返回活动实体信息，并额外返回解析好的图片URL数组。活动信息中包含 `currentParticipants` 字段，表示当前已通过的报名人数。

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "activity": {
      "id": 1,
      "name": "活动名称",
      "description": "活动描述",
      "maxParticipants": 100,
      "currentParticipants": 35,
      ...
    },
    "imageUrls": [
      "http://123.com/a.jpg",
      "http://123.com/b.jpg"
    ]
  }
}
```

**说明**:
- `currentParticipants`: 当前已通过的报名人数（统计状态为"已通过"的报名记录）
- 如果活动不存在，返回错误信息

---

### 10. 生成活动签到二维码

**接口**: `GET /api/activities/{activityId}/qrcode`

**说明**: 根据活动ID生成签到二维码，二维码内容为JSON格式：`{"activityId": 活动ID}`。前端小程序扫描二维码后，将二维码内容返回给后端进行签到验证。

**路径参数**:
- `activityId`: 活动ID（必填）

**请求示例**:
```
GET /api/activities/1/qrcode
```

**响应示例**:
```json
{
  "code": 200,
  "message": "生成二维码成功",
  "success": true,
  "data": {
    "qrcode": {
      "qrCode": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
      "activityId": 1,
      "activityName": "活动名称"
    }
  }
}
```

**说明**:
- `qrCode`: Base64编码的二维码图片（PNG格式），可直接用于前端显示
- `activityId`: 活动ID
- `activityName`: 活动名称
- 二维码内容为JSON字符串：`{"activityId": 1}`
- 如果活动不存在，返回错误信息

---

### 11. 扫码签到

**接口**: `POST /api/activities/checkin`

**说明**: 用户扫描二维码后，将二维码内容发送给后端进行签到验证。只有报名活动且审核通过的人员才能扫描签到，且只能在活动开始时间至活动结束时间之间签到。

**请求参数**（支持两种方式）:

**方式1**: 直接传递活动ID和用户ID
```json
{
  "activityId": 1,
  "userId": 3
}
```

**方式2**: 传递二维码内容和用户ID（推荐，小程序扫描后使用此方式）
```json
{
  "qrContent": "{\"activityId\":1}",
  "userId": 3
}
```

**请求示例**:
```json
{
  "qrContent": "{\"activityId\":1}",
  "userId": 3
}
```

**响应示例**（签到成功）:
```json
{
  "code": 200,
  "message": "签到成功",
  "success": true,
  "data": {
    "checkin": {
      "checkinId": 1,
      "checkinTime": 1703232000000,
      "activityName": "活动名称"
    }
  }
}
```

**响应示例**（签到失败 - 未报名）:
```json
{
  "code": 400,
  "message": "您未报名该活动，无法签到",
  "success": false,
  "data": {}
}
```

**响应示例**（签到失败 - 报名未通过审核）:
```json
{
  "code": 400,
  "message": "您的报名尚未通过审核，无法签到",
  "success": false,
  "data": {}
}
```

**响应示例**（签到失败 - 活动未开始）:
```json
{
  "code": 400,
  "message": "活动尚未开始，无法签到",
  "success": false,
  "data": {}
}
```

**响应示例**（签到失败 - 活动已结束）:
```json
{
  "code": 400,
  "message": "活动已结束，无法签到",
  "success": false,
  "data": {}
}
```

**响应示例**（签到失败 - 已签到）:
```json
{
  "code": 400,
  "message": "您已经签到过了",
  "success": false,
  "data": {}
}
```

**验证规则**:
1. 验证活动是否存在
2. 验证活动是否已通过审核（`auditStatus = 1`）
3. 验证用户是否报名了该活动
4. 验证用户报名状态是否为"已通过"
5. 验证当前时间是否在活动开始时间至活动结束时间之间
6. 防止重复签到（同一用户对同一活动只能签到一次）

**说明**:
- `checkinId`: 签到记录ID
- `checkinTime`: 签到时间（时间戳，毫秒）
- `activityName`: 活动名称
- 如果活动不存在，返回："活动不存在"
- 如果活动未通过审核，返回："活动尚未通过审核，无法签到"
- 如果用户未报名，返回："您未报名该活动，无法签到"
- 如果报名未通过审核，返回："您的报名尚未通过审核，无法签到"
- 如果活动时间未配置，返回："活动时间未配置，无法签到"
- 如果当前时间早于活动开始时间，返回："活动尚未开始，无法签到"
- 如果当前时间晚于活动结束时间，返回："活动已结束，无法签到"
- 如果已经签到过，返回："您已经签到过了"

---

### 12. 人员活动报名

**接口**: `POST /api/activities/{activityId}/register`

**路径参数**:
- `activityId`: 活动ID（必填）

**请求参数**:
```json
{
  "userId": 3
}
```

**说明**:
- 活动必须已通过审核才能报名；
- 报名时间必须在设置的报名时间范围内；
- 如果活动设置需要审核（`needAudit = true`），报名状态为 `"待审核"`，否则为 `"已通过"`。

**响应示例**:
```json
{
  "code": 200,
  "message": "报名成功",
  "success": true,
  "data": {
    "registration": {}
  }
}
```

---

### 13. 人员评价活动

**接口**: `POST /api/activities/comment`

**说明**: 当前仅支持评分（0-100），如需文字评价需在数据库中新增字段。

**请求参数**:
```json
{
  "activityId": 1,
  "userId": 3,
  "score": 95
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "评价成功",
  "success": true,
  "data": {}
}
```

---

### 14. 获取审核人员列表（由社团的管理者进行审核）

**接口**: `GET /api/activities/{activityId}/registrations/status`

**说明**: 由活动主办方社团的管理员查看待审核的报名人员列表，包含个人信息。时间字段返回时间戳（毫秒）。

**路径参数**:
- `activityId`: 活动ID（必填）

**请求参数** (查询参数):
- `managerUserId`: 管理者用户ID（必填，需要是该活动主办社团的管理员）

**请求示例**:
```
GET /api/activities/1/registrations/status?managerUserId=2
```

**响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "items": [
      {
        "id": 3,
        "username": "user001",
        "isCompleted": true,
        "realName": "张三",
        "studentNo": "2021001",
        "gender": 1,
        "phone": "13800138000",
        "email": "zhangsan@example.com",
        "schoolName": "XX大学",
        "collegeName": "计算机学院",
        "className": "计算机1班",
        "completeTime": 1703059200000,
        "isManager": false,
        "isBoss": false,
        "avatarUrl": "https://example.com/avatar.jpg",
        "createTime": 1703059200000,
        "updateTime": 1703059200000
      }
    ]
  }
}
```

**说明**:
- 只有该活动主办社团的管理员才能调用此接口
- 返回该活动下所有状态为"待审核"的报名人员列表
- 列表中每个元素为用户个人信息对象
- 时间字段（如 `completeTime`、`createTime`、`updateTime` 等）以时间戳（毫秒）形式返回
- 如果没有待审核人员，`items` 为空数组

---

### 15. 查询用户是否报名了某个活动及其审核状态

**接口**: `GET /api/activities/{activityId}/registrations/check`

**说明**: 根据活动ID和用户ID查询该用户是否报名了该活动，以及报名状态（待审核、已通过、已拒绝）。用于判断用户是否被录取。

**路径参数**:
- `activityId`: 活动ID（必填）

**请求参数** (查询参数):
- `userId`: 用户ID（必填）

**请求示例**:
```
GET /api/activities/1/registrations/check?userId=3
```

**响应示例**（已报名且已通过）:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "registration": {
      "isRegistered": true,
      "status": "已通过",
      "registrationId": 1,
      "registrationTime": 1703059200000,
      "auditTime": 1703059300000,
      "score": 95,
      "isAccepted": true
    }
  }
}
```

**响应示例**（已报名但待审核）:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "registration": {
      "isRegistered": true,
      "status": "待审核",
      "registrationId": 1,
      "registrationTime": 1703059200000,
      "auditTime": null,
      "score": null,
      "isAccepted": false
    }
  }
}
```

**响应示例**（未报名）:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "registration": {
      "isRegistered": false,
      "status": null
    }
  }
}
```

**说明**:
- `isRegistered`: 是否已报名（true/false）
- `status`: 报名状态（"待审核"、"已通过"、"已拒绝"），未报名时为 null
- `registrationId`: 报名记录ID，未报名时为 null
- `registrationTime`: 报名时间（时间戳，毫秒），未报名时为 null
- `auditTime`: 审核时间（时间戳，毫秒），未审核时为 null
- `score`: 评分（0-100），未评分时为 null
- `isAccepted`: 是否被录取（true/false），当 status 为"已通过"时为 true，其他情况为 false
- 如果活动不存在，返回错误信息

---

### 16. 根据用户ID获取用户参与或管理的社团活动

**接口**: `GET /api/activities/user/{userId}`

**说明**: 根据用户ID返回活动列表，可以通过 `type` 参数控制返回的内容：
1. **用户参与的活动**：用户通过报名参与的活动（通过 `activity_registration` 表查询）
2. **用户管理的活动**：用户作为社团管理员，其管理的社团发布的所有活动

**路径参数**:
- `userId`: 用户ID（必填）

**请求参数** (查询参数):
- `type`: 查询类型（可选，默认 `all`）
  - `participated`: 只返回用户参与的活动
  - `managed`: 只返回用户管理的活动
  - `all`: 返回两种活动（默认值）
- `keyword`: 搜索关键字（可选）
  - 用于模糊搜索活动名称和描述
  - 当提供关键字时，只返回名称或描述中包含该关键字的活动

**请求示例**（返回所有活动）:
```
GET /api/activities/user/1
或
GET /api/activities/user/1?type=all
```

**请求示例**（只返回参与的活动）:
```
GET /api/activities/user/1?type=participated
```

**请求示例**（只返回管理的活动）:
```
GET /api/activities/user/1?type=managed
```

**请求示例**（搜索包含关键字的参与活动）:
```
GET /api/activities/user/1?type=participated&keyword=科技
```

**请求示例**（搜索所有包含关键字的活动）:
```
GET /api/activities/user/1?keyword=讲座
```

**响应示例**（type=all 或不传type，返回两种活动）:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "participated": [
      {
        "id": 1,
        "name": "活动名称1",
        "description": "活动描述",
        "location": "活动地点",
        "activityType": "活动类型",
        "activityLevel": "活动级别",
        "status": "报名中",
        "maxParticipants": 100,
        "currentParticipants": 35,
        "needAudit": true,
        "score": 95.5,
        "auditStatus": 1,
        "clubId": 1,
        "registrationStartTime": 1703059200000,
        "registrationEndTime": 1703145600000,
        "startTime": 1703232000000,
        "endTime": 1703318400000,
        "imageUrls": [
          "http://123.com/a.jpg",
          "http://123.com/b.jpg"
        ],
        "createTime": "2025-12-20T09:00:00",
        "updateTime": "2025-12-20T09:00:00"
      }
    ],
    "managed": [
      {
        "id": 2,
        "name": "活动名称2",
        "description": "活动描述",
        "location": "活动地点",
        "activityType": "活动类型",
        "activityLevel": "活动级别",
        "status": "进行中",
        "maxParticipants": 50,
        "currentParticipants": 20,
        "needAudit": false,
        "score": 88.0,
        "auditStatus": 1,
        "clubId": 2,
        "registrationStartTime": 1703059200000,
        "registrationEndTime": 1703145600000,
        "startTime": 1703232000000,
        "endTime": 1703318400000,
        "imageUrls": [
          "http://123.com/c.jpg"
        ],
        "createTime": "2025-12-21T09:00:00",
        "updateTime": "2025-12-21T09:00:00"
      }
    ]
  }
}
```

**响应示例**（type=participated，只返回参与的活动）:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "activities": [
      {
        "id": 1,
        "name": "活动名称1",
        "description": "活动描述",
        "location": "活动地点",
        "activityType": "活动类型",
        "activityLevel": "活动级别",
        "status": "报名中",
        "maxParticipants": 100,
        "currentParticipants": 35,
        "needAudit": true,
        "score": 95.5,
        "auditStatus": 1,
        "clubId": 1,
        "registrationStartTime": 1703059200000,
        "registrationEndTime": 1703145600000,
        "startTime": 1703232000000,
        "endTime": 1703318400000,
        "imageUrls": [
          "http://123.com/a.jpg",
          "http://123.com/b.jpg"
        ],
        "createTime": "2025-12-20T09:00:00",
        "updateTime": "2025-12-20T09:00:00"
      }
    ]
  }
}
```

**响应示例**（type=managed，只返回管理的活动）:
```json
{
  "code": 200,
  "message": "查询成功",
  "success": true,
  "data": {
    "activities": [
      {
        "id": 2,
        "name": "活动名称2",
        "description": "活动描述",
        "location": "活动地点",
        "activityType": "活动类型",
        "activityLevel": "活动级别",
        "status": "进行中",
        "maxParticipants": 50,
        "currentParticipants": 20,
        "needAudit": false,
        "score": 88.0,
        "auditStatus": 1,
        "clubId": 2,
        "registrationStartTime": 1703059200000,
        "registrationEndTime": 1703145600000,
        "startTime": 1703232000000,
        "endTime": 1703318400000,
        "imageUrls": [
          "http://123.com/c.jpg"
        ],
        "createTime": "2025-12-21T09:00:00",
        "updateTime": "2025-12-21T09:00:00"
      }
    ]
  }
}
```

**说明**:
- `type` 参数说明：
  - `participated`: 只返回用户参与的活动，响应数据中 `activities` 字段包含参与的活动列表
  - `managed`: 只返回用户管理的活动，响应数据中 `activities` 字段包含管理的活动列表
  - `all` 或不传: 返回两种活动，响应数据中包含 `participated` 和 `managed` 两个字段
- `keyword` 参数说明：
  - 用于模糊搜索活动名称和描述
  - 不区分大小写
  - 支持部分匹配（如关键字"科技"会匹配"科技创新活动"和"科技前沿讲座"）
- `participated`: 用户参与的活动列表（通过报名记录查询）
- `managed`: 用户管理的活动列表（用户是社团管理员，查询这些社团发布的活动）
- 活动列表中的活动都会自动刷新状态（报名中/等待中/进行中/已结束）
- **活动列表排序规则**：优先显示进行中的活动，其他活动按创建时间倒序排列
- `currentParticipants`: 当前已通过的报名人数（实时统计状态为"已通过"的报名记录）
- `imageUrls`: 活动图片URL数组（从数据库中的逗号分隔字符串解析而来）
- 如果用户没有参与任何活动，`participated` 或 `activities` 为空数组
- 如果用户不是任何社团的管理员，`managed` 或 `activities` 为空数组
- 如果用户ID为空，返回错误信息
- 如果 `type` 参数值无效（不是 `participated`、`managed` 或 `all`），返回错误信息

---

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求失败（参数错误、业务错误等） |

