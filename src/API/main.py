from fastapi import FastAPI
from pydantic import BaseModel
from src.webui.components import browser_use_agent_tab
from src.webui.components.browser_use_agent_tab import run_agent_task
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os


app = FastAPI()


# Mount the videos folder
app.mount("/videos", StaticFiles(directory="outputdata/videos"), name="videos")
app.mount("/static", StaticFiles(directory=os.getcwd()), name="static")



class AgentRequest(BaseModel):
    query: str
    url: str

@app.post("/run-agent")
async def run_agent(request: AgentRequest):
    try:
        result = await run_agent_task(request.query, request.url)
        #print("🧪 Raw result from run_agent_task:", result)
        # logger.info(f"🧪 Raw result from run_agent_task: {result}")
        #print("In main.py ",result["final_result"])
        return {
            "status": "success",
            "task_id": result["task_id"],
            "final_result": result["final_result"],
            "videos": result["videos"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/stop-agent")
def stop_agent():
    # call stop_wrapper or shutdown browser/session
    return {"status": "stopped"}

# @app.post("/run-agent")
# async def run_agent(request: AgentRequest):
#     try:
#         result = await run_agent_task(request.query, request.url)
#         print("TYPE OF RESULT:", type(result))
#         print("DIR OF RESULT:", dir(result))
      

#         return {
#             "status": "success",
#             "task_id": result["task_id"],
#             "final_result": result["final_result"],
#             #"final_result": result.final_result,
#             # "output_dir": result["output_dir"],
#             # "screenshots": len(result["screenshot_paths"]),
#             #"responses": len(result["response_paths"]),          #no need
#             #"steps": result["step_count"] 
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# Serve index.html at /
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")



