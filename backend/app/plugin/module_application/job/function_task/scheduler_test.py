# -*- coding: utf-8 -*-

import time
from datetime import datetime

from app.core.logger import log

def job(*args, **kwargs) -> None:
    """
    定时任务执行同步函数示例

    参数:
    - args: 位置参数。
    - kwargs: 关键字参数。
    """
    try:
        print(f"开始执行任务: {args}-{kwargs}")
        time.sleep(3)
        print(f'{datetime.now()}同步函数执行完成')
    except Exception as e:
        log.error(f"同步任务执行失败: {e}")
        raise

async def async_job(*args, **kwargs) -> None:
    """
    定时任务执行异步函数示例

    参数:
    - args: 位置参数。
    - kwargs: 关键字参数。
    """
    try:
        print(f"开始执行任务: {args}-{kwargs}")
        time.sleep(3)
        print(f'{datetime.now()}异步函数执行完成')
    except Exception as e:
        log.error(f"异步任务执行失败: {e}")
        raise

async def switch_config_backup_every_five_seconds(*args, **kwargs) -> None:
    """
    定时任务执行异步函数示例,每5秒备份一次交换机配置文件

    参数:
    - args: 位置参数。
    - kwargs: 关键字参数。
    """
    try:
        print(f"开始执行任务: {args}-{kwargs}")
        time.sleep(5)
        print(f'{datetime.now()}备份交换机配置文件')
    except Exception as e:
        log.error(f"备份配置文件失败: {e}")