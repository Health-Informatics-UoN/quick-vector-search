from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str ="postgres"
    db_password: str ="password"
    db_name: str ="omop"
    db_schema: str ="cdm"
    db_vectable: str ="embeddings"
    
    embeddings_model: str = "BAAI/bge-small-en-v1.5"

    def db_uri(self):
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
