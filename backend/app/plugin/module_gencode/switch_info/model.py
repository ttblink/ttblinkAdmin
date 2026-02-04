# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import , DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SwitchInfoModel(ModelMixin, UserMixin):
    """
    交换机信息表
    """
    __tablename__: str = 'switch_info'
    __table_args__: dict[str, str] = {'comment': '交换机信息'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='名称')
    ip: Mapped[str | None] = mapped_column(String(20), nullable=True, comment='IP')
    brand: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='品牌')
    model: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='型号')
    manageWay: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='管理方式')
    username: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='用户名')
    password: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='密码')
    enablePassword: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='enable密码')
    serviceType: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='服务类型')
    location: Mapped[str | None] = mapped_column(String(100), nullable=True, comment='安装位置')

