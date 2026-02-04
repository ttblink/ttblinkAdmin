<!-- 交换机信息 -->
<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div v-show="visible" class="search-container">
      <el-form
        ref="queryFormRef"
        :model="queryFormData"
        label-suffix=":"
        :inline="true"
        @submit.prevent="handleQuery"
      >
        <el-form-item label="名称" prop="name">
          <el-input v-model="queryFormData.name" placeholder="请输入名称" clearable />
        </el-form-item>
        <el-form-item label="IP" prop="ip">
          <el-input v-model="queryFormData.ip" placeholder="请输入IP" clearable />
        </el-form-item>
        <el-form-item label="品牌" prop="brand">
          <el-input v-model="queryFormData.brand" placeholder="请输入品牌" clearable />
        </el-form-item>
        <el-form-item label="型号" prop="model">
          <el-input v-model="queryFormData.model" placeholder="请输入型号" clearable />
        </el-form-item>
        <el-form-item label="管理方式" prop="manageWay">
          <el-input v-model="queryFormData.manageWay" placeholder="请输入管理方式" clearable />
        </el-form-item>
        <el-form-item label="服务类型" prop="serviceType">
          <el-input v-model="queryFormData.serviceType" placeholder="请输入服务类型" clearable />
        </el-form-item>
        <el-form-item label="安装位置" prop="location">
          <el-input v-model="queryFormData.location" placeholder="请输入安装位置" clearable />
        </el-form-item>
        <el-form-item prop="status" label="状态">
          <el-select
            v-model="queryFormData.status"
            placeholder="请选择状态"
            style="width: 170px"
            clearable
          >
            <el-option value="0" label="启用" />
            <el-option value="1" label="停用" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="isExpand" prop="created_time" label="创建时间">
          <DatePicker
            v-model="createdDateRange"
            @update:model-value="handleCreatedDateRangeChange"
          />
        </el-form-item>
        <el-form-item v-if="isExpand" prop="updated_time" label="更新时间">
          <DatePicker
            v-model="updatedDateRange"
            @update:model-value="handleUpdatedDateRangeChange"
          />
        </el-form-item>
        <el-form-item v-if="isExpand" prop="created_id" label="创建人">
          <UserTableSelect
            v-model="queryFormData.created_id"
            @confirm-click="handleConfirm"
            @clear-click="handleQuery"
          />
        </el-form-item>
        <el-form-item v-if="isExpand" prop="updated_id" label="更新人">
          <UserTableSelect
            v-model="queryFormData.updated_id"
            @confirm-click="handleConfirm"
            @clear-click="handleQuery"
          />
        </el-form-item>
        <!-- 查询、重置、展开/收起按钮 -->
        <el-form-item>
          <el-button
            v-hasPerm="['module_gencode:switch_info:query']"
            type="primary"
            icon="search"
            @click="handleQuery"
          >
            查询
          </el-button>
          <el-button
            v-hasPerm="['module_gencode:switch_info:query']"
            icon="refresh"
            @click="handleResetQuery"
          >
            重置
          </el-button>
          <!-- 展开/收起 -->
          <template v-if="isExpandable">
            <el-link class="ml-3" type="primary" underline="never" @click="isExpand = !isExpand">
              {{ isExpand ? "收起" : "展开" }}
              <el-icon>
                <template v-if="isExpand">
                  <ArrowUp />
                </template>
                <template v-else>
                  <ArrowDown />
                </template>
              </el-icon>
            </el-link>
          </template>
        </el-form-item>
      </el-form>
    </div>

    <!-- 内容区域 -->
    <el-card class="data-table">
      <template #header>
        <div class="card-header">
          <span>
            交换机信息列表
            <el-tooltip content="交换机信息列表">
              <QuestionFilled class="w-4 h-4 mx-1" />
            </el-tooltip>
          </span>
        </div>
      </template>

      <!-- 功能区域 -->
      <div class="data-table__toolbar">
        <div class="data-table__toolbar--left">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:switch_info:create']"
                type="success"
                icon="plus"
                @click="handleOpenDialog('create')"
              >
                新增
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:switch_info:delete']"
                type="danger"
                icon="delete"
                :disabled="selectIds.length === 0"
                @click="handleDelete(selectIds)"
              >
                批量删除
              </el-button>
            </el-col>
            <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:switch_info:getSwitchConfig']"
                type="primary"
                icon="Document"
                :disabled="selectIds.length !== 1"
                @click="handleOpenDialog('backup',selectIds[0])"
              >
                获取配置
              </el-button>
            </el-col>
            <!-- <el-col :span="1.5">
              <el-button
                v-hasPerm="['module_gencode:switch_info:batch']"
                type="primary"
                icon="Operation"
                :disabled="selectIds.length <=1"
                @click=""
              >
                批量备份
              </el-button>
            </el-col> -->
            <el-col :span="1.5">
              <el-dropdown v-hasPerm="['module_gencode:switch_info:batch']" trigger="click">
                <el-button type="default" :disabled="selectIds.length === 0" icon="ArrowDown">
                  更多
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :icon="Check" @click="handleMoreClick('0')">
                      批量启用
                    </el-dropdown-item>
                    <el-dropdown-item :icon="CircleClose" @click="handleMoreClick('1')">
                      批量停用
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </el-col>
          </el-row>
        </div>
        <div class="data-table__toolbar--right">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-tooltip content="导入">
                <el-button
                  v-hasPerm="['module_gencode:switch_info:import']"
                  type="success"
                  icon="upload"
                  circle
                  @click="handleOpenImportDialog"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="导出">
                <el-button
                  v-hasPerm="['module_gencode:switch_info:export']"
                  type="warning"
                  icon="download"
                  circle
                  @click="handleOpenExportsModal"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="搜索显示/隐藏">
                <el-button
                  v-hasPerm="['*:*:*']"
                  type="info"
                  icon="search"
                  circle
                  @click="visible = !visible"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip content="刷新">
                <el-button
                  v-hasPerm="['module_gencode:switch_info:query']"
                  type="primary"
                  icon="refresh"
                  circle
                  @click="handleRefresh"
                />
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-popover placement="bottom" trigger="click">
                <template #reference>
                  <el-button type="danger" icon="operation" circle></el-button>
                </template>
                <el-scrollbar max-height="350px">
                  <template v-for="column in tableColumns" :key="column.prop">
                    <el-checkbox v-if="column.prop" v-model="column.show" :label="column.label" />
                  </template>
                </el-scrollbar>
              </el-popover>
            </el-col>
          </el-row>
        </div>
      </div>

      <!-- 表格区域：系统配置列表 -->
      <el-table
        ref="tableRef"
        v-loading="loading"
        :data="pageTableData"
        highlight-current-row
        class="data-table__content"
        :height="450"
        border
        stripe
        @selection-change="handleSelectionChange"
      >
        <template #empty>
          <el-empty :image-size="80" description="暂无数据" />
        </template>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'selection')?.show"
          type="selection"
          min-width="55"
          align="center"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'index')?.show"
          fixed
          label="序号"
          min-width="60"
        >
          <template #default="scope">
            {{ (queryFormData.page_no - 1) * queryFormData.page_size + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'name')?.show"
          label="名称"
          prop="name"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'ip')?.show"
          label="IP"
          prop="ip"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'brand')?.show"
          label="品牌"
          prop="brand"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'model')?.show"
          label="型号"
          prop="model"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'manageWay')?.show"
          label="管理方式"
          prop="manageWay"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'username')?.show"
          label="用户名"
          prop="username"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'password')?.show"
          label="密码"
          prop="password"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'enablePassword')?.show"
          label="enable密码"
          prop="enablePassword"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'serviceType')?.show"
          label="服务类型"
          prop="serviceType"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'location')?.show"
          label="安装位置"
          prop="location"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'status')?.show"
          label="是否启用(0:启用 1:禁用)"
          prop="status"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'status')?.show"
          label="是否启用(0:启用 1:禁用)"
          prop="status"
          min-width="140"
        >
          <template #default="scope">
            <el-tag :type="scope.row.status == '0' ? 'success' : 'info'">
              {{ scope.row.status == "0" ? "启用" : "停用" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'description')?.show"
          label="备注/描述"
          prop="description"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'created_time')?.show"
          label="创建时间"
          prop="created_time"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'updated_time')?.show"
          label="更新时间"
          prop="updated_time"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'created_id')?.show"
          label="创建人ID"
          prop="created_id"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'created_id')?.show"
          label="创建人ID"
          prop="created_id"
          min-width="140"
        >
          <template #default="scope">
            <el-tag>{{ scope.row.created_by?.name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'updated_id')?.show"
          label="更新人ID"
          prop="updated_id"
          min-width="140"
        />
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'updated_id')?.show"
          label="更新人ID"
          prop="updated_id"
          min-width="140"
        >
          <template #default="scope">
            <el-tag>{{ scope.row.updated_by?.name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          v-if="tableColumns.find((col) => col.prop === 'operation')?.show"
          fixed="right"
          label="操作"
          align="center"
          min-width="180"
        >
          <template #default="scope">
            <el-button
              v-hasPerm="['module_gencode:switch_info:detail']"
              type="info"
              size="small"
              link
              icon="document"
              @click="handleOpenDialog('detail', scope.row.id)"
            >
              详情
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:switch_info:update']"
              type="primary"
              size="small"
              link
              icon="edit"
              @click="handleOpenDialog('update', scope.row.id)"
            >
              编辑
            </el-button>
            <el-button
              v-hasPerm="['module_gencode:switch_info:delete']"
              type="danger"
              size="small"
              link
              icon="delete"
              @click="handleDelete([scope.row.id])"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页区域 -->
      <template #footer>
        <pagination
          v-model:total="total"
          v-model:page="queryFormData.page_no"
          v-model:limit="queryFormData.page_size"
          @pagination="loadingData"
        />
      </template>
    </el-card>

    <!-- 弹窗区域 -->
    <el-dialog
      v-model="dialogVisible.visible"
      :title="dialogVisible.title"
      @close="handleCloseDialog"
    >
      <!-- 详情 -->
      <template v-if="dialogVisible.type === 'detail'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="名称" :span="2">
            {{ detailFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="IP" :span="2">
            {{ detailFormData.ip }}
          </el-descriptions-item>
          <el-descriptions-item label="品牌" :span="2">
            {{ detailFormData.brand }}
          </el-descriptions-item>
          <el-descriptions-item label="型号" :span="2">
            {{ detailFormData.model }}
          </el-descriptions-item>
          <el-descriptions-item label="管理方式" :span="2">
            {{ detailFormData.manageWay }}
          </el-descriptions-item>
          <el-descriptions-item label="用户名" :span="2">
            {{ detailFormData.username }}
          </el-descriptions-item>
          <el-descriptions-item label="密码" :span="2">
            {{ detailFormData.password }}
          </el-descriptions-item>
          <el-descriptions-item label="enable密码" :span="2">
            {{ detailFormData.enablePassword }}
          </el-descriptions-item>
          <el-descriptions-item label="服务类型" :span="2">
            {{ detailFormData.serviceType }}
          </el-descriptions-item>
          <el-descriptions-item label="安装位置" :span="2">
            {{ detailFormData.location }}
          </el-descriptions-item>
          <el-descriptions-item label="主键ID" :span="2">
            {{ detailFormData.id }}
          </el-descriptions-item>
          <el-descriptions-item label="UUID全局唯一标识" :span="2">
            {{ detailFormData.uuid }}
          </el-descriptions-item>
          <el-descriptions-item label="状态" :span="2">
            <el-tag :type="detailFormData.status == '0' ? 'success' : 'danger'">
              {{ detailFormData.status == "0" ? "启用" : "停用" }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="备注/描述" :span="2">
            {{ detailFormData.description }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ detailFormData.created_time }}
          </el-descriptions-item>
          <el-descriptions-item label="更新时间" :span="2">
            {{ detailFormData.updated_time }}
          </el-descriptions-item>
          <el-descriptions-item label="创建人" :span="2">
            {{ detailFormData.created_by?.name }}
          </el-descriptions-item>
          <el-descriptions-item label="更新人" :span="2">
            {{ detailFormData.updated_by?.name }}
          </el-descriptions-item>
        </el-descriptions>
      </template>

      <!-- 新增、编辑表单 -->
      <template v-else-if="dialogVisible.type=='create' || dialogVisible.type=='update'">
        <el-form
          ref="dataFormRef"
          :model="formData"
          :rules="rules"
          label-suffix=":"
          label-width="auto"
          label-position="right"
        >
          <el-form-item label="名称" prop="name" :required="false">
            <el-input v-model="formData.name" placeholder="请输入名称" />
          </el-form-item>
          <el-form-item label="IP" prop="ip" :required="false">
            <el-input v-model="formData.ip" placeholder="请输入IP" />
          </el-form-item>
          <el-form-item label="品牌" prop="brand" :required="false">
            <el-input v-model="formData.brand" placeholder="请输入品牌" />
          </el-form-item>
          <el-form-item label="型号" prop="model" :required="false">
            <el-input v-model="formData.model" placeholder="请输入型号" />
          </el-form-item>
          <el-form-item label="管理方式" prop="manageWay" :required="false">
            <el-input v-model="formData.manageWay" placeholder="请输入管理方式" />
          </el-form-item>
          <el-form-item label="用户名" prop="username" :required="false">
            <el-input v-model="formData.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password" :required="false">
            <el-input v-model="formData.password" placeholder="请输入密码" />
          </el-form-item>
          <el-form-item label="enable密码" prop="enablePassword" :required="false">
            <el-input v-model="formData.enablePassword" placeholder="请输入enable密码" />
          </el-form-item>
          <el-form-item label="服务类型" prop="serviceType" :required="false">
            <el-input v-model="formData.serviceType" placeholder="请输入服务类型" />
          </el-form-item>
          <el-form-item label="安装位置" prop="location" :required="false">
            <el-input v-model="formData.location" placeholder="请输入安装位置" />
          </el-form-item>
          <el-form-item label="状态" prop="status" :required="true">
            <el-radio-group v-model="formData.status">
              <el-radio value="0">启用</el-radio>
              <el-radio value="1">停用</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="描述" prop="description">
            <el-input
              v-model="formData.description"
              :rows="4"
              :maxlength="100"
              show-word-limit
              type="textarea"
              placeholder="请输入描述"
            />
          </el-form-item>
        </el-form>
      </template>

      <!-- 备份表单 -->
      <template v-else-if="dialogVisible.type=='backup'">
        <el-descriptions :column="4" border>
          <el-descriptions-item label="交换机名称" :span="2">
            {{ backupFormData.name }}
          </el-descriptions-item>
          <el-descriptions-item label="交换机IP" :span="2">
            {{ backupFormData.ip }}
          </el-descriptions-item>
          <el-descriptions-item label="交换机品牌" :span="2">
            {{ backupFormData.brand }}
          </el-descriptions-item>
          <el-descriptions-item label="管理方式" :span="2">
            {{ backupFormData.manageWay }}
          </el-descriptions-item>
          <el-descriptions-item label="用户名" :span="4">
            {{ backupFormData.username }}
          </el-descriptions-item>
          <el-descriptions-item label="密码" :span="2">
            {{ backupFormData.password }}
          </el-descriptions-item>
          <el-descriptions-item label="enable密码" :span="2">
            {{ backupFormData.enablePassword }}
          </el-descriptions-item>
        </el-descriptions>
        <div style="margin-top: 10px;margin-bottom: 10px;">
          <el-row :gutter="10">
            <el-col :span="1.5">
              <el-button type="primary" @click="getSwitchConfig(backupFormData)">获取设备配置</el-button>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip 
                content="将配置文件上传到服务器的 /switchconfig/ 目录"
                placement="top"
              >
                <el-button 
                  type="success" 
                  :disabled="saveConfigToServer" 
                  icon="download" 
                  @click="saveConfig('server')"
                >
                  保存配置到服务器
                </el-button>
              </el-tooltip>
            </el-col>
            <el-col :span="1.5">
              <el-tooltip 
                content="将配置文件下载到本地计算机"
                placement="top"
              >
                <el-button 
                  type="success" 
                  :disabled="saveConfigToLocal" 
                  icon="download" 
                  @click="saveConfig('local')"
                >
                  保存配置到本地
                </el-button>
              </el-tooltip>
            </el-col>
          </el-row>
        </div>
        <el-input v-loading="getSwitchConfigLoading" v-model="switchConfig" type="textarea" :rows="10"></el-input>
      </template>

      <template #footer>
        <div class="dialog-footer">
          <!-- 详情弹窗不需要确定按钮的提交逻辑 -->
          <el-button @click="handleCloseDialog">取消</el-button>
          <el-button v-if="dialogVisible.type !== 'detail'" type="primary" @click="handleSubmit">
            确定
          </el-button>
          <el-button v-else type="primary" @click="handleCloseDialog">确定</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 导入弹窗 -->
    <ImportModal
      v-model="importDialogVisible"
      :content-config="curdContentConfig"
      @upload="handleUpload"
    />

    <!-- 导出弹窗 -->
    <ExportModal
      v-model="exportsDialogVisible"
      :content-config="curdContentConfig"
      :query-params="queryFormData"
      :page-data="pageTableData"
      :selection-data="selectionRows"
    />
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: "SwitchInfo",
  inheritAttrs: false,
});

import { ref, reactive, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { QuestionFilled, ArrowUp, ArrowDown, Check, CircleClose } from "@element-plus/icons-vue";
import { formatToDateTime } from "@/utils/dateUtil";
import { useDictStore } from "@/store";
import { ResultEnum } from "@/enums/api/result.enum";
import DatePicker from "@/components/DatePicker/index.vue";
import type { IContentConfig } from "@/components/CURD/types";
import ImportModal from "@/components/CURD/ImportModal.vue";
import ExportModal from "@/components/CURD/ExportModal.vue";
import SwitchInfoAPI, {
  SwitchInfoPageQuery,
  SwitchInfoTable,
  SwitchInfoForm,
  SwitchInfoConnectForm,
} from "@/api/module_gencode/switch_info";
import ResourceAPI from "@/api/module_monitor/resource";

const visible = ref(true);
const isExpand = ref(false);
const isExpandable = ref(true);
const queryFormRef = ref();
const dataFormRef = ref();
const total = ref(0);
const selectIds = ref<number[]>([]);
const selectionRows = ref<SwitchInfoTable[]>([]);
const loading = ref(false);
const getSwitchConfigLoading = ref(false);
const switchConfig = ref(""); //获取的交换机的配置内容
const saveConfigToServer = ref(true); //是否保存配置到服务器
const saveConfigToLocal = ref(true); //是否保存配置到本地

// 字典仓库与需要加载的字典类型
const dictStore = useDictStore();
const dictTypes: any = [
];

// 分页表单
const pageTableData = ref<SwitchInfoTable[]>([]);

// 表格列配置
const tableColumns = ref([
  { prop: "selection", label: "选择框", show: true },
  { prop: "index", label: "序号", show: true },
  { prop: "name", label: "名称", show: true },
  { prop: "ip", label: "IP", show: true },
  { prop: "brand", label: "品牌", show: true },
  { prop: "model", label: "型号", show: true },
  { prop: "manageWay", label: "管理方式", show: true },
  { prop: "username", label: "用户名", show: true },
  { prop: "password", label: "密码", show: true },
  { prop: "enablePassword", label: "enable密码", show: true },
  { prop: "serviceType", label: "服务类型", show: true },
  { prop: "location", label: "安装位置", show: true },
  { prop: "status", label: "是否启用(0:启用 1:禁用)", show: true },
  { prop: "description", label: "备注/描述", show: true },
  { prop: "created_time", label: "创建时间", show: true },
  { prop: "updated_time", label: "更新时间", show: true },
  { prop: "created_id", label: "创建人ID", show: true },
  { prop: "updated_id", label: "更新人ID", show: true },
  { prop: "operation", label: "操作", show: true },
]);

// 导出列（不含选择/序号/操作）
const exportColumns = [
  { prop: "name", label: "名称" },
  { prop: "ip", label: "IP" },
  { prop: "brand", label: "品牌" },
  { prop: "model", label: "型号" },
  { prop: "manageWay", label: "管理方式" },
  { prop: "username", label: "用户名" },
  { prop: "password", label: "密码" },
  { prop: "enablePassword", label: "enable密码" },
  { prop: "serviceType", label: "服务类型" },
  { prop: "location", label: "安装位置" },
  { prop: "status", label: "是否启用(0:启用 1:禁用)" },
  { prop: "description", label: "备注/描述" },
  { prop: "created_time", label: "创建时间" },
  { prop: "updated_time", label: "更新时间" },
  { prop: "created_id", label: "创建人ID" },
  { prop: "updated_id", label: "更新人ID" },
];

// 导入/导出配置
const curdContentConfig = {
  permPrefix: "module_gencode:switch_info",
  cols: exportColumns as any,
  importTemplate: () => SwitchInfoAPI.downloadTemplateSwitchInfo(),
  exportsAction: async (params: any) => {
    const query: any = { ...params };
    query.status = "0";
    query.page_no = 1;
    query.page_size = 9999;
    const all: any[] = [];
    while (true) {
      const res = await SwitchInfoAPI.listSwitchInfo(query);
      const items = res.data?.data?.items || [];
      const total = res.data?.data?.total || 0;
      all.push(...items);
      if (all.length >= total || items.length === 0) break;
      query.page_no += 1;
    }
    return all;
  },
} as unknown as IContentConfig;

// 详情表单
const detailFormData = ref<SwitchInfoTable>({});
// 日期范围临时变量
const createdDateRange = ref<[Date, Date] | []>([]);
// 更新时间范围临时变量
const updatedDateRange = ref<[Date, Date] | []>([]);

// 处理创建时间范围变化
function handleCreatedDateRangeChange(range: [Date, Date]) {
  createdDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.created_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.created_time = undefined;
  }
}

// 处理更新时间范围变化
function handleUpdatedDateRangeChange(range: [Date, Date]) {
  updatedDateRange.value = range;
  if (range && range.length === 2) {
    queryFormData.updated_time = [formatToDateTime(range[0]), formatToDateTime(range[1])];
  } else {
    queryFormData.updated_time = undefined;
  }
}

// 分页查询参数
const queryFormData = reactive<SwitchInfoPageQuery>({
  page_no: 1,
  page_size: 10,
  name: undefined,
  ip: undefined,
  brand: undefined,
  model: undefined,
  manageWay: undefined,
  serviceType: undefined,
  location: undefined,
  status: undefined,
  created_time: undefined,
  updated_time: undefined,
  created_id: undefined,
  updated_id: undefined,
});

// 编辑表单
const formData = reactive<SwitchInfoForm>({
  name: undefined,
  ip: undefined,
  brand: undefined,
  model: undefined,
  manageWay: undefined,
  username: undefined,
  password: undefined,
  enablePassword: undefined,
  serviceType: undefined,
  location: undefined,
  id: undefined,
  status: undefined,
  description: undefined,
});

// 备份配置表单
const backupFormData = reactive<SwitchInfoConnectForm>({
  name: undefined,
  ip: undefined,
  brand:undefined,
  manageWay:undefined,
  username:undefined,
  password:undefined,
  enablePassword:undefined,
});

// 弹窗状态
const dialogVisible = reactive({
  title: "",
  visible: false,
  type: "create" as "create" | "update" | "detail" | "backup",
});

// 表单验证规则
const rules = reactive({
  name: [{ required: false, message: "请输入名称", trigger: "blur" }],
  ip: [{ required: true, message: "请输入IP", trigger: "blur" }],
  brand: [{ required: true, message: "请输入品牌", trigger: "blur" }],
  model: [{ required: false, message: "请输入型号", trigger: "blur" }],
  manageWay: [{ required: true, message: "请输入管理方式", trigger: "blur" }],
  username: [{ required: false, message: "请输入用户名", trigger: "blur" }],
  password: [{ required: true, message: "请输入密码", trigger: "blur" }],
  enablePassword: [{ required: false, message: "请输入enable密码", trigger: "blur" }],
  serviceType: [{ required: false, message: "请输入服务类型", trigger: "blur" }],
  location: [{ required: false, message: "请输入安装位置", trigger: "blur" }],
  id: [{ required: false, message: "请输入主键ID", trigger: "blur" }],
  uuid: [{ required: false, message: "请输入UUID全局唯一标识", trigger: "blur" }],
  status: [{ required: false, message: "请输入是否启用(0:启用 1:禁用)", trigger: "blur" }],
  description: [{ required: false, message: "请输入备注/描述", trigger: "blur" }],
  created_time: [{ required: false, message: "请输入创建时间", trigger: "blur" }],
  updated_time: [{ required: false, message: "请输入更新时间", trigger: "blur" }],
  created_id: [{ required: true, message: "请输入创建人ID", trigger: "blur" }],
  updated_id: [{ required: true, message: "请输入更新人ID", trigger: "blur" }],
});

// 导入弹窗显示状态
const importDialogVisible = ref(false);

// 导出弹窗显示状态
const exportsDialogVisible = ref(false);

// 打开导入弹窗
function handleOpenImportDialog() {
  importDialogVisible.value = true;
}

// 打开导出弹窗
function handleOpenExportsModal() {
  exportsDialogVisible.value = true;
}

// 列表刷新
async function handleRefresh() {
  await loadingData();
}

// 加载表格数据
async function loadingData() {
  loading.value = true;
  try {
    const response = await SwitchInfoAPI.listSwitchInfo(queryFormData);
    pageTableData.value = response.data.data.items;
    total.value = response.data.data.total;
  } catch (error: any) {
    console.error(error);
  } finally {
    loading.value = false;
  }
}

// 查询（重置页码后获取数据）
async function handleQuery() {
  queryFormData.page_no = 1;
  loadingData();
}

// 选择创建人后触发查询
function handleConfirm() {
  handleQuery();
}

// 重置查询
async function handleResetQuery() {
  queryFormRef.value.resetFields();
  queryFormData.page_no = 1;
  // 重置日期范围选择器
  createdDateRange.value = [];
  updatedDateRange.value = [];
  queryFormData.created_time = undefined;
  queryFormData.updated_time = undefined;
  loadingData();
}

// 定义初始表单数据常量
const initialFormData: SwitchInfoForm = {
  name: undefined,
  ip: undefined,
  brand: undefined,
  model: undefined,
  manageWay: undefined,
  username: undefined,
  password: undefined,
  enablePassword: undefined,
  serviceType: undefined,
  location: undefined,
  id: undefined,
  status: undefined,
  description: undefined,
};

// 重置表单
async function resetForm() {
  if (dataFormRef.value) {
    dataFormRef.value.resetFields();
    dataFormRef.value.clearValidate();
  }
  // 完全重置 formData 为初始状态
  Object.assign(formData, initialFormData);
}

// 行复选框选中项变化
async function handleSelectionChange(selection: any) {
  selectIds.value = selection.map((item: any) => item.id);
  selectionRows.value = selection;
}

// 关闭弹窗
async function handleCloseDialog() {
  dialogVisible.visible = false;
  resetForm();
}

// 打开弹窗
async function handleOpenDialog(type: "create" | "update" | "detail" | "backup", id?: number) {
  dialogVisible.type = type;
  if (id) {
    const response = await SwitchInfoAPI.detailSwitchInfo(id);
    if (type === "detail") {
      dialogVisible.title = "详情";
      Object.assign(detailFormData.value, response.data.data);
    } else if (type === "update") {
      dialogVisible.title = "修改";
      Object.assign(formData, response.data.data);
    }else if (type === "backup") {
      // console.log("备份")
      dialogVisible.title = "备份";
      console.log(response.data.data)
      backupFormData.name = response.data.data.name;
      backupFormData.ip = response.data.data.ip;
      backupFormData.brand = response.data.data.brand;
      backupFormData.manageWay = response.data.data.manageWay;
      backupFormData.username = response.data.data.username;
      backupFormData.password = response.data.data.password;
      backupFormData.enablePassword = response.data.data.enablePassword;
      // console.log("backupFormData的值： ",backupFormData)
    }
  } else {
    dialogVisible.title = "新增SwitchInfo";
    formData.name = undefined;
    formData.ip = undefined;
    formData.brand = undefined;
    formData.model = undefined;
    formData.manageWay = undefined;
    formData.username = undefined;
    formData.password = undefined;
    formData.enablePassword = undefined;
    formData.serviceType = undefined;
    formData.location = undefined;
    formData.id = undefined;
    formData.status = undefined;
    formData.description = undefined;
  }
  dialogVisible.visible = true;
}

// 提交表单（防抖）
async function handleSubmit() {
  // 表单校验
  dataFormRef.value.validate(async (valid: any) => {
    if (valid) {
      loading.value = true;
      // 根据弹窗传入的参数(deatil\create\update)判断走什么逻辑
      const id = formData.id;
      if (id) {
        try {
          await SwitchInfoAPI.updateSwitchInfo(id, { id, ...formData });
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      } else {
        try {
          await SwitchInfoAPI.createSwitchInfo(formData);
          dialogVisible.visible = false;
          resetForm();
          handleCloseDialog();
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      }
    }
  });
}

// 删除、批量删除
async function handleDelete(ids: number[]) {
  ElMessageBox.confirm("确认删除该项数据?", "警告", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(async () => {
      try {
        loading.value = true;
        await SwitchInfoAPI.deleteSwitchInfo(ids);
        handleResetQuery();
      } catch (error: any) {
        console.error(error);
      } finally {
        loading.value = false;
      }
    })
    .catch(() => {
      ElMessageBox.close();
    });
}

// 批量启用/停用
async function handleMoreClick(status: string) {
  if (selectIds.value.length) {
    ElMessageBox.confirm(`确认${status === "0" ? "启用" : "停用"}该项数据?`, "警告", {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "warning",
    })
      .then(async () => {
        try {
          loading.value = true;
          await SwitchInfoAPI.batchSwitchInfo({ ids: selectIds.value, status });
          handleResetQuery();
        } catch (error: any) {
          console.error(error);
        } finally {
          loading.value = false;
        }
      })
      .catch(() => {
        ElMessageBox.close();
      });
  }
}

// 处理上传
const handleUpload = async (formData: FormData) => {
  try {
    const response = await SwitchInfoAPI.importSwitchInfo(formData);
    if (response.data.code === ResultEnum.SUCCESS) {
      ElMessage.success(`${response.data.msg}，${response.data.data}`);
      importDialogVisible.value = false;
      await handleQuery();
    }
  } catch (error: any) {
    console.error(error);
  }
};

onMounted(async () => {
  // 预加载字典数据
  if (dictTypes.length > 0) {
    await dictStore.getDict(dictTypes);
  }
  loadingData();
});


// 获取设备配置
async function getSwitchConfig(data: SwitchInfoConnectForm){
  try{
    getSwitchConfigLoading.value=true
    const response=await SwitchInfoAPI.backupConfig(data)
    console.log(response)
    if(response.status===200){
      // console.log(response.data.data)
      switchConfig.value=response.data.data
      saveConfigToServer.value=false
      saveConfigToLocal.value=false
    }else{
      switchConfig.value="获取配置失败，请检查网络或交换机连接信息是否正确！"
    }
  }
  catch(error:any){
    console.log("获取设备配置时出错："+error)
  }
  finally{
    getSwitchConfigLoading.value=false
  }
}

// 保存获取的配置
async function saveConfig(location: string) {
  console.log("保存配置到：" + location);
  
  if (location === "server") {
    // 保存配置到服务器
    try {
      // 验证配置内容
      if (!switchConfig.value || switchConfig.value.trim() === "") {
        ElMessage.warning("没有配置内容可以上传，请先获取设备配置");
        return;
      }
      
      const formData = new FormData();
      
      const blob = new Blob([switchConfig.value], { type: "text/plain;charset=utf-8" });
      const fileName = `${backupFormData.ip || "defaultIP"}${backupFormData.name ? "-" + backupFormData.name : ""}-switchConfig.txt`;
      const file = new File([blob], fileName, { type: "text/plain" });
      
      formData.append("file", file);
      // 设置目标路径为 switchconfig 目录
      formData.append("target_path", "switchconfig");
      
      const response = await ResourceAPI.uploadFile(formData);
    } catch (error: any) {
      console.error("上传配置文件失败：", error);
      ElMessage.error({
        message: `上传失败：${error.message || '网络错误'}`,
        duration: 5000,
      });
    }
  } else if (location === "local") {
    // 将 switchConfig.value 以 txt 格式保存到本地
    const blob = new Blob([switchConfig.value], { type: "text/plain;charset=utf-8" });
    const aLink = document.createElement("a");
    const fileName = `${backupFormData.ip || "defaultIP"}${backupFormData.name ? "-" + backupFormData.name : ""}-switchConfig.txt`;
    aLink.download = fileName;
    aLink.href = URL.createObjectURL(blob);
    aLink.click();
    
    // 释放 URL 对象
    setTimeout(() => {
      URL.revokeObjectURL(aLink.href);
    }, 100);
    
    ElMessage.success(`配置文件 "${fileName}" 已保存到本地！`);
  }
}

// 添加一个辅助函数格式化文件大小（与 resource.vue 中的相同）
function formatFileSize(size?: number | null) {
  if (!size || size === null) return "-";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let unitIndex = 0;
  let fileSize = size;

  while (fileSize >= 1024 && unitIndex < units.length - 1) {
    fileSize /= 1024;
    unitIndex++;
  }

  return `${fileSize.toFixed(1)} ${units[unitIndex]}`;
}
</script>

<style lang="scss" scoped></style>
