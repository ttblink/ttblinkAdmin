# -*- coding: utf-8 -*-

from pydantic import BaseModel, ConfigDict, Field
from fastapi import Query
import datetime
from app.core.validator import DateTimeStr
from app.core.base_schema import BaseSchema, UserBySchema

class SwitchInfoCreateSchema(BaseModel):
    """
    交换机数据新增模型
    """
    ip: str = Field(default=..., description='IP')
    name: str = Field(default=..., description='名称')
    brand: str = Field(default=..., description='品牌')
    model: str = Field(default=..., description='型号')
    manageWay: str = Field(default=..., description='管理方式')
    username: str = Field(default=..., description='用户名')
    password: str = Field(default=..., description='密码')
    enablePassword: str = Field(default=..., description='enable密码')
    serviceType: str = Field(default=..., description='服务类型')
    location: str = Field(default=..., description='安装位置')
    status: str = Field(default="0", description='是否启用(0:启用 1:禁用)')
    description: str | None = Field(default=None, max_length=255, description='备注/描述')


class SwitchInfoUpdateSchema(SwitchInfoCreateSchema):
    """
    交换机数据更新模型
    """
    ...


class SwitchInfoOutSchema(SwitchInfoCreateSchema, BaseSchema, UserBySchema):
    """
    交换机数据响应模型
    """
    model_config = ConfigDict(from_attributes=True)


class SwitchInfoQueryParam:
    """交换机数据查询参数"""

    def __init__(
        self,
        name: str | None = Query(None, description="名称"),
        username: str | None = Query(None, description="用户名"),
        ip: str | None = Query(None, description="IP"),
        brand: str | None = Query(None, description="品牌"),
        model: str | None = Query(None, description="型号"),
        manageWay: str | None = Query(None, description="管理方式"),
        password: str | None = Query(None, description="密码"),
        enablePassword: str | None = Query(None, description="enable密码"),
        serviceType: str | None = Query(None, description="服务类型"),
        location: str | None = Query(None, description="安装位置"),
        status: str | None = Query(None, description="是否启用(0:启用 1:禁用)"),
        created_id: int | None = Query(None, description="创建人ID"),
        updated_id: int | None = Query(None, description="更新人ID"),
        created_time: list[DateTimeStr] | None = Query(None, description="创建时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
        updated_time: list[DateTimeStr] | None = Query(None, description="更新时间范围", examples=["2025-01-01 00:00:00", "2025-12-31 23:59:59"]),
    ) -> None:
        # 精确查询字段
        self.ip = ip
        # 模糊查询字段
        self.name = ("like", name)
        # 精确查询字段
        self.brand = brand
        # 精确查询字段
        self.model = model
        # 精确查询字段
        self.manageWay = manageWay
        # 模糊查询字段
        self.username = ("like", username)
        # 精确查询字段
        self.password = password
        # 精确查询字段
        self.enablePassword = enablePassword
        # 精确查询字段
        self.serviceType = serviceType
        # 精确查询字段
        self.location = location
        # 精确查询字段
        self.status = status
        # 精确查询字段
        self.created_id = created_id
        # 精确查询字段
        self.updated_id = updated_id
        # 时间范围查询
        if created_time and len(created_time) == 2:
            self.created_time = ("between", (created_time[0], created_time[1]))
        if updated_time and len(updated_time) == 2:
            self.updated_time = ("between", (updated_time[0], updated_time[1]))
