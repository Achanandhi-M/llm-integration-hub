from fastapi import FastAPI, Depends, HTTPException, Header, Body
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from auth_service.util import get_current_user  # Import get_current_user from auth_service

load_dotenv()

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile")  # Use your model ID
)

app = FastAPI()

@app.post("/query_model")
def query_model(
    model: str = Body(...),  # Expecting 'model' in the request body
    messages: list = Body(...),  # Expecting 'messages' in the request body
    current_user: str = Depends(get_current_user),
    authorization: str = Header(None)
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not authorization:
        raise HTTPException(status_code=400, detail="Authorization token missing")
    
    try:
        # Here we're using the 'messages' part as in your cURL example
        response = agent.print_response(messages[0]["content"])  # Assuming 'content' is passed in the messages
        
        return {
            "answer": response,
            "user": current_user
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
