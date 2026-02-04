from scrapli.driver.core import AsyncIOSXEDriver
from scrapli import AsyncScrapli
import io
from datetime import datetime
import os
from asyncping3 import ping,verbose_ping, errors
from app.core.exceptions import CustomException
from app.core.logger import log

class Switch:
    """交换机操作类"""

    @classmethod
    async def ping_switch(cls,ip:str)->bool:
        """ping交换机"""
        try:
            ping_result = await ping(ip)
            if isinstance(ping_result,float):
                return True
            else:
                return False
        except errors.PingError as e:
            log.error(f"ping交换机失败: {str(e)}")
            return False
        except Exception as e:
            log.error(f"ping交换机失败: {str(e)}")
    

    @classmethod
    async def get_switch_configuration_service(cls,data:dict)->str:
        """获取交换机配置文件内容"""
        ip=data.get("ip")
        brand=data.get("brand")
        manageWay=data.get("manageWay")
        username=data.get("username")
        password=data.get("password")
        enablePassword=data.get("enablePassword")
        # 连接交换机,获取日志
        try:
            log_reault=""
            if brand=="华三":
                log_reault=await cls.connect_switch_send_command_service(ip, manageWay, brand, username, password, enablePassword, "display current-configuration")
            elif brand=="华为":
                log_reault=await cls.connect_switch_send_command_service(ip, manageWay, brand, username, password, enablePassword, "display current-configuration")
            elif brand=="思科":
                log_reault=await cls.connect_switch_send_command_service(ip, manageWay, brand, username, password, enablePassword, "show running-config")
            elif brand=="其他":
                log_reault="暂不支持其他品牌交换机日志获取"
            return log_reault
        except Exception as e:
            raise CustomException(msg=f"获取交换机日志失败: {str(e)}")
        
    
    @classmethod
    async def connect_switch_send_command_service(cls, ip: str, manageWay: str, brand: str, username: str, password: str, enablePassword: str, command: str) -> str:
        """连接交换机并发送命令"""
        # 检测交换机是否可达
        try:
            ping_result = await ping(ip)
            if isinstance(ping_result,float):
                if manageWay=="telnet" and brand=="华三":
                    conn=None
                    try:
                        device={
                            "host":ip,
                            "auth_username":username,
                            "auth_password":password,
                            "auth_strict_key":False,
                            "transport":"asynctelnet",
                            "port":23,
                            "platform":"hp_comware"
                        }
                        conn=AsyncScrapli(**device)
                        await conn.open()
                        if not conn.isalive():
                            raise CustomException(msg=f"华三telnet连接失败")
                        result=await conn.send_command(command)
                        if not result.failed:
                            # 返回命令结果
                            return result.result
                        else:
                            raise CustomException(msg=f"华三telnet命令执行失败: {result.result}")
                    except Exception as e:
                        raise CustomException(msg=f"华三telnet连接失败: {str(e)}")
                    finally:
                        # 关闭连接
                        if conn and hasattr(conn, 'close'):
                            try:
                                if hasattr(conn, 'isalive') and conn.isalive():
                                    await conn.close()
                            except Exception as e:
                                log.warning(f"关闭华三telnet连接失败: {str(e)}")
                elif manageWay=="ssh" and brand=="华三":
                    conn=None
                    try:
                        device={
                            "host":ip,
                            "auth_username":username,
                            "auth_password":password,
                            "auth_strict_key":False,
                            "transport":"asyncssh",
                            "port":22,
                            "platform":"hp_comware",
                            # 添加ssh配置
                            "transport_options":{
                                "asyncssh": {
                                    "encryption_algs": ["aes128-cbc", "aes256-cbc", "3des-cbc"],
                                    "kex_algs": ["diffie-hellman-group1-sha1", "diffie-hellman-group14-sha1"],
                                    "server_host_key_algs": ["ssh-rsa"],  # 关键：允许ssh-rsa算法
                                }
                            }
                        }
                        conn=AsyncScrapli(**device)
                        await conn.open()
                        if not conn.isalive():
                            raise CustomException(msg=f"华三ssh连接失败")
                        result=await conn.send_command(command)
                        if not result.failed:
                            # 返回命令结果
                            return result.result
                        else:
                            raise CustomException(msg=f"华三ssh命令执行失败: {result.result}")
                    except Exception as e:
                        raise CustomException(msg=f"华三ssh连接失败: {str(e)}")
                    finally:
                        # 关闭连接
                        if conn and hasattr(conn, 'close'):
                            try:
                                if hasattr(conn, 'isalive') and conn.isalive():
                                    await conn.close()
                            except Exception as e:
                                log.error(f"关闭华三ssh连接失败: {str(e)}")
                elif manageWay=="ssh" and brand=="华为":
                    conn=None
                    try:
                        device={
                            "host":ip,
                            "auth_username":username,
                            "auth_password":password,
                            "auth_strict_key":False,
                            "transport":"asyncssh",
                            "port":22,
                            "platform":"huawei_vrp",
                            # 添加ssh配置
                            "transport_options":{
                                "asyncssh": {
                                    "encryption_algs": ["aes128-cbc", "aes256-cbc", "3des-cbc"],
                                    "kex_algs": ["diffie-hellman-group1-sha1", "diffie-hellman-group14-sha1"],
                                    "server_host_key_algs": ["ssh-rsa"],  # 关键：允许ssh-rsa算法
                                }
                            }
                        }
                        conn=AsyncScrapli(**device)
                        await conn.open()
                        if not conn.isalive():
                            raise CustomException(msg=f"华为ssh连接失败")
                        result=await conn.send_command(command)
                        if not result.failed:
                            # 返回命令结果
                            return result.result
                        else:
                            raise CustomException(msg=f"华为ssh命令执行失败: {result.result}")
                    except Exception as e:
                        raise CustomException(msg=f"华为ssh连接失败: {str(e)}")
                    finally:
                        # 关闭连接
                        if conn and hasattr(conn, 'close'):
                            try:
                                if hasattr(conn, 'isalive') and conn.isalive():
                                    await conn.close()
                            except Exception as e:
                                log.error(f"关闭华为ssh连接失败: {str(e)}")
                elif manageWay=="telnet" and brand=="华为":
                    conn=None
                    try:
                        device={
                            "host":ip,
                            "auth_username":username,
                            "auth_password":password,
                            "auth_strict_key":False,
                            "transport":"asynctelnet",
                            "port":23,
                            "platform":"huawei_vrp"
                        }
                        conn=AsyncScrapli(**device)
                        await conn.open()
                        if not conn.isalive():
                            raise CustomException(msg=f"华为telnet连接失败")
                        result=await conn.send_command(command)
                        if not result.failed:
                            # 返回命令结果
                            return result.result
                        else:
                            raise CustomException(msg=f"华为telnet命令执行失败: {result.result}")
                    except Exception as e:
                        raise CustomException(msg=f"华为telnet连接失败: {str(e)}")
                    finally:
                        # 关闭连接
                        if conn and hasattr(conn, 'close'):
                            try:
                                if hasattr(conn, 'isalive') and conn.isalive():
                                    await conn.close()
                            except Exception as e:
                                log.warning(f"关闭华为telnet连接失败: {str(e)}")
                elif manageWay=="ssh" and brand=="思科":
                    conn=None
                    try:
                        device={
                            "host":ip,
                            "auth_username":username,
                            "auth_password":password,
                            "auth_secondary":enablePassword,
                            "auth_strict_key":False,
                            "transport":"asyncssh",
                            "port":22,
                            # 添加ssh配置
                            "transport_options":{
                                "asyncssh": {
                                    "encryption_algs": ["aes128-cbc", "aes256-cbc", "3des-cbc"],
                                    "kex_algs": ["diffie-hellman-group1-sha1", "diffie-hellman-group14-sha1"],
                                    "server_host_key_algs": ["ssh-rsa"],  # 关键：允许ssh-rsa算法
                                }
                            }
                        }
                        conn=AsyncIOSXEDriver(**device)
                        await conn.open()
                        if not conn.isalive():
                            raise CustomException(msg=f"思科ssh连接失败")
                        result=await conn.send_command(command)
                        if not result.failed:
                            # 返回命令结果
                            return result.result
                        else:
                            raise CustomException(msg=f"思科ssh命令执行失败: {result.result}")
                    except Exception as e:
                        raise CustomException(msg=f"思科ssh连接失败: {str(e)}")
                    finally:
                        # 关闭连接
                        if conn and hasattr(conn, 'close'):
                            try:
                                if hasattr(conn, 'isalive') and conn.isalive():
                                    await conn.close()
                            except Exception as e:
                                log.error(f"关闭思科ssh连接失败: {str(e)}")
                elif manageWay=="telnet" and brand=="思科":
                    conn=None
                    try:
                        device={
                            "host":ip,
                            "auth_username":username,
                            "auth_password":password,
                            "auth_secondary":enablePassword,
                            "auth_strict_key":False,
                            "transport":"asynctelnet",
                            "port":23,
                        }
                        conn=AsyncIOSXEDriver(**device)
                        await conn.open()
                        if not conn.isalive():
                            raise CustomException(msg=f"思科telnet连接失败")
                        result=await conn.send_command(command)
                        if not result.failed:
                            # 返回命令结果
                            return result.result
                        else:
                            raise CustomException(msg=f"思科telnet命令执行失败: {result.result}")
                    except Exception as e:
                        raise CustomException(msg=f"思科telnet连接失败: {str(e)}")
                    finally:
                        # 关闭连接
                        if conn and hasattr(conn, 'close'):
                            try:
                                if hasattr(conn, 'isalive') and conn.isalive():
                                    await conn.close()
                            except Exception as e:
                                log.warning(f"关闭思科telnet连接失败: {str(e)}")
                else:
                    raise CustomException(msg=f"暂不支持{brand}的{manageWay}方式")
            else:
                raise CustomException(msg=f"交换机{ip}不可达，请检查网络连接")
        except errors.PingError as e:
            raise CustomException(msg=f"交换机{ip}不可达，请检查网络连接")
