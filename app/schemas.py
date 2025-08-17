from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    version: str = Field(..., description="API version")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class DataAnalysisRequest(BaseModel):
    """Request model for data analysis"""
    csv_data: str = Field(..., description="CSV data as string")
    detect_anomalies: bool = Field(default=True, description="Whether to detect anomalies")
    analysis_type: str = Field(default="full", description="Type of analysis: basic, full, or custom")
    
    class Config:
        schema_extra = {
            "example": {
                "csv_data": "name,age,city\nJohn,25,NYC\nJane,30,LA",
                "detect_anomalies": True,
                "analysis_type": "full"
            }
        }

class ColumnInfo(BaseModel):
    """Information about a data column"""
    name: str
    dtype: str
    null_count: int
    null_percentage: float
    unique_count: int
    sample_values: List[Any]

class StatisticalSummary(BaseModel):
    """Statistical summary for numerical columns"""
    count: float
    mean: float
    std: float
    min: float
    q25: float
    q50: float
    q75: float
    max: float

class AnomalyInfo(BaseModel):
    """Information about detected anomalies"""
    column_name: str
    anomaly_type: str  # outlier, missing, duplicate, etc.
    anomaly_count: int
    anomaly_indices: List[int]
    severity: str  # low, medium, high

class EDAResults(BaseModel):
    """Exploratory Data Analysis results"""
    data_info: Dict[str, Any]
    column_info: List[ColumnInfo]
    missing_data_summary: Dict[str, Any]
    duplicate_rows: int
    data_types: Dict[str, str]
    shape: tuple

class StatisticsResults(BaseModel):
    """Statistical analysis results"""
    numerical_summary: Dict[str, StatisticalSummary]
    categorical_summary: Dict[str, Dict[str, Any]]
    correlation_matrix: Optional[Dict[str, Dict[str, float]]]
    distribution_info: Dict[str, Dict[str, Any]]

class DataAnalysisResponse(BaseModel):
    """Response model for data analysis"""
    success: bool
    message: str
    eda_results: EDAResults
    statistics: StatisticsResults
    anomalies: Optional[List[AnomalyInfo]]
    data_shape: tuple
    processing_time: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

class ReportRequest(BaseModel):
    """Request model for generating reports"""
    analysis_id: str
    report_format: str = Field(default="pdf", description="Report format: pdf, html, or json")
    include_charts: bool = Field(default=True, description="Whether to include charts in the report")
    custom_sections: Optional[List[str]] = Field(default=None, description="Custom sections to include")

class ReportResponse(BaseModel):
    """Response model for report generation"""
    success: bool
    report_url: Optional[str] = None
    report_id: str
    message: str
    generated_at: datetime = Field(default_factory=datetime.now)
