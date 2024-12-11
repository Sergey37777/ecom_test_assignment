import re
from pathlib import Path
from typing import Dict
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import logging

from pydantic import BaseModel
from tinydb import TinyDB, Query

from db import initialize_db, cleanup_db

DB_FILE = Path('./db.json')
db = TinyDB(DB_FILE)

logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Initializing database models")
    initialize_db(db=db)
    yield
    logging.info("Dropping database models")
    cleanup_db(DB_FILE)


def validate_email(value):
    return bool(re.match(r"^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,}$", value))


def validate_phone(value):
    return bool(re.match(r"^\+7 *\d{3} *\d{3} *\d{2} *\d{2}$", value))


def validate_date(value):
    return bool(re.match(r"^(\d{2}\.\d{2}\.\d{4}|\d{4}-\d{2}-\d{2})$", value))


def determine_field_type(value):
    if validate_date(value):
        return "date"
    elif validate_phone(value):
        return "phone"
    elif validate_email(value):
        return "email"
    else:
        return "text"


app = FastAPI(lifespan=lifespan)


def find_matching_template(fields: Dict[str, str]) -> str | None:
    form_templates_table = db.table("form_templates")
    templates = form_templates_table.all()
    for template in templates:
        match = True
        for field in template['fields']:
            field_name = field['field_name']
            field_type = field['field_type']
            if field_name not in fields or determine_field_type(fields[field_name]) != field_type:
                match = False
                break
        if match:
            return template['name']
    return None


class FormInput(BaseModel):
    fields: Dict[str, str]

@app.post("/get_form")
async def get_form(input_data: FormInput) -> Dict[str, str]:
    input_data = input_data.fields
    matching_template = find_matching_template(input_data)
    if matching_template:
        return {"template_name": matching_template}

    field_types = {f"f_name{idx+1}": determine_field_type(value) for idx, (_, value) in enumerate(input_data.items())}
    return field_types

