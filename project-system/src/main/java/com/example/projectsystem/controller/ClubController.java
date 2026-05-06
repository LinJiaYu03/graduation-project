package com.example.projectsystem.controller;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.example.projectsystem.commons.PageResult;
import com.example.projectsystem.commons.Results;
import com.example.projectsystem.domain.Club;
import com.example.projectsystem.domain.ClubMember;
import com.example.projectsystem.domain.User;
import com.example.projectsystem.dto.ClubOptionDTO;
import com.example.projectsystem.dto.ClubMemberWithUserDTO;
import com.example.projectsystem.dto.ClubRequest;
import com.example.projectsystem.dto.ClubSearchRequest;
import com.example.projectsystem.dto.JoinClubRequest;
import com.example.projectsystem.dto.JoinedClubSearchRequest;
import com.example.projectsystem.service.ClubMemberService;
import com.example.projectsystem.service.ClubService;
import com.example.projectsystem.service.UserService;
import org.springframework.util.StringUtils;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/clubs")
public class ClubController {

    private final ClubService clubService;
    private final ClubMemberService clubMemberService;
    private final UserService userService;

    public ClubController(ClubService clubService, ClubMemberService clubMemberService, UserService userService) {
        this.clubService = clubService;
        this.clubMemberService = clubMemberService;
        this.userService = userService;
    }

    /**
     * 添加社团
     */
    @PostMapping
    public Results createClub(@RequestBody ClubRequest request) {
        try {
            if (!StringUtils.hasText(request.getName())) {
                return Results.fail().message("社团名称不能为空");
            }

            Club club = new Club();
            club.setIconUrl(request.getIconUrl());
            club.setName(request.getName());
            club.setTags(request.getTags());
            club.setDescription(request.getDescription());
            // 设置社团类型
            club.setLevelTag(request.getLevelTag());
            club.setStatus(1); // 默认启用

            Club createdClub = clubService.createClub(club);

            // 如果提供了创建者用户ID，则自动添加创建者为社团管理员
            if (request.getUserId() != null) {
                User creator = userService.getById(request.getUserId());
                if (creator != null) {
                    String userName = StringUtils.hasText(creator.getRealName()) ? creator.getRealName() : creator.getUsername();
                    ClubMember adminMember = new ClubMember();
                    adminMember.setClubId(createdClub.getId());
                    adminMember.setUserId(request.getUserId());
                    adminMember.setUserName(userName);
                    adminMember.setIsManager(true);
                    adminMember.setJoinTime(LocalDateTime.now());
                    clubMemberService.save(adminMember);
                }
            }

            return Results.success()
                    .message("创建社团成功")
                    .data("club", createdClub)
                    .data("clubId", createdClub.getId());
        } catch (Exception e) {
            return Results.fail().message("创建社团失败: " + e.getMessage());
        }
    }

    /**
     * 模糊查询社团列表
     */
    @PostMapping("/search")
    public Results searchClubs(@RequestBody ClubSearchRequest request) {
        Integer currentPage = request.getCurrentPage() != null && request.getCurrentPage() > 0
                ? request.getCurrentPage() : 1;
        Integer pageSize = request.getPageSize() != null && request.getPageSize() > 0
                ? request.getPageSize() : 10;

        Page<Club> page = new Page<>(currentPage, pageSize);
        LambdaQueryWrapper<Club> queryWrapper = new LambdaQueryWrapper<>();

        if (StringUtils.hasText(request.getKeyword())) {
            queryWrapper.and(wrapper -> wrapper
                    .like(Club::getName, request.getKeyword())
                    .or()
                    .like(Club::getTags, request.getKeyword())
                    .or()
                    .like(Club::getDescription, request.getKeyword())
            );
        }

        // 只查询启用的社团
        queryWrapper.eq(Club::getStatus, 1);
        queryWrapper.orderByDesc(Club::getCreateTime);

        IPage<Club> pageResult = clubService.page(page, queryWrapper);

        // 填充社团人数
        List<Club> clubs = pageResult.getRecords();
        for (Club club : clubs) {
            long count = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, club.getId())
                    .count();
            club.setMemberCount(count);
        }

        PageResult<Club> pageData = new PageResult<>(
                pageResult.getTotal(),
                (int) pageResult.getCurrent(),
                (int) pageResult.getSize(),
                pageResult.getRecords()
        );

        return Results.success()
                .message("查询成功")
                .data("page", pageData);
    }

    /**
     * 加入社团
     */
    @PostMapping("/join")
    public Results joinClub(@RequestBody JoinClubRequest request) {
        try {
            if (request.getClubId() == null) {
                return Results.fail().message("社团ID不能为空");
            }
            if (request.getUserId() == null) {
                return Results.fail().message("用户ID不能为空");
            }

            // 检查社团是否存在
            Club club = clubService.getById(request.getClubId());
            if (club == null) {
                return Results.fail().message("社团不存在");
            }
            if (club.getStatus() == null || club.getStatus() != 1) {
                return Results.fail().message("该社团已禁用");
            }

            ClubMember clubMember = clubMemberService.joinClub(request.getClubId(), request.getUserId());
            return Results.success()
                    .message("加入社团成功")
                    .data("clubMember", clubMember);
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        } catch (Exception e) {
            return Results.fail().message("加入社团失败: " + e.getMessage());
        }
    }

    /**
     * 模糊查询已加入的社团列表
     */
    @PostMapping("/joined")
    public Results getJoinedClubs(@RequestBody JoinedClubSearchRequest request) {
        try {
            if (request.getUserId() == null) {
                return Results.fail().message("用户ID不能为空");
            }

            Integer currentPage = request.getCurrentPage() != null && request.getCurrentPage() > 0
                    ? request.getCurrentPage() : 1;
            Integer pageSize = request.getPageSize() != null && request.getPageSize() > 0
                    ? request.getPageSize() : 10;

            // 先查询用户加入的社团成员记录
            LambdaQueryWrapper<ClubMember> memberWrapper = new LambdaQueryWrapper<>();
            memberWrapper.eq(ClubMember::getUserId, request.getUserId());

            // 根据 type 过滤：management 时只查管理员
            if ("management".equalsIgnoreCase(request.getType())) {
                memberWrapper.eq(ClubMember::getIsManager, true);
            }

            List<ClubMember> members = clubMemberService.list(memberWrapper);

            if (members.isEmpty()) {
                PageResult<Club> emptyPage = new PageResult<>(0L, currentPage, pageSize, List.of());
                return Results.success()
                        .message("查询成功")
                        .data("page", emptyPage);
            }

            // 获取所有加入的社团ID
            List<Long> clubIds = members.stream()
                    .map(ClubMember::getClubId)
                    .collect(Collectors.toList());

            // 查询社团信息
            Page<Club> page = new Page<>(currentPage, pageSize);
            LambdaQueryWrapper<Club> clubWrapper = new LambdaQueryWrapper<>();
            clubWrapper.in(Club::getId, clubIds);

            // 模糊查询条件
            if (StringUtils.hasText(request.getKeyword())) {
                clubWrapper.and(wrapper -> wrapper
                        .like(Club::getName, request.getKeyword())
                        .or()
                        .like(Club::getTags, request.getKeyword())
                        .or()
                        .like(Club::getDescription, request.getKeyword())
                );
            }

            clubWrapper.eq(Club::getStatus, 1);
            clubWrapper.orderByDesc(Club::getCreateTime);

            IPage<Club> pageResult = clubService.page(page, clubWrapper);

            // 填充社团人数
            List<Club> clubs = pageResult.getRecords();
            for (Club club : clubs) {
                long count = clubMemberService.lambdaQuery()
                        .eq(ClubMember::getClubId, club.getId())
                        .count();
                club.setMemberCount(count);
            }

            PageResult<Club> pageData = new PageResult<>(
                    pageResult.getTotal(),
                    (int) pageResult.getCurrent(),
                    (int) pageResult.getSize(),
                    pageResult.getRecords()
            );

            return Results.success()
                    .message("查询成功")
                    .data("page", pageData);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    } // 这里添加了缺失的右大括号

    /**
     * 获取当前用户管理的社团下拉列表
     */
    @GetMapping("/managed")
    public Results getManagedClubs(@RequestParam Long userId) {
        try {
            List<ClubOptionDTO> items = clubMemberService.getManagedClubOptionsByUserId(userId);
            return Results.success()
                    .message("查询成功")
                    .data("items", items);
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 获取加入该社团的人员列表
     */
    @GetMapping("/{clubId}/members")
    public Results getClubMembers(@PathVariable Long clubId) {
        // 查询该社团的成员列表（包含完整用户信息），管理员排在前面
        List<ClubMemberWithUserDTO> items = clubMemberService.getMembersWithUserByClubId(clubId);

        return Results.success()
                .message("查询成功")
                .data("items", items);
    }

    /**
     * 设置社团人员为管理员 / 取消管理员
     */
    @PostMapping("/{clubId}/members/{userId}/manager")
    public Results setClubMemberManager(@PathVariable Long clubId,
                                        @PathVariable Long userId,
                                        @RequestParam(defaultValue = "true") boolean isManager) {
        try {
            clubMemberService.setManager(clubId, userId, isManager);
            return Results.success()
                    .message(isManager ? "设置管理员成功" : "取消管理员成功");
        } catch (IllegalArgumentException e) {
            return Results.fail().message(e.getMessage());
        } catch (Exception e) {
            return Results.fail().message("操作失败: " + e.getMessage());
        }
    }

    /**
     * 根据社团ID获取社团信息
     */
    @GetMapping("/{id}")
    public Results getClubById(@PathVariable Long id) {
        try {
            Club club = clubService.getById(id);
            if (club == null) {
                return Results.fail().message("社团不存在");
            }

            // 填充社团人数
            long memberCount = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, id)
                    .count();
            club.setMemberCount(memberCount);

            return Results.success()
                    .message("查询成功")
                    .data("club", club);
        } catch (Exception e) {
            return Results.fail().message("查询失败: " + e.getMessage());
        }
    }

    /**
     * 获取最新的社团列表（默认前四个）
     */
    @GetMapping("/latest")
    public Results getLatestClubs(@RequestParam(value = "limit", defaultValue = "4") Integer limit) {
        if (limit == null || limit <= 0) {
            limit = 4;
        }

        List<Club> clubs = clubService.getLatestClubs(limit);

        // 填充社团人数
        for (Club club : clubs) {
            long count = clubMemberService.lambdaQuery()
                    .eq(ClubMember::getClubId, club.getId())
                    .count();
            club.setMemberCount(count);
        }

        return Results.success()
                .message("查询成功")
                .data("items", clubs);
    }
}