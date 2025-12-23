from typing import List

from pydantic import BaseModel, Field


class ExportDataBlock(BaseModel):
    csv_lines: List[str] = Field(alias="EXPORT_DATA")


class ExportResponse(BaseModel):
    error_code: str = Field(alias="ERROR_CODE")
    data: ExportDataBlock = Field(alias="DATA")
