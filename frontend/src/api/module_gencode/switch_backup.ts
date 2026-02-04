import request from "@/utils/request";

const API_PATH = "/gencode/switch_backup";

const SwitchBackupAPI = {
  // 列表查询
  listSwitchBackup(query: SwitchBackupPageQuery) {
    return request<ApiResponse<PageResult<SwitchBackupTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSwitchBackup(id: number) {
    return request<ApiResponse<SwitchBackupTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSwitchBackup(body: SwitchBackupForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSwitchBackup(id: number, body: SwitchBackupForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSwitchBackup(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSwitchBackup(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSwitchBackup(query: SwitchBackupPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSwitchBackup() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSwitchBackup(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default SwitchBackupAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface SwitchBackupPageQuery extends PageQuery {
  ip?: string;
  name?: string;
  backupType?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SwitchBackupTable extends BaseType {
  ip?: string;
  name?: string;
  backupType?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SwitchBackupForm extends BaseFormType {
  ip?: string;
  name?: string;
  backupType?: string;
}
