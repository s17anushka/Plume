import azure.functions as func
import json
from agent.orchestrator import PlumeAgent

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

agent = PlumeAgent()

# ==========================
# CORS PREFLIGHT (OPTIONS)
# ==========================
@app.route(route="chat", methods=["OPTIONS"])
def options(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        "",
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )


# ==========================
# MAIN CHAT ENDPOINT
# ==========================
@app.route(route="chat", methods=["POST"])
def chat(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_json()

        session_id = body.get("sessionId", "default")
        user_message = body.get("message", "").strip()

        if not user_message:
            return func.HttpResponse(
                json.dumps({"error": "No message provided"}),
                status_code=400,
                mimetype="application/json",
                headers={"Access-Control-Allow-Origin": "*"}
            )

        # Call agent
        result = agent.handle_message(session_id, user_message)

        response_payload = {
            "response": result.get("response"),
            "metadata": {
                "intent": result.get("intent"),
                "crisisScore": result.get("crisisScore"),
                "trend": result.get("trend"),
                "escalationLevel": result.get("escalationLevel"),
                "safeMode": result.get("safeMode")
            }
        }

        return func.HttpResponse(
            json.dumps(response_payload),
            status_code=200,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )

    except Exception as e:
        # Return readable backend error
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "type": type(e).__name__
            }),
            status_code=500,
            mimetype="application/json",
            headers={"Access-Control-Allow-Origin": "*"}
        )