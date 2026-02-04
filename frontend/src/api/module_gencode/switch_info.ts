import request from "@/utils/request";

const API_PATH = "/gencode/switch_info";

const SwitchInfoAPI = {
  // 列表查询
  listSwitchInfo(query: SwitchInfoPageQuery) {
    return request<ApiResponse<PageResult<SwitchInfoTable[]>>>({
      url: `${API_PATH}/list`,
      method: "get",
      params: query,
    });
  },

  // 详情查询
  detailSwitchInfo(id: number) {
    return request<ApiResponse<SwitchInfoTable>>({
      url: `${API_PATH}/detail/${id}`,
      method: "get",
    });
  },

  // 新增
  createSwitchInfo(body: SwitchInfoForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/create`,
      method: "post",
      data: body,
    });
  },

  // 修改（带主键）
  updateSwitchInfo(id: number, body: SwitchInfoForm) {
    return request<ApiResponse>({
      url: `${API_PATH}/update/${id}`,
      method: "put",
      data: body,
    });
  },

  // 删除（支持批量）
  deleteSwitchInfo(ids: number[]) {
    return request<ApiResponse>({
      url: `${API_PATH}/delete`,
      method: "delete",
      data: ids,
    });
  },

  // 批量启用/停用
  batchSwitchInfo(body: BatchType) {
    return request<ApiResponse>({
      url: `${API_PATH}/available/setting`,
      method: "patch",
      data: body,
    });
  },

  // 导出
  exportSwitchInfo(query: SwitchInfoPageQuery) {
    return request<Blob>({
      url: `${API_PATH}/export`,
      method: "post",
      data: query,
      responseType: "blob",
    });
  },

  // 下载导入模板
  downloadTemplateSwitchInfo() {
    return request<Blob>({
      url: `${API_PATH}/download/template`,
      method: "post",
      responseType: "blob",
    });
  },

  // 导入
  importSwitchInfo(body: FormData) {
    return request<ApiResponse>({
      url: `${API_PATH}/import`,
      method: "post",
      data: body,
      headers: { "Content-Type": "multipart/form-data" },
    });
  },
};

export default SwitchInfoAPI;

// ------------------------------
// TS 类型声明
// ------------------------------

// 列表查询参数
export interface SwitchInfoPageQuery extends PageQuery {
  name?: string;
  ip?: string;
  brand?: string;
  model?: string;
  manageWay?: string;
  serviceType?: string;
  location?: string;
  status?: string;
  created_id?: number;
  updated_id?: number;
  created_time?: string[];
  updated_time?: string[];
}

// 列表展示项
export interface SwitchInfoTable extends BaseType {
  name?: string;
  ip?: string;
  brand?: string;
  model?: string;
  manageWay?: string;
  username?: string;
  password?: string;
  enablePassword?: string;
  serviceType?: string;
  location?: string;
  created_id?: string;
  updated_id?: string;
  created_by?: CommonType;
  updated_by?: CommonType;
}

// 新增/修改/详情表单参数
export interface SwitchInfoForm extends BaseFormType {
  name?: string;
  ip?: string;
  brand?: string;
  model?: string;
  manageWay?: string;
  username?: string;
  password?: string;
  enablePassword?: string;
  serviceType?: string;
  location?: string;
}
