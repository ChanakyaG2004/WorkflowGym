from pydantic import BaseModel, ConfigDict


class ScenarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    scenario_key: str
    customer_name: str
    month: str
    prompt: str
    required_tools: list[str]
