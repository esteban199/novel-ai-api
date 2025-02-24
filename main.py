from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from fastapi.middleware.cors import CORSMiddleware

# Cargar variables de entorno
load_dotenv()

# Configurar logging con más detalles
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL de tu aplicación React
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los headers
)

class NovelInput(BaseModel):
    text: str

@app.post("/analyze_novel")
def analyze_novel(novel: NovelInput):
    # Agregar múltiples logs para mejor debugging
    logger.debug("Iniciando análisis de novela")
    logger.debug(f"Longitud del texto recibido: {len(novel.text)} caracteres")
    logger.debug(f"Primeros 100 caracteres del texto: {novel.text[:100]}...")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un experto en literatura y análisis de novelas."},
            {"role": "user", "content": f"Analiza esta novela y dime personajes, Plot principal, Heroes, Villanos, y cualquier otro detalle que sea relevante, cada punto separado por espacios: {novel.text}"}
        ]
    )
    
    results = response.choices[0].message.content
    logger.debug(f"Análisis completado. Resultado: {results}")
    return {"analysis": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)