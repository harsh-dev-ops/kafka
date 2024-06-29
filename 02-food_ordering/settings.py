from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ORDER_KAFKA_TOPIC:str
    ORDER_CONFIRMED_KAFKA_TOPIC:str
    KAFKA_BROKER:str
    
    class Config:
        env_file = './.env'
        
settings = Settings()