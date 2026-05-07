package com.example.projectsystem.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.projectsystem.commons.PageResult;
import com.example.projectsystem.commons.Results;
import com.example.projectsystem.domain.*;
import com.example.projectsystem.dto.*;
import com.example.projectsystem.service.*;
import com.example.projectsystem.util.QrCodeUtil;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.math.RoundingMode;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/activities")
public class ActivityController {

    private final ActivityService activityService;
    private final ActivityRegistrationService activityRegistrationService;
    private final ClubService clubService;
    private final ClubMemberService clubMemberService;
    private final UserService userService;
    private final ActivityCheckinService activityCheckinService;
    private final ObjectMapper objectMapper;

    public ActivityController(ActivityService activityService,
                              ActivityRegistrationService activityRegistrationService,
                              ClubService clubService,
                              ClubMemberService clubMemberService,
                              UserService userService,
                              ActivityCheckinService activityCheckinService,
                              ObjectMapper objectMapper) {
        this.activityService = activityService;
        this.activityRegistrationService = activityRegistrationService;
        this.clubService = clubService;
        this.clubMemberService = clubMemberService;
        this.userService = userService;
        this.activityCheckinService = activityCheckinService;
        this.objectMapper = objectMapper;
    }

    /**
     * 创建活动
     * 活动状态默认为“审核中”，活动等级由社团的 level_tag 决定
     */
    @PostMapping
    public Results createActivity(@RequestBody ActivityCreateRequest request) {
        try {
            if (!StringUtils.hasText(request.getName())) {
                return Results.fail().message("活动名称不能为空");
            }
            if (request.getClubId() == null) {
                return Results.fail().message("主办方社团ID不能为空");
            }

            Club club = clubService.getById(request.getClubId());
            if (club == null) {
                return Results.fail().message("主办方社团不存在");
            }

            Activity activity = new Activity();
            activity.setName(request.getName());
            activity.setDescription(request.getDescription());
            activity.setActivityType(request.getActivityType());
            activity.setLocation(request.getLocation());
            activity.setClubId(request.getClubId());
            activity.setNotice(request.getNotice());
            activity.setRegistrationStartTime(request.getRegistrationStartTime());
            activity.setRegistrationEndTime(request.getRegistrationEndTime());
            activity.setStartTime(request.getStartTime());
            activity.setEndTime(request.getEndTime());
            activity.setMaxParticipants(request.getMaxParticipants());
            activity.setNeedAudit(request.getNeedAudit() != null ? request.getNeedAudit() : Boolean.FALSE);

            // 图片 URL 数组用逗号拼接存储
            if (!CollectionUtils.isEmpty(request.getImageUrls())) {
                String joined = String.join(",", request.getImageUrls());
                activity.setImageUrls(joined);
            }

            Activity created = activityService.createActivity(activity);
            return Results.success()
                    .message("创建活动成功")
                    .data("activity", created);
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        } catch (Exception e) {
            return Results.fail().message("创建活动失败: " + e.getMessage());
        }
    }

    /**
     * 编辑已审核成功的活动
     * 只能编辑审核状态为已通过（audit_status = 1）的活动
     * 编辑后活动将重新进入审核状态（audit_status = 0，status = "审核中"）
     */
    @PutMapping("/update")
    public Results updateActivity(@RequestBody ActivityUpdateRequest request) {
        try {
            if (request.getActivityId() == null) {
                return Results.fail().message("活动ID不能为空");
            }
            if (request.getManagerUserId() == null) {
                return Results.fail().message("管理员用户ID不能为空");
            }

            // 查询活动
            Activity activity = activityService.getById(request.getActivityId());
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 校验是否为该社团管理员
            ClubMember member = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, activity.getClubId())
                    .eq(ClubMember::getUserId, request.getManagerUserId())
                    .one();
            if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                return Results.fail().message("无权限编辑该活动，您不是该活动主办社团的管理员");
            }

            // 更新活动信息（只更新提供的字段）
            if (StringUtils.hasText(request.getName())) {
                activity.setName(request.getName());
            }
            if (request.getDescription() != null) {
                activity.setDescription(request.getDescription());
            }
            if (request.getActivityType() != null) {
                activity.setActivityType(request.getActivityType());
            }
            if (request.getLocation() != null) {
                activity.setLocation(request.getLocation());
            }
            if (request.getNotice() != null) {
                activity.setNotice(request.getNotice());
            }
            if (request.getRegistrationStartTime() != null) {
                activity.setRegistrationStartTime(request.getRegistrationStartTime());
            }
            if (request.getRegistrationEndTime() != null) {
                activity.setRegistrationEndTime(request.getRegistrationEndTime());
            }
            if (request.getStartTime() != null) {
                activity.setStartTime(request.getStartTime());
            }
            if (request.getEndTime() != null) {
                activity.setEndTime(request.getEndTime());
            }
            if (request.getMaxParticipants() != null) {
                activity.setMaxParticipants(request.getMaxParticipants());
            }
            if (request.getNeedAudit() != null) {
                activity.setNeedAudit(request.getNeedAudit());
            }
            if (request.getImageUrls() != null) {
                // 图片 URL 数组用逗号拼接存储
                if (!CollectionUtils.isEmpty(request.getImageUrls())) {
                    String joined = String.join(",", request.getImageUrls());
                    activity.setImageUrls(joined);
                } else {
                    activity.setImageUrls(null);
                }
            }

            // 编辑后重新进入审核状态
            activity.setAuditStatus(0); // 待审核
            activity.setStatus("审核中");
            activity.setAuditUserId(null);
            activity.setAuditTime(null);

            activityService.updateById(activity);

            return Results.success()
                    .message("编辑活动成功，活动已重新进入审核状态")
                    .data("activity", activity);
        } catch (Exception e) {
            return Results.fail().message("编辑活动失败: " + e.getMessage());
        }
    }

    /**
     * 获取待审核活动列表（由 isBoss = true 的用户查看）
     */
    @GetMapping("/pending")
    public Results getPendingActivities(@RequestParam("bossUserId") Long bossUserId,
                                        @RequestParam(value = "currentPage", defaultValue = "1") Integer currentPage,
                                        @RequestParam(value = "pageSize", defaultValue = "10") Integer pageSize) {
        try {
            User user = userService.getById(bossUserId);
            if (user == null || user.getIsBoss() == null || !user.getIsBoss()) {
                return Results.fail().message("无权限查看待审核活动");
            }

            Page<Activity> page = new Page<>(currentPage, pageSize);
            LambdaQueryWrapper<Activity> wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(Activity::getAuditStatus, 0); // 待审核
            wrapper.orderByDesc(Activity::getCreateTime);

            IPage<Activity> result = activityService.page(page, wrapper);
            
            // 转换为 DTO，将 imageUrls 字符串转换为数组，时间转换为时间戳
            List<ActivityDTO> activityDTOs = result.getRecords().stream()
                    .map(activity -> {
                        ActivityDTO dto = new ActivityDTO(activity);
                        // 将 imageUrls 字符串转换为数组
                        if (StringUtils.hasText(activity.getImageUrls())) {
                            List<String> urls = Arrays.stream(activity.getImageUrls().split(","))
                                    .map(String::trim)
                                    .filter(StringUtils::hasText)
                                    .collect(Collectors.toList());
                            dto.setImageUrls(urls);
                        } else {
                            dto.setImageUrls(new ArrayList<>());
                        }
                        return dto;
                    })
                    .collect(Collectors.toList());
            
            PageResult<ActivityDTO> pageData = new PageResult<>(
                    result.getTotal(),
                    (int) result.getCurrent(),
                    (int) result.getSize(),
                    activityDTOs);

            return Results.success()
                    .message("查询成功")
                    .data("page", pageData);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 审核活动（由 isBoss = true 的用户进行）
     */
    @PostMapping("/review")
    public Results reviewActivity(@RequestBody ActivityReviewRequest request) {
        try {
            if (request.getActivityId() == null || request.getAuditUserId() == null || request.getPass() == null) {
                return Results.fail().message("参数不完整");
            }
            User user = userService.getById(request.getAuditUserId());
            if (user == null || user.getIsBoss() == null || !user.getIsBoss()) {
                return Results.fail().message("无审核权限");
            }

            Activity activity = activityService.getById(request.getActivityId());
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            if (Boolean.TRUE.equals(request.getPass())) {
                activity.setAuditStatus(1);
            } else {
                activity.setAuditStatus(2);
                activity.setStatus("已拒绝");
            }
            activity.setAuditUserId(request.getAuditUserId());
            activity.setAuditTime(LocalDateTime.now());

            // 审核通过后，根据时间刷新活动状态（报名中 / 等待中 / 进行中 / 已结束）
            if (activity.getAuditStatus() != null && activity.getAuditStatus() == 1) {
                refreshActivityStatusByTime(activity);
            } else {
                activityService.updateById(activity);
            }
            return Results.success().message("审核成功");
        } catch (Exception e) {
            return Results.fail().message("审核失败: " + e.getMessage());
        }
    }

    /**
     * 获取某活动下待审核的报名人员（由主办方的管理者进行审核）
     */
    @GetMapping("/{activityId}/registrations/pending")
    public Results getPendingRegistrations(@PathVariable Long activityId,
                                           @RequestParam("managerUserId") Long managerUserId) {
        try {
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 校验是否为该社团管理员
            Long clubId = activity.getClubId();
            ClubMember member = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, clubId)
                    .eq(ClubMember::getUserId, managerUserId)
                    .one();
            if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                return Results.fail().message("无权限查看该活动报名信息");
            }

            List<ActivityRegistration> list = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "待审核")
                    .orderByAsc(ActivityRegistration::getRegistrationTime)
                    .list();

            return Results.success()
                    .message("查询成功")
                    .data("items", list);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 审核报名人员（通过/拒绝）
     */
    @PostMapping("/registrations/review")
    public Results reviewRegistration(@RequestBody RegistrationReviewRequest request) {
        try {
            if (request.getActivityId() == null
                    || request.getUserId() == null
                    || request.getManagerUserId() == null
                    || request.getPass() == null) {
                return Results.fail().message("参数不完整");
            }

            Activity activity = activityService.getById(request.getActivityId());
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 校验是否为该社团管理员
            ClubMember member = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, activity.getClubId())
                    .eq(ClubMember::getUserId, request.getManagerUserId())
                    .one();
            if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                return Results.fail().message("无审核权限");
            }

            // 通过活动ID和用户ID查找报名记录
            ActivityRegistration registration = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, request.getActivityId())
                    .eq(ActivityRegistration::getUserId, request.getUserId())
                    .one();
            if (registration == null) {
                return Results.fail().message("报名记录不存在");
            }

            String oldStatus = registration.getStatus();
            if (Boolean.TRUE.equals(request.getPass())) {
                registration.setStatus("已通过");
            } else {
                registration.setStatus("已拒绝");
            }
            registration.setAuditUserId(request.getManagerUserId());
            registration.setAuditTime(LocalDateTime.now());

            activityRegistrationService.updateById(registration);

            // 更新活动的当前报名人数（只统计已通过的）
            if (Boolean.TRUE.equals(request.getPass()) && !"已通过".equals(oldStatus)) {
                // 审核通过，且之前不是已通过状态，增加人数
                long approvedCount = activityRegistrationService.lambdaQuery()
                        .eq(ActivityRegistration::getActivityId, request.getActivityId())
                        .eq(ActivityRegistration::getStatus, "已通过")
                        .count();
                activity.setCurrentParticipants((int) approvedCount);
                activityService.updateById(activity);
            } else if (!Boolean.TRUE.equals(request.getPass()) && "已通过".equals(oldStatus)) {
                // 审核拒绝，且之前是已通过状态，减少人数
                long approvedCount = activityRegistrationService.lambdaQuery()
                        .eq(ActivityRegistration::getActivityId, request.getActivityId())
                        .eq(ActivityRegistration::getStatus, "已通过")
                        .count();
                activity.setCurrentParticipants((int) approvedCount);
                activityService.updateById(activity);
            }

            return Results.success().message("审核成功");
        } catch (Exception e) {
            return Results.fail().message("审核失败: " + e.getMessage());
        }
    }

    /**
     * 模糊查询活动列表
     * 请求参数均为可选，如果都为空，则返回所有活动
     */
    @PostMapping("/search")
    public Results searchActivities(@RequestBody ActivitySearchRequest request) {
        try {
            Integer currentPage = request.getCurrentPage() != null && request.getCurrentPage() > 0
                    ? request.getCurrentPage() : 1;
            Integer pageSize = request.getPageSize() != null && request.getPageSize() > 0
                    ? request.getPageSize() : 10;

            Page<Activity> page = new Page<>(currentPage, pageSize);
            LambdaQueryWrapper<Activity> wrapper = new LambdaQueryWrapper<>();

            // 排除已拒绝的活动（auditStatus = 2）
            wrapper.ne(Activity::getAuditStatus, 2);
            // 只查询已上架的活动
            wrapper.eq(Activity::getIsPublished, true);

            if (StringUtils.hasText(request.getKeyword())) {
                wrapper.and(w -> w
                        .like(Activity::getName, request.getKeyword())
                        .or()
                        .like(Activity::getDescription, request.getKeyword())
                        .or()
                        .like(Activity::getLocation, request.getKeyword())
                );
            }
            if (StringUtils.hasText(request.getStatus())) {
                wrapper.eq(Activity::getStatus, request.getStatus());
            }
            if (StringUtils.hasText(request.getCategory())) {
                wrapper.eq(Activity::getActivityType, request.getCategory());
            }
            if (StringUtils.hasText(request.getLevel())) {
                wrapper.eq(Activity::getActivityLevel, request.getLevel());
            }

            wrapper.orderByDesc(Activity::getCreateTime);

            IPage<Activity> result = activityService.page(page, wrapper);
            // 查询时根据当前时间刷新每个活动的状态
            for (Activity activity : result.getRecords()) {
                refreshActivityStatusByTime(activity);
            }
            
            // 转换为 DTO，将 imageUrls 字符串转换为数组
            List<ActivityDTO> activityDTOs = result.getRecords().stream()
                    .map(activity -> {
                        ActivityDTO dto = new ActivityDTO(activity);
                        // 将 imageUrls 字符串转换为数组
                        if (StringUtils.hasText(activity.getImageUrls())) {
                            List<String> urls = Arrays.stream(activity.getImageUrls().split(","))
                                    .map(String::trim)
                                    .filter(StringUtils::hasText)
                                    .collect(Collectors.toList());
                            dto.setImageUrls(urls);
                        } else {
                            dto.setImageUrls(new ArrayList<>());
                        }
                        return dto;
                    })
                    .collect(Collectors.toList());
            
            PageResult<ActivityDTO> pageData = new PageResult<>(
                    result.getTotal(),
                    (int) result.getCurrent(),
                    (int) result.getSize(),
                    activityDTOs
            );

            return Results.success()
                    .message("查询成功")
                    .data("page", pageData);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 获取热门活动列表（根据报名人数排序，返回前6个）
     * 优先返回报名中 > 进行中 > 已结束状态的活动
     */
    @GetMapping("/hot")
    public Results getHotActivities() {
        try {
            LambdaQueryWrapper<Activity> wrapper = new LambdaQueryWrapper<>();
            // 只查询已通过审核且已上架的活动
            wrapper.eq(Activity::getAuditStatus, 1);
            wrapper.eq(Activity::getIsPublished, true);
            
            List<Activity> activities = activityService.list(wrapper);
            
            // 统计每个活动的实际报名人数并更新状态
            for (Activity activity : activities) {
                long participantCount = activityRegistrationService.lambdaQuery()
                        .eq(ActivityRegistration::getActivityId, activity.getId())
                        .eq(ActivityRegistration::getStatus, "已通过")
                        .count();
                activity.setCurrentParticipants((int) participantCount);
                // 刷新活动状态
                refreshActivityStatusByTime(activity);
            }
            
            // 按状态优先级和报名人数降序排序：报名中 > 进行中 > 已结束，取前6个
            List<Activity> hotActivities = activities.stream()
                    .filter(activity -> "报名中".equals(activity.getStatus()) || "进行中".equals(activity.getStatus()) || "已结束".equals(activity.getStatus()))
                    .sorted((a1, a2) -> {
                        int count1 = a1.getCurrentParticipants() != null ? a1.getCurrentParticipants() : 0;
                        int count2 = a2.getCurrentParticipants() != null ? a2.getCurrentParticipants() : 0;
                        // 优先按状态排序：报名中(1) > 进行中(2) > 已结束(3)
                        int statusPriority1 = getStatusPriority(a1.getStatus());
                        int statusPriority2 = getStatusPriority(a2.getStatus());
                        if (statusPriority1 != statusPriority2) {
                            return Integer.compare(statusPriority1, statusPriority2);
                        }
                        // 同状态按报名人数降序
                        return Integer.compare(count2, count1);
                    })
                    .limit(6)
                    .collect(Collectors.toList());
            
            // 转换为 DTO，将 imageUrls 字符串转换为数组
            List<ActivityDTO> activityDTOs = hotActivities.stream()
                    .map(activity -> {
                        ActivityDTO dto = new ActivityDTO(activity);
                        // 将 imageUrls 字符串转换为数组
                        if (StringUtils.hasText(activity.getImageUrls())) {
                            List<String> urls = Arrays.stream(activity.getImageUrls().split(","))
                                    .map(String::trim)
                                    .filter(StringUtils::hasText)
                                    .collect(Collectors.toList());
                            dto.setImageUrls(urls);
                        } else {
                            dto.setImageUrls(new ArrayList<>());
                        }
                        return dto;
                    })
                    .collect(Collectors.toList());
            
            return Results.success()
                    .message("查询成功")
                    .data("activities", activityDTOs);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 根据社团ID获取该社团的活动列表
     */
    @GetMapping("/club/{clubId}")
    public Results getActivitiesByClubId(@PathVariable Long clubId,
                                        @RequestParam(value = "currentPage", defaultValue = "1") Integer currentPage,
                                        @RequestParam(value = "pageSize", defaultValue = "10") Integer pageSize) {
        try {
            // 验证社团是否存在
            Club club = clubService.getById(clubId);
            if (club == null) {
                return Results.fail().message("社团不存在");
            }

            Page<Activity> page = new Page<>(currentPage, pageSize);
            LambdaQueryWrapper<Activity> wrapper = new LambdaQueryWrapper<>();
            wrapper.eq(Activity::getClubId, clubId);
            // 只查询已上架的活动
            wrapper.eq(Activity::getIsPublished, true);
            wrapper.orderByDesc(Activity::getCreateTime);

            IPage<Activity> result = activityService.page(page, wrapper);
            
            // 查询时根据当前时间刷新每个活动的状态
            for (Activity activity : result.getRecords()) {
                refreshActivityStatusByTime(activity);
                // 统计已通过的报名人数
                long participantCount = activityRegistrationService.lambdaQuery()
                        .eq(ActivityRegistration::getActivityId, activity.getId())
                        .eq(ActivityRegistration::getStatus, "已通过")
                        .count();
                activity.setCurrentParticipants((int) participantCount);
            }
            
            // 转换为 DTO，将 imageUrls 字符串转换为数组
            List<ActivityDTO> activityDTOs = result.getRecords().stream()
                    .map(activity -> {
                        ActivityDTO dto = new ActivityDTO(activity);
                        // 将 imageUrls 字符串转换为数组
                        if (StringUtils.hasText(activity.getImageUrls())) {
                            List<String> urls = Arrays.stream(activity.getImageUrls().split(","))
                                    .map(String::trim)
                                    .filter(StringUtils::hasText)
                                    .collect(Collectors.toList());
                            dto.setImageUrls(urls);
                        } else {
                            dto.setImageUrls(new ArrayList<>());
                        }
                        return dto;
                    })
                    .collect(Collectors.toList());
            
            PageResult<ActivityDTO> pageData = new PageResult<>(
                    result.getTotal(),
                    (int) result.getCurrent(),
                    (int) result.getSize(),
                    activityDTOs
            );

            return Results.success()
                    .message("查询成功")
                    .data("page", pageData);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 根据活动ID查看活动详情
     */
    @GetMapping("/{id}")
    public Results getActivityDetail(@PathVariable Long id,
                                    @RequestParam(value = "managerUserId", required = false) Long managerUserId) {
        try {
            Activity activity = activityService.getById(id);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 允许查看所有活动的详情，不管是否上架
            // 上架/下架状态只影响活动列表的显示，不影响查看详情

            // 进入详情时也根据时间刷新一次状态
            refreshActivityStatusByTime(activity);

            // 统计已通过的报名人数
            long participantCount = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, id)
                    .eq(ActivityRegistration::getStatus, "已通过")
                    .count();
            activity.setCurrentParticipants((int) participantCount);

            // 创建包含时间戳的活动响应对象
            Map<String, Object> activityMap = new HashMap<>();
            activityMap.put("id", activity.getId());
            activityMap.put("name", activity.getName());
            activityMap.put("clubId", activity.getClubId());
            activityMap.put("description", activity.getDescription());
            activityMap.put("location", activity.getLocation());
            activityMap.put("notice", activity.getNotice());
            // 将时间字段转换为时间戳（毫秒）
            activityMap.put("registrationStartTime", activity.getRegistrationStartTime() != null
                    ? activity.getRegistrationStartTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
                    : null);
            activityMap.put("registrationEndTime", activity.getRegistrationEndTime() != null
                    ? activity.getRegistrationEndTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
                    : null);
            activityMap.put("startTime", activity.getStartTime() != null
                    ? activity.getStartTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
                    : null);
            activityMap.put("endTime", activity.getEndTime() != null
                    ? activity.getEndTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
                    : null);
            activityMap.put("maxParticipants", activity.getMaxParticipants());
            activityMap.put("currentParticipants", activity.getCurrentParticipants());
            activityMap.put("needAudit", activity.getNeedAudit());
            activityMap.put("activityType", activity.getActivityType());
            activityMap.put("activityLevel", activity.getActivityLevel());
            activityMap.put("status", activity.getStatus());
            activityMap.put("score", activity.getScore());
            activityMap.put("auditStatus", activity.getAuditStatus());
            activityMap.put("auditTime", activity.getAuditTime());
            activityMap.put("auditUserId", activity.getAuditUserId());
            activityMap.put("isPublished", activity.getIsPublished());
            activityMap.put("createTime", activity.getCreateTime());
            activityMap.put("updateTime", activity.getUpdateTime());

            // 查询进行了文字评价的成员列表
            List<ActivityRegistration> commentedRegistrations = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, id)
                    .eq(ActivityRegistration::getStatus, "已通过")
                    .isNotNull(ActivityRegistration::getComment)
                    .ne(ActivityRegistration::getComment, "")
                    .list();
            
            List<Map<String, Object>> commentedMembers = new ArrayList<>();
            for (ActivityRegistration reg : commentedRegistrations) {
                User user = userService.getById(reg.getUserId());
                if (user != null) {
                    Map<String, Object> memberInfo = new HashMap<>();
                    memberInfo.put("userId", user.getId());
                    memberInfo.put("realName", user.getRealName());
                    memberInfo.put("studentNo", user.getStudentNo());
                    memberInfo.put("avatarUrl", user.getAvatarUrl());
                    memberInfo.put("comment", reg.getComment());
                    memberInfo.put("score", reg.getScore());
                    // 添加评论时间戳（毫秒）
                    memberInfo.put("commentTime", reg.getUpdateTime() != null
                            ? reg.getUpdateTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
                            : null);
                    commentedMembers.add(memberInfo);
                }
            }
            activityMap.put("commentedMembers", commentedMembers);

            // 解析图片 URL 数组给前端更友好一些
            if (StringUtils.hasText(activity.getImageUrls())) {
                List<String> urls = Arrays.stream(activity.getImageUrls().split(","))
                        .map(String::trim)
                        .filter(StringUtils::hasText)
                        .collect(Collectors.toList());
                return Results.success()
                        .message("查询成功")
                        .data("activity", activityMap)
                        .data("imageUrls", urls);
            }

            return Results.success()
                    .message("查询成功")
                    .data("activity", activityMap);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 人员活动报名
     */
    @PostMapping("/{activityId}/register")
    public Results registerActivity(@PathVariable Long activityId,
                                    @RequestBody ActivityRegisterRequest request) {
        try {
            if (request.getUserId() == null) {
                return Results.fail().message("用户ID不能为空");
            }

            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }
            if (activity.getAuditStatus() == null || activity.getAuditStatus() != 1) {
                return Results.fail().message("活动尚未通过审核，无法报名");
            }
            if (!Boolean.TRUE.equals(activity.getIsPublished())) {
                return Results.fail().message("活动已下架，无法报名");
            }

            // 报名时间范围校验
            LocalDateTime now = LocalDateTime.now();
            if (activity.getRegistrationStartTime() == null
                    || activity.getRegistrationEndTime() == null) {
                return Results.fail().message("活动报名时间未配置，无法报名");
            }
            if (now.isBefore(activity.getRegistrationStartTime())
                    || now.isAfter(activity.getRegistrationEndTime())) {
                return Results.fail().message("当前不在报名时间范围内");
            }

            // 检查是否已报名
            ActivityRegistration existing = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getUserId, request.getUserId())
                    .one();
            if (existing != null) {
                return Results.fail().message("您已报名该活动");
            }

            // 检查人数上限（只统计已通过的）
            if (activity.getMaxParticipants() != null && activity.getMaxParticipants() > 0) {
                long approvedCount = activityRegistrationService.lambdaQuery()
                        .eq(ActivityRegistration::getActivityId, activityId)
                        .eq(ActivityRegistration::getStatus, "已通过")
                        .count();
                if (approvedCount >= activity.getMaxParticipants()) {
                    return Results.fail().message("报名人数已达上限");
                }
            }

            ActivityRegistration registration = new ActivityRegistration();
            registration.setActivityId(activityId);
            registration.setUserId(request.getUserId());
            // 不需要审核则直接标记为已通过，否则为待审核
            if (Boolean.TRUE.equals(activity.getNeedAudit())) {
                registration.setStatus("待审核");
            } else {
                registration.setStatus("已通过");
            }
            registration.setRegistrationTime(LocalDateTime.now());

            activityRegistrationService.save(registration);

            // 如果不需要审核直接通过，更新活动的当前报名人数
            if (!Boolean.TRUE.equals(activity.getNeedAudit())) {
                long approvedCount = activityRegistrationService.lambdaQuery()
                        .eq(ActivityRegistration::getActivityId, activityId)
                        .eq(ActivityRegistration::getStatus, "已通过")
                        .count();
                activity.setCurrentParticipants((int) approvedCount);
                activityService.updateById(activity);
            }

            return Results.success()
                    .message("报名成功")
                    .data("registration", registration);
        } catch (Exception e) {
            return Results.fail().message("报名失败: " + e.getMessage());
        }
    }

    /**
     * 人员评价活动（支持评分和文字评价）
     */
    @PostMapping("/comment")
    public Results commentActivity(@RequestBody ActivityCommentRequest request) {
        try {
            if (request.getActivityId() == null || request.getUserId() == null) {
                return Results.fail().message("参数不完整");
            }
            // 评分和文字评价至少需要提供一个
            if (request.getScore() == null && (request.getComment() == null || request.getComment().trim().isEmpty())) {
                return Results.fail().message("请至少提供评分或文字评价");
            }
            Activity activity = activityService.getById(request.getActivityId());
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 只能在活动结束后进行评分
            if (activity.getEndTime() == null) {
                return Results.fail().message("活动结束时间未配置，无法评分");
            }
            LocalDateTime now = LocalDateTime.now();
            if (!now.isAfter(activity.getEndTime())) {
                return Results.fail().message("活动结束后才能进行评分");
            }

            ActivityRegistration registration = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, request.getActivityId())
                    .eq(ActivityRegistration::getUserId, request.getUserId())
                    .one();
            if (registration == null) {
                return Results.fail().message("未找到报名记录，不能评价");
            }
            if (!"已通过".equals(registration.getStatus())) {
                return Results.fail().message("报名未通过，不能评价");
            }

            // 检查用户是否已签到（必须是活动结束且已签到的成员才能评价）
            ActivityCheckin checkin = activityCheckinService.lambdaQuery()
                    .eq(ActivityCheckin::getActivityId, request.getActivityId())
                    .eq(ActivityCheckin::getUserId, request.getUserId())
                    .one();
            if (checkin == null) {
                return Results.fail().message("您未签到该活动，不能评价");
            }

            // Check if the user has already commented
            if (registration.getScore() != null || (registration.getComment() != null && !registration.getComment().trim().isEmpty())) {
                return Results.fail().message("您已经评价过该活动，不能重复评价");
            }

            // 处理评分
            if (request.getScore() != null) {
                BigDecimal score = request.getScore();
                if (score.compareTo(BigDecimal.ZERO) < 0 || score.compareTo(new BigDecimal("5")) > 0) {
                    return Results.fail().message("评分范围应在0-5之间");
                }
                registration.setScore(score);
            }

            // 处理文字评价
            if (request.getComment() != null && !request.getComment().trim().isEmpty()) {
                String comment = request.getComment().trim();
                // 限制文字评价长度，例如最多1000字符
                if (comment.length() > 1000) {
                    return Results.fail().message("文字评价不能超过1000字符");
                }
                registration.setComment(comment);
            }

            activityRegistrationService.updateById(registration);

            // 计算活动平均评分（仅统计已通过且已评分的报名记录），保留1位小数
            List<ActivityRegistration> scoredList = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, request.getActivityId())
                    .eq(ActivityRegistration::getStatus, "已通过")
                    .isNotNull(ActivityRegistration::getScore)
                    .list();
            if (!scoredList.isEmpty()) {
                BigDecimal totalScore = scoredList.stream()
                        .map(ActivityRegistration::getScore)
                        .reduce(BigDecimal.ZERO, BigDecimal::add);
                BigDecimal averageScore = totalScore.divide(
                        BigDecimal.valueOf(scoredList.size()), 1, RoundingMode.HALF_UP);
                activity.setScore(averageScore);
            } else {
                activity.setScore(BigDecimal.ZERO);
            }
            activityService.updateById(activity);

            return Results.success().message("评价成功");
        } catch (Exception e) {
            return Results.fail().message("评价失败: " + e.getMessage());
        }
    }

    /**
     * 获取审核人员列表（由社团的管理者进行审核）
     * 返回待审核人员列表，包含个人信息
     */
    @GetMapping("/{activityId}/registrations/status")
    public Results getRegistrationStatus(@PathVariable Long activityId,
                                         @RequestParam("managerUserId") Long managerUserId) {
        try {
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 校验是否为该社团管理员
            Long clubId = activity.getClubId();
            ClubMember member = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, clubId)
                    .eq(ClubMember::getUserId, managerUserId)
                    .one();
            if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                return Results.fail().message("无权限查看该活动报名信息");
            }

            // 查询所有待审核的报名记录
            List<ActivityRegistration> registrations = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "待审核")
                    .orderByAsc(ActivityRegistration::getRegistrationTime)
                    .list();

            if (registrations.isEmpty()) {
                return Results.success()
                        .message("查询成功")
                        .data("items", new ArrayList<>());
            }

            // 批量查询用户信息
            List<Long> userIds = registrations.stream()
                    .map(ActivityRegistration::getUserId)
                    .distinct()
                    .collect(Collectors.toList());
            List<User> users = userService.listByIds(userIds);

            // 转换为 DTO，时间字段转换为时间戳
            List<UserDTO> resultList = users.stream()
                    .map(UserDTO::new)
                    .collect(Collectors.toList());

            return Results.success()
                    .message("查询成功")
                    .data("items", resultList);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 查询用户是否报名了某个活动及其审核状态
     * 根据活动ID和用户ID查询报名状态（待审核、已通过、已拒绝、签到成功）
     */
    @GetMapping("/{activityId}/registrations/check")
    public Results checkUserRegistration(@PathVariable Long activityId,
                                        @RequestParam("userId") Long userId) {
        try {
            // 验证活动是否存在
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 查询报名记录
            ActivityRegistration registration = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getUserId, userId)
                    .one();

            // 构建返回结果
            Map<String, Object> result = new HashMap<>();
            if (registration == null) {
                // 未报名
                result.put("isRegistered", false);
                result.put("status", null);
            } else {
                // 已报名，判断状态
                String status = registration.getStatus();
                
                // 如果状态是"已通过"，检查是否已签到
                if ("已通过".equals(status)) {
                    ActivityCheckin checkin = activityCheckinService.lambdaQuery()
                            .eq(ActivityCheckin::getActivityId, activityId)
                            .eq(ActivityCheckin::getUserId, userId)
                            .one();
                    
                    // 如果已签到，状态改为"签到成功"
                    if (checkin != null) {
                        status = "签到成功";
                    }
                }
                
                result.put("isRegistered", true);
                result.put("status", status);
                result.put("registrationId", registration.getId());
                result.put("registrationTime", registration.getRegistrationTime() != null
                        ? registration.getRegistrationTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
                        : null);
                result.put("auditTime", registration.getAuditTime() != null
                        ? registration.getAuditTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
                        : null);
                result.put("score", registration.getScore());
                // 判断是否被录取（状态为"已通过"或"签到成功"）
                result.put("isAccepted", "已通过".equals(registration.getStatus()) || "签到成功".equals(status));
            }

            return Results.success()
                    .message("查询成功")
                    .data("registration", result);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 获取单个活动的报名状态统计（用于ECharts饼图）
     */
    @GetMapping("/{activityId}/statistics")
    public Results getActivityStatistics(@PathVariable Long activityId,
                                         @RequestParam("managerUserId") Long managerUserId) {
        try {
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 校验是否为该社团管理员
            ClubMember member = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, activity.getClubId())
                    .eq(ClubMember::getUserId, managerUserId)
                    .one();
            if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                return Results.fail().message("无权限查看该活动统计信息");
            }

            // 报名状态统计
            Map<String, Object> statusStats = new HashMap<>();
            
            // 各状态报名人数
            long pendingCount = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "待审核")
                    .count();
            long approvedCount = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "已通过")
                    .count();
            long rejectedCount = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "已拒绝")
                    .count();
            
            statusStats.put("pending", pendingCount);
            statusStats.put("approved", approvedCount);
            statusStats.put("rejected", rejectedCount);
            statusStats.put("total", pendingCount + approvedCount + rejectedCount);

            // 报名成功率统计
            double successRate = 0.0;
            long totalRegistrations = pendingCount + approvedCount + rejectedCount;
            if (totalRegistrations > 0) {
                successRate = (double) approvedCount / totalRegistrations * 100;
                successRate = new BigDecimal(successRate).setScale(2, RoundingMode.HALF_UP).doubleValue();
            }

            // 构建返回数据
            Map<String, Object> statistics = new HashMap<>();
            statistics.put("activityInfo", new ActivityDTO(activity));
            statistics.put("statusStats", statusStats);
            statistics.put("successRate", successRate);
            statistics.put("maxParticipants", activity.getMaxParticipants());
            statistics.put("currentParticipants", activity.getCurrentParticipants());

            return Results.success()
                    .message("查询成功")
                    .data("statistics", statistics);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 获取单个活动的签到统计（用于ECharts饼图）
     */
    @GetMapping("/{activityId}/checkin-statistics")
    public Results getCheckinStatistics(@PathVariable Long activityId,
                                       @RequestParam("managerUserId") Long managerUserId) {
        try {
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 校验是否为该社团管理员
            ClubMember member = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, activity.getClubId())
                    .eq(ClubMember::getUserId, managerUserId)
                    .one();
            if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                return Results.fail().message("无权限查看该活动统计信息");
            }

            // 统计已通过审核的报名人数（这些人有资格签到）
            long approvedCount = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "已通过")
                    .count();

            // 统计已签到人数
            long checkedInCount = activityCheckinService.lambdaQuery()
                    .eq(ActivityCheckin::getActivityId, activityId)
                    .count();

            // 未签到人数 = 已通过审核人数 - 已签到人数
            long notCheckedInCount = approvedCount - checkedInCount;

            // 签到率
            double checkinRate = 0.0;
            if (approvedCount > 0) {
                checkinRate = (double) checkedInCount / approvedCount * 100;
                checkinRate = new BigDecimal(checkinRate).setScale(2, RoundingMode.HALF_UP).doubleValue();
            }

            // 构建返回数据
            Map<String, Object> statistics = new HashMap<>();
            statistics.put("activityInfo", new ActivityDTO(activity));
            statistics.put("checkedIn", checkedInCount);
            statistics.put("notCheckedIn", notCheckedInCount);
            statistics.put("totalApproved", approvedCount);
            statistics.put("checkinRate", checkinRate);

            return Results.success()
                    .message("查询成功")
                    .data("statistics", statistics);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 获取单个活动的评分统计（用于ECharts柱状图或饼图）
     */
    @GetMapping("/{activityId}/score-statistics")
    public Results getScoreStatistics(@PathVariable Long activityId,
                                     @RequestParam("managerUserId") Long managerUserId) {
        try {
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 校验是否为该社团管理员
            ClubMember member = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, activity.getClubId())
                    .eq(ClubMember::getUserId, managerUserId)
                    .one();
            if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                return Results.fail().message("无权限查看该活动统计信息");
            }

            // 查询所有已通过审核且有评分的报名记录
            List<ActivityRegistration> scoredRegistrations = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "已通过")
                    .isNotNull(ActivityRegistration::getScore)
                    .list();

            // 按分数段统计：0.5-1.0, 1.5-2.0, 2.5-3.0, 3.5-4.0, 4.5-5.0
            long score05_10 = 0;
            long score15_20 = 0;
            long score25_30 = 0;
            long score35_40 = 0;
            long score45_50 = 0;

            BigDecimal totalScore = BigDecimal.ZERO;
            int scoredCount = scoredRegistrations.size();

            for (ActivityRegistration reg : scoredRegistrations) {
                BigDecimal score = reg.getScore();
                if (score != null) {
                    totalScore = totalScore.add(score);
                    double scoreValue = score.doubleValue();
                    if (scoreValue >= 0.5 && scoreValue <= 1.0) {
                        score05_10++;
                    } else if (scoreValue >= 1.5 && scoreValue <= 2.0) {
                        score15_20++;
                    } else if (scoreValue >= 2.5 && scoreValue <= 3.0) {
                        score25_30++;
                    } else if (scoreValue >= 3.5 && scoreValue <= 4.0) {
                        score35_40++;
                    } else if (scoreValue >= 4.5 && scoreValue <= 5.0) {
                        score45_50++;
                    }
                }
            }

            // 计算平均分
            BigDecimal averageScore = BigDecimal.ZERO;
            if (scoredCount > 0) {
                averageScore = totalScore.divide(BigDecimal.valueOf(scoredCount), 2, RoundingMode.HALF_UP);
            }

            // 统计已通过审核的总人数
            long totalApproved = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getStatus, "已通过")
                    .count();

            // 未评分人数
            long notScoredCount = totalApproved - scoredCount;

            // 评分率
            double scoreRate = 0.0;
            if (totalApproved > 0) {
                scoreRate = (double) scoredCount / totalApproved * 100;
                scoreRate = new BigDecimal(scoreRate).setScale(2, RoundingMode.HALF_UP).doubleValue();
            }

            // 构建分数段统计数据
            Map<String, Object> scoreDistribution = new HashMap<>();
            scoreDistribution.put("0.5-1.0", score05_10);
            scoreDistribution.put("1.5-2.0", score15_20);
            scoreDistribution.put("2.5-3.0", score25_30);
            scoreDistribution.put("3.5-4.0", score35_40);
            scoreDistribution.put("4.5-5.0", score45_50);

            // 构建返回数据
            Map<String, Object> statistics = new HashMap<>();
            statistics.put("activityInfo", new ActivityDTO(activity));
            statistics.put("scoreDistribution", scoreDistribution);
            statistics.put("averageScore", averageScore);
            statistics.put("scoredCount", scoredCount);
            statistics.put("notScoredCount", notScoredCount);
            statistics.put("totalApproved", totalApproved);
            statistics.put("scoreRate", scoreRate);

            return Results.success()
                    .message("查询成功")
                    .data("statistics", statistics);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 根据用户ID获取用户参与或管理的社团活动
     * 返回两部分：
     * 1. 用户参与的活动（通过 activity_registration 表查询）
     * 2. 用户管理的活动（用户是社团管理员，查询这些社团发布的活动）
     * 
     * @param userId 用户ID
     * @param type 查询类型：participated（只返回参与的活动）、managed（只返回管理的活动）、all或不传（返回两种活动）
     */
    @GetMapping("/user/{userId}")
    public Results getUserActivities(@PathVariable Long userId,
                                    @RequestParam(value = "type", required = false, defaultValue = "all") String type,
                                    @RequestParam(value = "keyword", required = false) String keyword) {
        try {
            if (userId == null) {
                return Results.fail().message("用户ID不能为空");
            }

            // 规范化type参数
            if (type == null || type.trim().isEmpty()) {
                type = "all";
            }
            type = type.toLowerCase().trim();

            // 验证type参数
            if (!"participated".equals(type) && !"managed".equals(type) && !"all".equals(type)) {
                return Results.fail().message("type参数值无效，只能是：participated、managed 或 all");
            }

            List<ActivityDTO> participatedDTOs = new ArrayList<>();
            List<ActivityDTO> managedDTOs = new ArrayList<>();

            // 如果需要查询参与的活动（type为"participated"或"all"）
            if ("participated".equals(type) || "all".equals(type)) {
                // 查询用户参与的活动（通过报名记录）
                List<ActivityRegistration> registrations = activityRegistrationService.lambdaQuery()
                        .eq(ActivityRegistration::getUserId, userId)
                        .list();

                List<Long> participatedActivityIds = registrations.stream()
                        .map(ActivityRegistration::getActivityId)
                        .distinct()
                        .collect(Collectors.toList());

                List<Activity> participatedActivities = new ArrayList<>();
                if (!participatedActivityIds.isEmpty()) {
                    // 构建查询条件，支持模糊搜索
                    LambdaQueryWrapper<Activity> participatedWrapper = new LambdaQueryWrapper<>();
                    participatedWrapper.in(Activity::getId, participatedActivityIds);
                    
                    // 应用 keyword 过滤
                    if (StringUtils.hasText(keyword)) {
                        participatedWrapper.and(wrapper -> wrapper
                            .like(Activity::getName, keyword)
                            .or()
                            .like(Activity::getDescription, keyword));
                    }
                    
                    participatedActivities = activityService.list(participatedWrapper);
                    // 刷新活动状态并统计报名人数
                    for (Activity activity : participatedActivities) {
                        refreshActivityStatusByTime(activity);
                        long participantCount = activityRegistrationService.lambdaQuery()
                                .eq(ActivityRegistration::getActivityId, activity.getId())
                                .eq(ActivityRegistration::getStatus, "已通过")
                                .count();
                        activity.setCurrentParticipants((int) participantCount);
                    }
                    
                    // 按活动状态排序，优先显示进行中的活动
                    participatedActivities.sort((a1, a2) -> {
                        // 先比较状态
                        if ("进行中".equals(a1.getStatus()) && !"进行中".equals(a2.getStatus())) {
                            return -1; // a1 排在前面
                        }
                        if (!"进行中".equals(a1.getStatus()) && "进行中".equals(a2.getStatus())) {
                            return 1; // a2 排在前面
                        }
                        // 状态相同按创建时间倒序
                        return a2.getCreateTime().compareTo(a1.getCreateTime());
                    });
                }

                // 转换为 DTO
                participatedDTOs = participatedActivities.stream()
                        .map(activity -> {
                            ActivityDTO dto = new ActivityDTO(activity);
                            // 将 imageUrls 字符串转换为数组
                            if (StringUtils.hasText(activity.getImageUrls())) {
                                List<String> urls = Arrays.stream(activity.getImageUrls().split(","))
                                        .map(String::trim)
                                        .filter(StringUtils::hasText)
                                        .collect(Collectors.toList());
                                dto.setImageUrls(urls);
                            } else {
                                dto.setImageUrls(new ArrayList<>());
                            }
                            return dto;
                        })
                        .collect(Collectors.toList());
            }

            // 如果需要查询管理的活动（type为"managed"或"all"）
            if ("managed".equals(type) || "all".equals(type)) {
                // 查询用户管理的社团（用户是管理员）
                List<ClubMember> managerRecords = clubMemberService.lambdaQuery()
                        .eq(ClubMember::getUserId, userId)
                        .eq(ClubMember::getIsManager, true)
                        .list();

                List<Activity> managedActivities = new ArrayList<>();
                if (!managerRecords.isEmpty()) {
                    List<Long> managedClubIds = managerRecords.stream()
                            .map(ClubMember::getClubId)
                            .distinct()
                            .collect(Collectors.toList());

                    // 查询这些社团发布的所有活动
                    LambdaQueryWrapper<Activity> wrapper = new LambdaQueryWrapper<>();
                    wrapper.in(Activity::getClubId, managedClubIds);
                    
                    // 应用 keyword 过滤
                    if (StringUtils.hasText(keyword)) {
                        wrapper.and(q -> q
                            .like(Activity::getName, keyword)
                            .or()
                            .like(Activity::getDescription, keyword));
                    }
                    
                    // 先按创建时间倒序查询，后续会重新排序
                    wrapper.orderByDesc(Activity::getCreateTime);
                    managedActivities = activityService.list(wrapper);
                    
                    // 按活动状态排序，优先显示进行中的活动
                    managedActivities.sort((a1, a2) -> {
                        // 先比较状态
                        if ("进行中".equals(a1.getStatus()) && !"进行中".equals(a2.getStatus())) {
                            return -1; // a1 排在前面
                        }
                        if (!"进行中".equals(a1.getStatus()) && "进行中".equals(a2.getStatus())) {
                            return 1; // a2 排在前面
                        }
                        // 状态相同按创建时间倒序
                        return a2.getCreateTime().compareTo(a1.getCreateTime());
                    });

                    // 刷新活动状态并统计报名人数
                    for (Activity activity : managedActivities) {
                        refreshActivityStatusByTime(activity);
                        long participantCount = activityRegistrationService.lambdaQuery()
                                .eq(ActivityRegistration::getActivityId, activity.getId())
                                .eq(ActivityRegistration::getStatus, "已通过")
                                .count();
                        activity.setCurrentParticipants((int) participantCount);
                    }
                }

                // 转换为 DTO
                managedDTOs = managedActivities.stream()
                        .map(activity -> {
                            ActivityDTO dto = new ActivityDTO(activity);
                            // 将 imageUrls 字符串转换为数组
                            if (StringUtils.hasText(activity.getImageUrls())) {
                                List<String> urls = Arrays.stream(activity.getImageUrls().split(","))
                                        .map(String::trim)
                                        .filter(StringUtils::hasText)
                                        .collect(Collectors.toList());
                                dto.setImageUrls(urls);
                            } else {
                                dto.setImageUrls(new ArrayList<>());
                            }
                            return dto;
                        })
                        .collect(Collectors.toList());
            }

            // 根据type参数决定返回的数据结构
            Results result = Results.success().message("查询成功");
            if ("participated".equals(type)) {
                // 只返回参与的活动
                result.data("activities", participatedDTOs);
            } else if ("managed".equals(type)) {
                // 只返回管理的活动
                result.data("activities", managedDTOs);
            } else {
                // 返回两种活动
                result.data("participated", participatedDTOs)
                       .data("managed", managedDTOs);
            }

            return result;
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 生成活动签到二维码
     * 二维码内容为JSON格式：{"activityId": 活动ID}
     */
    @GetMapping("/{activityId}/qrcode")
    public Results generateQrCode(@PathVariable Long activityId) {
        try {
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 构建二维码内容（JSON格式）
            Map<String, Object> qrContent = new HashMap<>();
            qrContent.put("activityId", activityId);
            String qrContentJson = objectMapper.writeValueAsString(qrContent);

            // 生成二维码Base64图片（300x300像素）
            String qrCodeBase64 = QrCodeUtil.generateQrCodeBase64(qrContentJson, 300, 300);

            Map<String, Object> result = new HashMap<>();
            result.put("qrCode", qrCodeBase64);
            result.put("activityId", activityId);
            result.put("activityName", activity.getName());

            return Results.success()
                    .message("生成二维码成功")
                    .data("qrcode", result);
        } catch (Exception e) {
            return Results.fail().message("生成二维码失败: " + e.getMessage());
        }
    }

    /**
     * 扫码签到
     * 只有报名活动且审核通过的人员才能扫描签到
     * 只能在活动开始时间至活动结束时间之间签到
     */
    @PostMapping("/checkin")
    public Results checkin(@RequestBody Map<String, Object> request) {
        try {
            Long activityId = null;
            Long userId = null;
            String qrContent = null;

            // 支持两种方式：直接传activityId和userId，或者传二维码内容
            if (request.containsKey("activityId") && request.containsKey("userId")) {
                activityId = Long.valueOf(request.get("activityId").toString());
                userId = Long.valueOf(request.get("userId").toString());
            } else if (request.containsKey("qrContent") && request.containsKey("userId")) {
                qrContent = request.get("qrContent").toString();
                userId = Long.valueOf(request.get("userId").toString());
                // 解析二维码内容
                Map<String, Object> qrData = objectMapper.readValue(qrContent, new TypeReference<Map<String, Object>>() {});
                activityId = Long.valueOf(qrData.get("activityId").toString());
            } else {
                return Results.fail().message("参数不完整，需要提供activityId和userId，或者qrContent和userId");
            }

            if (activityId == null || userId == null) {
                return Results.fail().message("活动ID和用户ID不能为空");
            }

            // 验证活动是否存在
            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 验证活动是否已通过审核
            if (activity.getAuditStatus() == null || activity.getAuditStatus() != 1) {
                return Results.fail().message("活动尚未通过审核，无法签到");
            }
            // 验证活动是否已上架
            if (!Boolean.TRUE.equals(activity.getIsPublished())) {
                return Results.fail().message("活动已下架，无法签到");
            }

            // 验证用户是否报名且审核通过
            ActivityRegistration registration = activityRegistrationService.lambdaQuery()
                    .eq(ActivityRegistration::getActivityId, activityId)
                    .eq(ActivityRegistration::getUserId, userId)
                    .one();

            if (registration == null) {
                return Results.fail().message("您未报名该活动，无法签到");
            }

            if (!"已通过".equals(registration.getStatus())) {
                return Results.fail().message("您的报名尚未通过审核，无法签到");
            }

            // 验证时间：只能在活动开始时间至活动结束时间之间签到
            LocalDateTime now = LocalDateTime.now();
            if (activity.getStartTime() == null || activity.getEndTime() == null) {
                return Results.fail().message("活动时间未配置，无法签到");
            }

            if (now.isBefore(activity.getStartTime())) {
                return Results.fail().message("活动尚未开始，无法签到");
            }

            if (now.isAfter(activity.getEndTime())) {
                return Results.fail().message("活动已结束，无法签到");
            }

            // 检查是否已经签到过
            ActivityCheckin existingCheckin = activityCheckinService.lambdaQuery()
                    .eq(ActivityCheckin::getActivityId, activityId)
                    .eq(ActivityCheckin::getUserId, userId)
                    .one();

            if (existingCheckin != null) {
                return Results.fail().message("您已经签到过了");
            }

            // 记录签到
            ActivityCheckin checkin = new ActivityCheckin();
            checkin.setActivityId(activityId);
            checkin.setUserId(userId);
            checkin.setCheckinTime(now);
            activityCheckinService.save(checkin);

            Map<String, Object> result = new HashMap<>();
            result.put("checkinId", checkin.getId());
            result.put("checkinTime", checkin.getCheckinTime().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli());
            result.put("activityName", activity.getName());

            return Results.success()
                    .message("签到成功")
                    .data("checkin", result);
        } catch (Exception e) {
            return Results.fail().message("签到失败: " + e.getMessage());
        }
    }

    /**
     * 根据当前时间刷新活动状态：
     * - 报名中：当前时间在报名开始和报名结束之间
     * - 等待中：报名结束后且当前时间在活动开始之前，或者当前时间在报名开始之前
     * - 进行中：当前时间在活动开始和活动结束之间
     * - 已结束：当前时间晚于活动结束
     *
     * 仅在活动已通过审核（auditStatus = 1）时生效。
     */
    private void refreshActivityStatusByTime(Activity activity) {
        if (activity == null) {
            return;
        }
        if (activity.getAuditStatus() == null || activity.getAuditStatus() != 1) {
            return;
        }

        LocalDateTime now = LocalDateTime.now();
        LocalDateTime regStart = activity.getRegistrationStartTime();
        LocalDateTime regEnd = activity.getRegistrationEndTime();
        LocalDateTime start = activity.getStartTime();
        LocalDateTime end = activity.getEndTime();

        // 关键时间未配置时，不强制调整状态
        if (regStart == null || regEnd == null || start == null || end == null) {
            activityService.updateById(activity);
            return;
        }

        String newStatus;
        if (now.isAfter(regStart) && now.isBefore(regEnd)) {
            newStatus = "报名中";
        } else if ((now.isAfter(regEnd) && now.isBefore(start)) || now.isBefore(regStart)) {
            newStatus = "等待中";
        } else if (now.isAfter(start) && now.isBefore(end)) {
            newStatus = "进行中";
        } else if (now.isAfter(end)) {
            newStatus = "已结束";
        } else {
            // 其他边界情况，保持原状态
            newStatus = activity.getStatus();
        }

        if (newStatus != null && !newStatus.equals(activity.getStatus())) {
            activity.setStatus(newStatus);
            activityService.updateById(activity);
        } else {
            // 即便状态未变化，也保证其他字段更新（例如审核时间等）
            activityService.updateById(activity);
        }
    }

    /**
     * 获取活动状态的优先级（用于排序）
     * 报名中(1) > 进行中(2) > 已结束(3)
     */
    private int getStatusPriority(String status) {
        if ("报名中".equals(status)) {
            return 1;
        } else if ("进行中".equals(status)) {
            return 2;
        } else if ("已结束".equals(status)) {
            return 3;
        }
        return 4; // 其他状态排在最后
    }

    /**
     * 上架/下架活动
     * 只有社团管理员或超级管理员可以操作
     * 
     * @param activityId 活动ID
     * @param request 请求参数，包含 managerUserId 和 isPublished
     */
    @PutMapping("/{activityId}/publish-status")
    public Results updatePublishStatus(@PathVariable Long activityId,
                                      @RequestBody Map<String, Object> request) {
        try {
            if (activityId == null) {
                return Results.fail().message("活动ID不能为空");
            }
            
            Long managerUserId = null;
            Boolean isPublished = null;
            
            if (request.containsKey("managerUserId")) {
                managerUserId = Long.valueOf(request.get("managerUserId").toString());
            }
            if (request.containsKey("isPublished")) {
                isPublished = Boolean.valueOf(request.get("isPublished").toString());
            }
            
            if (managerUserId == null || isPublished == null) {
                return Results.fail().message("参数不完整，需要提供 managerUserId 和 isPublished");
            }

            Activity activity = activityService.getById(activityId);
            if (activity == null) {
                return Results.fail().message("活动不存在");
            }

            // 验证权限：超级管理员或该社团管理员
            User user = userService.getById(managerUserId);
            boolean isBoss = user != null && Boolean.TRUE.equals(user.getIsBoss());
            
            if (!isBoss) {
                // 如果不是超级管理员，验证是否为该社团管理员
                ClubMember member = clubMemberService.lambdaQuery()
                        .eq(ClubMember::getClubId, activity.getClubId())
                        .eq(ClubMember::getUserId, managerUserId)
                        .one();
                if (member == null || member.getIsManager() == null || !member.getIsManager()) {
                    return Results.fail().message("无权限操作该活动");
                }
            }

            // 只有审核通过的活动才能上架
            if (Boolean.TRUE.equals(isPublished)) {
                if (activity.getAuditStatus() == null || activity.getAuditStatus() != 1) {
                    return Results.fail().message("活动尚未通过审核，无法上架");
                }
            }

            activity.setIsPublished(isPublished);
            activityService.updateById(activity);

            String message = Boolean.TRUE.equals(isPublished) ? "活动上架成功" : "活动下架成功";
            return Results.success()
                    .message(message)
                    .data("activity", activity);
        } catch (Exception e) {
            return Results.fail().message("操作失败: " + e.getMessage());
        }
    }
}


