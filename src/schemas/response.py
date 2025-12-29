from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ExportDataBlock(BaseModel):
    # optional to handle API error responses without crashing
    csv_lines: Optional[List[str]] = Field(default=None, alias="EXPORT_DATA")
    error_detail: Optional[Any] = Field(default=None, alias="ERROR_DETAIL")


class ExportResponse(BaseModel):
    error_code: str = Field(alias="ERROR_CODE")
    data: Optional[ExportDataBlock] = Field(default=None, alias="DATA")
