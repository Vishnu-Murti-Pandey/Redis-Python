from fastapi import FastAPI
from pydantic import BaseModel

from queue_config import email_queue
from tasks import send_email

app = FastAPI()

class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str


@app.post("/send-email")
def queue_email(request: EmailRequest):
    job = email_queue.enqueue(
        send_email,
        request.email,
        request.subject,
        request.body
    )

    return {
        "message": "Email queued",
        "job_id": job.id,
        "status": job.get_status()
    }