from fastapi import FastAPI, Form
from fastapi.responses import RedirectResponse, Response
import base64
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./links.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

Base = declarative_base()

class Link(Base):
    __tablename__ = "links"
 
    id = Column(Integer, primary_key=True, index=True)
    original_link = Column(String)
    short_link_dir = Column(String)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()
app = FastAPI()

@app.get("/")
def read_root():
    with open('index.html','r',encoding='utf-8') as file:
        html = file.read()
    return Response(content = html, status_code = 200,media_type='text/html')

@app.get("/{short_link_dir}/")
def read_root(short_link_dir):
    checker = db.query(Link).filter(Link.short_link_dir == short_link_dir).first()
    response = RedirectResponse(url=checker.original_link) if checker else RedirectResponse(url='/')
    return response


@app.post('/create-link/')
def add_link(original_link: str = Form()):
    domain = 'http://127.0.0.1:8000'
    checker = db.query(Link).filter(Link.original_link == original_link).first()
    if checker:
        short_link = f'{domain}/{checker.short_link_dir}'
    else:
        short_link_dir = base64.urlsafe_b64encode(bytes(original_link, 'utf-8'))[-11:-2].decode("utf-8")
        short_link = f'{domain}/{short_link_dir}'
        new_link = Link(original_link = original_link, short_link_dir = short_link_dir)
        db.add(new_link)
        db.commit()
    return Response(content = f'<center> Ваша ссылка: {short_link}</center>',media_type='text/html')
