from pydantic import BaseModel


class UserRoleAssignRequest(BaseModel):
    roleCodes: list[str] = []


class RolePermissionUpdateRequest(BaseModel):
    permissionCodes: list[str] = []
