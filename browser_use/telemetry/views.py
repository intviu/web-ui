"""
View models for telemetry.
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class TelemetryEvent(BaseModel):
    """Base class for telemetry events"""
    timestamp: datetime = datetime.utcnow()
    event_type: str
    
class AgentRunTelemetryEvent(TelemetryEvent):
    """Event when an agent run starts"""
    event_type: str = "agent_run"
    task: str
    model_name: str
    
class AgentStepTelemetryEvent(TelemetryEvent):
    """Event when an agent step completes"""
    event_type: str = "agent_step"
    step_number: int
    action: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
class AgentEndTelemetryEvent(TelemetryEvent):
    """Event when an agent run ends"""
    event_type: str = "agent_end"
    success: bool
    step_count: int
    error: Optional[str] = None 