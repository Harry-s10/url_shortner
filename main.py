from datetime import datetime

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import models
from authentication import get_current_active_user
from database import engine, get_db
from repository.url_util import absolute_url, create_short_url, extend_url_expiry, get_url_access_logs, get_url_record, \
    log_url_access
from routers import login, register, users
from schemas import URLAccessLog, URLAnalytics, URLBase, URLCreate, User

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(login.router)
app.include_router(register.router)


@app.post("/shorten-url", response_model=URLCreate)
def shorten_url(request: URLBase, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_active_user)):
    url_record = create_short_url(request.long_url, db)
    url_record.short_url = f"http://localhost:8000/{url_record.short_url}"
    return url_record


@app.get("/{short_code}")
def redirect_to_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    url_record = get_url_record(short_code, db)
    if url_record is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Didn't find URL for {short_code} code"
        )
    if url_record.expiry and url_record.expiry < datetime.utcnow():
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="URL is expired"
        )
    ip_address = request.client.host
    user_agent = request.headers.get('User-Agent')
    log_url_access(db, url_record.id, ip_address, user_agent)
    return RedirectResponse(url=absolute_url(url_record.long_url))


@app.put("/extend-url/{short_code}", status_code=status.HTTP_202_ACCEPTED)
def extend_expiry(short_code: str, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_active_user)):
    return extend_url_expiry(short_code, db)


@app.get("/analytics/{short_code}", response_model=URLAnalytics)
def get_url_analytics(short_code: str, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
    url_record = get_url_record(short_code, db)
    if url_record is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Didn't find URL for {short_code} code"
        )
    access_logs = get_url_access_logs(db, url_record.id)
    return URLAnalytics(
            id=url_record.id,
            long_url=url_record.long_url,
            short_url=url_record.short_url,
            expiry=url_record.expiry,
            click_count=len(access_logs),
            logs=[
                URLAccessLog(
                        id=log.id,
                        access_time=log.access_time,
                        ip_address=log.ip_address,
                        user_agent=log.user_agent
                )
                for log in access_logs
            ]
    )


if __name__ == '__main__':
    uvicorn.run(app)
