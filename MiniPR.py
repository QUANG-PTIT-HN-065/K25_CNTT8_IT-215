from fastapi import FastAPI, Request, status, HTTPException
from fastapi.responses import JSONResponse, Response
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Tuple
from datetime import datetime, timezone
import re

app = FastAPI()

tasks_db = {
    1: {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z",
    },
    2: {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z",
    },
}


class TaskCreateSchema(BaseModel):
    title: str = Field(
        ..., min_length=3, max_length=150, description="Tiêu đề công việc"
    )
    description: str = Field(..., min_length=1, description="Mô tả công việc")
    assignee: str = Field(..., min_length=2, description="Người thực hiện")
    priority: int = Field(..., ge=1, le=5, description="Độ ưu tiên từ 1-5")

    @field_validator("assignee")
    def validate_assignee(cls, value):
        if not value.strip():
            raise ValueError(
                "Người thực hiện không được bỏ trống hoặc chỉ chứa khoảng trắng"
            )
        return value.strip()


class TaskStatusUpdateSchema(BaseModel):
    status: str = Field(..., description="Trạng thái công việc")

    @field_validator("status")
    def validate_status(cls, value):
        allowed_status = ["todo", "in_progress", "done"]
        if value not in allowed_status:
            raise ValueError(
                "Business logic error: Invalid task status value. Allowed enumerated selection list: ['todo', 'in_progress', 'done']."
            )
        return value

def unified_response(
    request: Request,
    status_code: int,
    message: str,
    data: Any = None,
    error: str = "",
) -> JSONResponse:
    """Hàm bọc dữ liệu chuẩn 6 trường"""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    content = {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": timestamp,
        "path": request.url.path,
    }
    return JSONResponse(status_code=status_code, content=content)


class BusinessException(Exception):
    def __init__(self, status_code: int, message: str, error: str):
        self.status_code = status_code
        self.message = message
        self.error = error


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    return unified_response(request, exc.status_code, exc.message, error=exc.error)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return unified_response(
        request,
        status_code=422,
        message="Lỗi: Dữ liệu đầu vào sai định dạng hoặc thiếu trường bắt buộc!",
        error="ERR-VAL-422: Gateway validation error: Input json parameters datatype hints mismatch or core required fields missing.",
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return unified_response(
        request,
        status_code=500,
        message="Lỗi hệ thống không xác định!",
        error="ERR-SYS-500: Internal Server Error. Please contact backend administrator.",
    )


def calculate_team_metrics() -> Tuple[int, int, float]:
    """Sử dụng tasks_db.values() để duyệt Dictionary"""
    total_tasks = len(tasks_db)
    if total_tasks == 0:
        return (0, 0, 0.0)

    completed_tasks = sum(1 for task in tasks_db.values() if task["status"] == "done")
    completion_rate = (completed_tasks / total_tasks) * 100.0
    return (total_tasks, completed_tasks, completion_rate)


@app.get("/tasks/analytics/dashboard")
async def get_dashboard_analytics(request: Request):
    total, completed, rate = calculate_team_metrics()
    data = {
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_rate_percentage": round(rate, 2),
    }
    return unified_response(
        request, 200, "Lấy số liệu thống kê hiệu suất nhóm thành công!", data=data
    )


@app.get("/tasks/search")
async def search_tasks(
    request: Request, keyword: Optional[str] = None, status: Optional[str] = None
):
    results = list(tasks_db.values())

    if status:
        results = [task for task in results if task["status"] == status]

    if keyword:
        pattern = re.compile(keyword, re.IGNORECASE)
        results = [
            task
            for task in results
            if pattern.search(task["title"]) or pattern.search(task["assignee"])
        ]

    data = {"total": len(results), "results": results}
    return unified_response(request, 200, "Tìm kiếm công việc thành công!", data=data)


@app.get("/tasks")
async def get_all_tasks(request: Request, status: Optional[str] = None):
    filtered_tasks = list(tasks_db.values())
    if status:
        filtered_tasks = [task for task in filtered_tasks if task["status"] == status]
    return unified_response(
        request, 200, "Lấy danh sách công việc thành công!", data=filtered_tasks
    )


@app.get("/tasks/{task_id}")
async def read_task_detail(request: Request, task_id: int):
    task = tasks_db.get(task_id)

    if not task:
        raise BusinessException(
            404,
            "Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            "ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope.",
        )
    return unified_response(
        request, 200, "Truy vấn chi tiết công việc thành công!", data=task
    )


@app.post("/tasks")
async def create_task(request: Request, task_in: TaskCreateSchema):
    for task in tasks_db.values():
        if task["title"] == task_in.title:
            raise BusinessException(
                400,
                "Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                "ERR-TASK-01: Task conflict: Title field duplicates an existing record.",
            )

    new_id = max(tasks_db.keys(), default=0) + 1

    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee,
        "priority": task_in.priority,
        "status": "todo",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    tasks_db[new_id] = new_task
    return unified_response(
        request, 201, "Khởi tạo công việc mới thành công!", data=new_task
    )


@app.put("/tasks/{task_id}")
async def update_task_status(
    request: Request, task_id: int, status_in: TaskStatusUpdateSchema
):
    if task_id not in tasks_db:
        raise BusinessException(
            404,
            "Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            "ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope.",
        )

    current_task = tasks_db[task_id]

    if current_task["status"] == "done":
        raise BusinessException(
            400,
            "Lỗi: Trạng thái công việc cập nhật không đúng quy định (Không được cập nhật khi đã Done)!",
            "ERR-TASK-03: Business logic error: Cannot update status backwards if already done.",
        )

    current_task["status"] = status_in.status
    tasks_db[task_id] = current_task

    return unified_response(
        request, 200, "Cập nhật tiến độ công việc thành công!", data=current_task
    )


@app.delete("/tasks/{task_id}")
async def delete_task(request: Request, task_id: int):
    if task_id not in tasks_db:
        raise BusinessException(
            404,
            "Lỗi: Không tìm thấy ID công việc yêu cầu trong hệ thống!",
            "ERR-TASK-04: Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope.",
        )

    tasks_db.pop(task_id)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
