from pydantic import BaseModel

class WordSchema(BaseModel):
    id: int
    word: str
    part_of_speech: str
    language_origin: str
    definition: str
    example: str
    prefixes_suffixes: str
    root_word: str
    grade_level: str
    bee_level: str
    lexical_level: str

    #model_config = {
    #    "from_attributes": True  # Pydantic v2 equivalent of orm_mode
    #}

    class Config:
        from_attributes = True  # Pydantic v2 replaces orm_mode