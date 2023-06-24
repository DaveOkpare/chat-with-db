import openai
from openai_function_call import OpenAISchema
from pydantic import Field
from sqlalchemy import create_engine
import json
from sqlalchemy import inspect
from typing import Optional


class Query(OpenAISchema):
    """
    Class representing an SQL schema and a question.
    Each query should contain a syntax.
    """
    sql: Optional[str] = Field(None, description="SQL syntax to query the schema")
    python: Optional[str] = Field(None, description="Python syntax to query the schema")
    golang: Optional[str] = Field(None, description="Golang syntax to query the schema")
    javascript: Optional[str] = Field(None, description="JavaScript syntax to query the schema")
    dart: Optional[str] = Field(None, description="Dart syntax to query the schema")


def ask_ai(schema: str, prompt: str, database: str, languages: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        temperature=0.2,
        max_tokens=1000,
        functions=[Query.openai_schema],
        function_call={"name": Query.openai_schema["name"]},
        messages=[
            {
                "role": "system",
                "content": f"You are a world class algorithm to generate correct syntax to query on a given schema."
            },
            {"role": "user", "content": f"Answer request using the following context. "
                                        f"If no Languages mentioned, only generate SQL syntax."
                                        f"Do NOT return Languages not mentioned."},
            {"role": "user", "content": f"Schema: \n {schema}"},
            {"role": "user", "content": f"Request: {prompt}"},
            {"role": "user", "content": f"Database: {database}"},
            {"role": "user", "content": f"Languages: {languages}"},
        ],
    )

    # Creating an Answer object from the completion response
    return Query.from_response(completion)


def generate_schema(database_url):
    # Create the SQLAlchemy engine
    engine = create_engine(database_url)

    # Create the Inspector and reflect the database
    inspector = inspect(engine)
    schema = inspector.default_schema_name

    # Get the table names
    table_names = inspector.get_table_names(schema=schema)

    # Dictionary to store column information
    column_dict = {}

    # Iterate over the tables and populate the column dictionary
    for table_name in table_names:
        columns = inspector.get_columns(table_name, schema=schema)
        for column in columns:
            column_name = column['name']
            column_type = column['type']
            column_key = f"{schema}.{table_name}.{column_name}"
            column_dict[column_key] = str(column_type)

    # Close the database connection
    engine.dispose()

    return json.dumps(column_dict)
