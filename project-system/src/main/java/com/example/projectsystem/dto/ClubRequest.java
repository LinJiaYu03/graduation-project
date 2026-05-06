package com.example.projectsystem.dto;

public class ClubRequest {
    private String iconUrl;
    private String name;
    private String tags;
    private String description;
    /**
     * 社团类型，对应表字段 level_tag
     */
    private String levelTag;
    /**
     * 创建者用户ID
     */
    private Long userId;

    public String getIconUrl() {
        return iconUrl;
    }

    public void setIconUrl(String iconUrl) {
        this.iconUrl = iconUrl;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getLevelTag() {
        return levelTag;
    }

    public void setLevelTag(String levelTag) {
        this.levelTag = levelTag;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }
}

