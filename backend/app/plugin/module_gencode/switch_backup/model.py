# -*- coding: utf-8 -*-

import datetime
from sqlalchemy import DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.base_model import ModelMixin, UserMixin


class SwitchBackupModel(ModelMixin, UserMixin):
    """
    交换机备份管理表
    """
    __tablename__: str = 'switch_backup'
    __table_args__: dict[str, str] = {'comment': '交换机备份管理'}
    __loader_options__: list[str] = ["created_by", "updated_by"]

    ip: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='交换机IP')
    name: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='交换机名称')
    backupType: Mapped[str | None] = mapped_column(String(64), nullable=True, comment='备份方式')

