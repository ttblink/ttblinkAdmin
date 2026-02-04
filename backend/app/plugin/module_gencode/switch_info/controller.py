# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, UploadFile, Body, Path, Query
from fastapi.responses import StreamingResponse, JSONResponse

from app.common.response import SuccessResponse, StreamResponse
from app.core.dependencies import AuthPermission
from app.api.v1.module_system.auth.schema import AuthSchema
from app.core.base_params import PaginationQueryParam
from app.utils.common_util import bytes2file_response
from app.core.logger import log
from app.core.base_schema import BatchSetAvailable

from .service import SwitchInfoService
from .schema import SwitchInfoCreateSchema, SwitchInfoUpdateSchema, SwitchInfoQueryParam

SwitchInfoRouter = APIRouter(prefix='/switch_info', tags=["交换机数据模块"]) 

@SwitchInfoRouter.get("/detail/{id}", summary="获取交换机数据详情", description="获取交换机数据详情")
async def get_switch_info_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:query"]))
) -> JSONResponse:
    """获取交换机数据详情接口"""
    result_dict = await SwitchInfoService.detail_switch_info_service(auth=auth, id=id)
    log.info(f"获取交换机数据详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取交换机数据详情成功")

@SwitchInfoRouter.get("/list", summary="查询交换机数据列表", description="查询交换机数据列表")
async def get_switch_info_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SwitchInfoQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:query"]))
) -> JSONResponse:
    """查询交换机数据列表接口（数据库分页）"""
    result_dict = await SwitchInfoService.page_switch_info_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询交换机数据列表成功")
    return SuccessResponse(data=result_dict, msg="查询交换机数据列表成功")

@SwitchInfoRouter.post("/create", summary="创建交换机数据", description="创建交换机数据")
async def create_switch_info_controller(
    data: SwitchInfoCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:create"]))
) -> JSONResponse:
    """创建交换机数据接口"""
    result_dict = await SwitchInfoService.create_switch_info_service(auth=auth, data=data)
    log.info("创建交换机数据成功")
    return SuccessResponse(data=result_dict, msg="创建交换机数据成功")

@SwitchInfoRouter.put("/update/{id}", summary="修改交换机数据", description="修改交换机数据")
async def update_switch_info_controller(
    data: SwitchInfoUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:update"]))
) -> JSONResponse:
    """修改交换机数据接口"""
    result_dict = await SwitchInfoService.update_switch_info_service(auth=auth, id=id, data=data)
    log.info("修改交换机数据成功")
    return SuccessResponse(data=result_dict, msg="修改交换机数据成功")

@SwitchInfoRouter.delete("/delete", summary="删除交换机数据", description="删除交换机数据")
async def delete_switch_info_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:delete"]))
) -> JSONResponse:
    """删除交换机数据接口"""
    await SwitchInfoService.delete_switch_info_service(auth=auth, ids=ids)
    log.info(f"删除交换机数据成功: {ids}")
    return SuccessResponse(msg="删除交换机数据成功")

@SwitchInfoRouter.patch("/available/setting", summary="批量修改交换机数据状态", description="批量修改交换机数据状态")
async def batch_set_available_switch_info_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:patch"]))
) -> JSONResponse:
    """批量修改交换机数据状态接口"""
    await SwitchInfoService.set_available_switch_info_service(auth=auth, data=data)
    log.info(f"批量修改交换机数据状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改交换机数据状态成功")

@SwitchInfoRouter.post('/export', summary="导出交换机数据", description="导出交换机数据")
async def export_switch_info_list_controller(
    search: SwitchInfoQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:export"]))
) -> StreamingResponse:
    """导出交换机数据接口"""
    result_dict_list = await SwitchInfoService.list_switch_info_service(search=search, auth=auth)
    export_result = await SwitchInfoService.batch_export_switch_info_service(obj_list=result_dict_list)
    log.info('导出交换机数据成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=switch_info.xlsx'
        }
    )

@SwitchInfoRouter.post('/import', summary="导入交换机数据", description="导入交换机数据")
async def import_switch_info_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:import"]))
) -> JSONResponse:
    """导入交换机数据接口"""
    batch_import_result = await SwitchInfoService.batch_import_switch_info_service(file=file, auth=auth, update_support=True)
    log.info("导入交换机数据成功")
    return SuccessResponse(data=batch_import_result, msg="导入交换机数据成功")

@SwitchInfoRouter.post('/download/template', summary="获取交换机数据导入模板", description="获取交换机数据导入模板", dependencies=[Depends(AuthPermission(["module_gencode:switch_info:download"]))])
async def export_switch_info_template_controller() -> StreamingResponse:
    """获取交换机数据导入模板接口"""
    import_template_result = await SwitchInfoService.import_template_download_switch_info_service()
    log.info('获取交换机数据导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=switch_info_template.xlsx'}
    )

@SwitchInfoRouter.post('/backup/config', summary="获取交换机配置备份文件", description="获取交换机配置备份文件")
async def backup_switch_config_controller(
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_info:backup"]))
    ,data: dict = Body(..., description="交换机配置备份文件获取参数")
) -> JSONResponse:
    """获取交换机配置备份文件接口"""
    result = await SwitchInfoService.get_switch_config_service(auth=auth, data=data)
    log.info("获取交换机配置备份文件成功")
    return SuccessResponse(data=result, msg="获取交换机配置备份文件成功")