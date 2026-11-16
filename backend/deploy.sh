#!/usr/bin/env bash
# =============================================================
# 校园活动系统 - 后端自动部署脚本（供宝塔 WebHook 调用）
#
# 流程：拉取代码 -> 更新虚拟环境依赖 -> 重启后端服务 -> 健康检查
# 健康检查失败时会自动回滚到上一个版本
#
# 使用前：
#   1. 按下方“配置区”修改路径、分支、服务名、端口
#   2. 服务器上给脚本执行权限：chmod +x backend/deploy.sh
#   3. 宝塔 WebHook 中执行：bash /www/wwwroot/python/graduation-project/backend/deploy.sh
# =============================================================

set -euo pipefail

# ==================== 配置区（按服务器实际修改） ====================
# 服务器上 git 仓库根目录（包含 backend/、frontend/）
PROJECT_DIR="/www/wwwroot/python/graduation-project"
# 要部署的分支（与推送触发 WebHook 的分支一致）
BRANCH="dev"
# 后端目录与虚拟环境目录
# 若使用宝塔 Python 项目自带的虚拟环境，把这里改成该环境路径（可用 ps -ef | grep uvicorn 查看）
BACKEND_DIR="$PROJECT_DIR/backend"
VENV_DIR="$BACKEND_DIR/.venv"
# 创建虚拟环境使用的 Python（需 >= 3.10），可写绝对路径，例如：
# PYTHON_BIN="/www/server/python_manager/versions/3.11.9/bin/python3"
PYTHON_BIN="/www/server/pyporject_evn/versions/3.11.9/bin/python3"
# 宝塔 Python 项目的项目名称（同时用于匹配 systemd 服务 / init.d 脚本 / supervisor 程序）
SERVICE_NAME="graduation-backend"
# 后端监听端口，必须与宝塔 Python 项目启动命令中的 --port 一致
PORT=8080
# pip 安装源（国内服务器建议用镜像）
PIP_INDEX="https://pypi.tuna.tsinghua.edu.cn/simple"
# 部署日志文件
LOG_FILE="/www/wwwlogs/graduation-backend-deploy.log"
# 自定义重启命令，留空则自动检测 systemd / init.d / supervisor
# 例如宝塔“Python 项目”若不在上述管理方式内，可填："btpython restart graduation-backend"
RESTART_CMD=""
# ==================================================================

# 保证 WebHook 的非交互环境也能找到常用命令
export PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:${PATH:-}"

# 日志不可写时退回 /tmp
if ! touch "$LOG_FILE" 2>/dev/null; then
  LOG_FILE="/tmp/graduation-backend-deploy.log"
  touch "$LOG_FILE"
fi

# 把 stderr 合并到 stdout，让 git 等命令的报错也出现在面板日志里
exec 2>&1

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG_FILE"
}

fail() {
  log "[ERROR] $*"
  exit 1
}

# 防止多次推送并发部署
LOCK_FILE="/tmp/graduation-backend-deploy.lock"
exec 9>"$LOCK_FILE"
if command -v flock >/dev/null 2>&1; then
  flock -n 9 || { log "已有部署任务在执行，跳过本次"; exit 0; }
fi

health_check() {
  if ! command -v curl >/dev/null 2>&1; then
    log "[WARN] 未找到 curl，跳过健康检查"
    return 0
  fi
  for _ in $(seq 1 15); do
    if curl -fsS --max-time 3 -o /dev/null "http://127.0.0.1:${PORT}/docs"; then
      return 0
    fi
    sleep 1
  done
  return 1
}

restart_service() {
  if [ -n "$RESTART_CMD" ]; then
    bash -c "$RESTART_CMD" >>"$LOG_FILE" 2>&1 && return 0
    return 1
  fi
  if systemctl cat "${SERVICE_NAME}.service" >/dev/null 2>&1; then
    systemctl restart "$SERVICE_NAME" >>"$LOG_FILE" 2>&1 && return 0
  fi
  if [ -x "/etc/init.d/${SERVICE_NAME}" ]; then
    "/etc/init.d/${SERVICE_NAME}" restart >>"$LOG_FILE" 2>&1 && return 0
  fi
  if command -v supervisorctl >/dev/null 2>&1 \
    && supervisorctl status "$SERVICE_NAME" >/dev/null 2>&1; then
    supervisorctl restart "$SERVICE_NAME" >>"$LOG_FILE" 2>&1 && return 0
  fi
  return 1
}

log "========== 开始部署后端 =========="
log "执行用户：$(id -un 2>/dev/null || echo unknown)，HOME=${HOME:-未设置}"

# ---------- 环境检查 ----------
[ -d "$PROJECT_DIR/.git" ] || fail "未找到 git 仓库：$PROJECT_DIR"
[ -d "$BACKEND_DIR" ] || fail "未找到后端目录：$BACKEND_DIR"
command -v git >/dev/null 2>&1 || fail "服务器未安装 git"

# 通过环境变量告诉 git 本项目是安全目录，避免 WebHook 环境缺少 HOME 或属主不一致导致失败
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0="safe.directory"
export GIT_CONFIG_VALUE_0="$PROJECT_DIR"

# ---------- 拉取代码 ----------
if ! OLD_COMMIT="$(git -C "$PROJECT_DIR" rev-parse HEAD)"; then
  fail "读取当前提交失败，请确认 $PROJECT_DIR 是有效仓库"
fi
log "拉取远程分支 origin/$BRANCH ..."
if ! git -C "$PROJECT_DIR" fetch --prune origin "$BRANCH" >>"$LOG_FILE" 2>&1; then
  fail "git fetch 失败，请检查服务器能否访问远程仓库"
fi
if ! NEW_COMMIT="$(git -C "$PROJECT_DIR" rev-parse "origin/${BRANCH}")"; then
  fail "读取远程分支 origin/$BRANCH 失败"
fi

REQ_CHANGED=0
if ! git -C "$PROJECT_DIR" diff --quiet "$OLD_COMMIT" "$NEW_COMMIT" -- backend/requirements.txt; then
  REQ_CHANGED=1
fi

if [ "$OLD_COMMIT" != "$NEW_COMMIT" ]; then
  log "代码更新：${OLD_COMMIT:0:8} -> ${NEW_COMMIT:0:8}"
  git -C "$PROJECT_DIR" checkout -f -B "$BRANCH" "origin/${BRANCH}" >>"$LOG_FILE" 2>&1 \
    || fail "切换代码版本失败"
else
  log "代码已是最新：${NEW_COMMIT:0:8}"
fi

# ---------- 虚拟环境与依赖 ----------
NEED_INSTALL=0
if [ ! -x "$VENV_DIR/bin/python" ]; then
  log "创建虚拟环境：$VENV_DIR"
  "$PYTHON_BIN" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null \
    || fail "需要 Python 3.10+，请检查 PYTHON_BIN 配置"
  "$PYTHON_BIN" -m venv "$VENV_DIR" \
    || fail "创建虚拟环境失败，请确认已安装 python3-venv 或改用宝塔的 Python"
  NEED_INSTALL=1
fi

if [ "$REQ_CHANGED" -eq 1 ]; then
  NEED_INSTALL=1
fi

if [ "$NEED_INSTALL" -eq 0 ]; then
  log "依赖无变化，跳过安装"
else
  log "安装/更新依赖..."
  "$VENV_DIR/bin/python" -m pip install --upgrade pip -i "$PIP_INDEX" >>"$LOG_FILE" 2>&1 \
    || log "[WARN] pip 升级失败，继续安装依赖"
  if ! "$VENV_DIR/bin/python" -m pip install -r "$BACKEND_DIR/requirements.txt" -i "$PIP_INDEX" 2>&1 \
    | tee -a "$LOG_FILE"; then
    fail "依赖安装失败，请查看上方日志"
  fi
fi

# ---------- 重启服务 ----------
log "重启服务：$SERVICE_NAME"
if ! restart_service; then
  fail "重启失败：未找到 $SERVICE_NAME 对应的 systemd 服务 / init.d 脚本 / supervisor 程序。请检查 SERVICE_NAME 或配置 RESTART_CMD"
fi

# ---------- 健康检查与回滚 ----------
if health_check; then
  log "健康检查通过：http://127.0.0.1:${PORT}/docs"
  log "========== 部署成功：$(git -C "$PROJECT_DIR" rev-parse --short HEAD) =========="
  exit 0
fi

log "[ERROR] 健康检查失败：http://127.0.0.1:${PORT}/docs"
if [ "$OLD_COMMIT" != "$NEW_COMMIT" ]; then
  log "开始回滚到 ${OLD_COMMIT:0:8}"
  git -C "$PROJECT_DIR" reset --hard "$OLD_COMMIT" >>"$LOG_FILE" 2>&1 || log "[ERROR] 回滚代码失败"
  if [ "$REQ_CHANGED" -eq 1 ]; then
    "$VENV_DIR/bin/python" -m pip install -r "$BACKEND_DIR/requirements.txt" -i "$PIP_INDEX" >>"$LOG_FILE" 2>&1 \
      || log "[ERROR] 回滚时依赖安装失败"
  fi
  if restart_service; then
    if health_check; then
      log "回滚成功，服务已恢复到 ${OLD_COMMIT:0:8}"
    else
      log "[ERROR] 回滚后健康检查仍失败，请登录服务器查看日志"
    fi
  else
    log "[ERROR] 回滚时重启服务失败"
  fi
fi

exit 1
