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

from .service import SwitchBackupService
from .schema import SwitchBackupCreateSchema, SwitchBackupUpdateSchema, SwitchBackupQueryParam

SwitchBackupRouter = APIRouter(prefix='/switch_backup', tags=["交换机备份管理模块"]) 

@SwitchBackupRouter.get("/detail/{id}", summary="获取交换机备份管理详情", description="获取交换机备份管理详情")
async def get_switch_backup_detail_controller(
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:query"]))
) -> JSONResponse:
    """获取交换机备份管理详情接口"""
    result_dict = await SwitchBackupService.detail_switch_backup_service(auth=auth, id=id)
    log.info(f"获取交换机备份管理详情成功 {id}")
    return SuccessResponse(data=result_dict, msg="获取交换机备份管理详情成功")

@SwitchBackupRouter.get("/list", summary="查询交换机备份管理列表", description="查询交换机备份管理列表")
async def get_switch_backup_list_controller(
    page: PaginationQueryParam = Depends(),
    search: SwitchBackupQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:query"]))
) -> JSONResponse:
    """查询交换机备份管理列表接口（数据库分页）"""
    result_dict = await SwitchBackupService.page_switch_backup_service(
        auth=auth,
        page_no=page.page_no if page.page_no is not None else 1,
        page_size=page.page_size if page.page_size is not None else 10,
        search=search,
        order_by=page.order_by
    )
    log.info("查询交换机备份管理列表成功")
    return SuccessResponse(data=result_dict, msg="查询交换机备份管理列表成功")

@SwitchBackupRouter.post("/create", summary="创建交换机备份管理", description="创建交换机备份管理")
async def create_switch_backup_controller(
    data: SwitchBackupCreateSchema,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:create"]))
) -> JSONResponse:
    """创建交换机备份管理接口"""
    result_dict = await SwitchBackupService.create_switch_backup_service(auth=auth, data=data)
    log.info("创建交换机备份管理成功")
    return SuccessResponse(data=result_dict, msg="创建交换机备份管理成功")

@SwitchBackupRouter.put("/update/{id}", summary="修改交换机备份管理", description="修改交换机备份管理")
async def update_switch_backup_controller(
    data: SwitchBackupUpdateSchema,
    id: int = Path(..., description="ID"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:update"]))
) -> JSONResponse:
    """修改交换机备份管理接口"""
    result_dict = await SwitchBackupService.update_switch_backup_service(auth=auth, id=id, data=data)
    log.info("修改交换机备份管理成功")
    return SuccessResponse(data=result_dict, msg="修改交换机备份管理成功")

@SwitchBackupRouter.delete("/delete", summary="删除交换机备份管理", description="删除交换机备份管理")
async def delete_switch_backup_controller(
    ids: list[int] = Body(..., description="ID列表"),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:delete"]))
) -> JSONResponse:
    """删除交换机备份管理接口"""
    await SwitchBackupService.delete_switch_backup_service(auth=auth, ids=ids)
    log.info(f"删除交换机备份管理成功: {ids}")
    return SuccessResponse(msg="删除交换机备份管理成功")

@SwitchBackupRouter.patch("/available/setting", summary="批量修改交换机备份管理状态", description="批量修改交换机备份管理状态")
async def batch_set_available_switch_backup_controller(
    data: BatchSetAvailable,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:patch"]))
) -> JSONResponse:
    """批量修改交换机备份管理状态接口"""
    await SwitchBackupService.set_available_switch_backup_service(auth=auth, data=data)
    log.info(f"批量修改交换机备份管理状态成功: {data.ids}")
    return SuccessResponse(msg="批量修改交换机备份管理状态成功")

@SwitchBackupRouter.post('/export', summary="导出交换机备份管理", description="导出交换机备份管理")
async def export_switch_backup_list_controller(
    search: SwitchBackupQueryParam = Depends(),
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:export"]))
) -> StreamingResponse:
    """导出交换机备份管理接口"""
    result_dict_list = await SwitchBackupService.list_switch_backup_service(search=search, auth=auth)
    export_result = await SwitchBackupService.batch_export_switch_backup_service(obj_list=result_dict_list)
    log.info('导出交换机备份管理成功')
    return StreamResponse(
        data=bytes2file_response(export_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={
            'Content-Disposition': 'attachment; filename=switch_backup.xlsx'
        }
    )

@SwitchBackupRouter.post('/import', summary="导入交换机备份管理", description="导入交换机备份管理")
async def import_switch_backup_list_controller(
    file: UploadFile,
    auth: AuthSchema = Depends(AuthPermission(["module_gencode:switch_backup:import"]))
) -> JSONResponse:
    """导入交换机备份管理接口"""
    batch_import_result = await SwitchBackupService.batch_import_switch_backup_service(file=file, auth=auth, update_support=True)
    log.info("导入交换机备份管理成功")
    return SuccessResponse(data=batch_import_result, msg="导入交换机备份管理成功")

@SwitchBackupRouter.post('/download/template', summary="获取交换机备份管理导入模板", description="获取交换机备份管理导入模板", dependencies=[Depends(AuthPermission(["module_gencode:switch_backup:download"]))])
async def export_switch_backup_template_controller() -> StreamingResponse:
    """获取交换机备份管理导入模板接口"""
    import_template_result = await SwitchBackupService.import_template_download_switch_backup_service()
    log.info('获取交换机备份管理导入模板成功')
    return StreamResponse(
        data=bytes2file_response(import_template_result),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename=switch_backup_template.xlsx'}
    )