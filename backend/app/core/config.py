from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Sistema de Asistencia Pasantes"
    DATABASE_URL: str = "postgresql://postgres:abmm@localhost/asistencia"
    SECRET_KEY: str = "super_secreta_clave_para_jwt_cambiar_en_produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480 

    class Config:
        env_file = ".env"

settings = Settings()