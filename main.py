from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo para criar nova cidade via POST
class NovaCidade(BaseModel):
    nome: str
    uf: str

# Modelo principal Cidade (deve ser definido antes de instanciar)
class Cidade(BaseModel):
    id: int
    nome: str
    uf: str

# Lista de dicionários (exemplo bruto)
cidades_list = [
    {'id': 1, 'nome': 'Teresina', 'uf': 'PI'},
    {'id': 2, 'nome': 'Altos', 'uf': 'PI'},
    {'id': 3, 'nome': 'Coelho Neto', 'uf': 'MA'},
    {'id': 4, 'nome': 'Pedro II', 'uf': 'PI'},
]

# Lista de modelos Cidade (exemplo usando Pydantic)
cidades: List[Cidade] = [
    Cidade(id=1, nome='Teresina', uf='PI'),
    Cidade(id=2, nome='Coelho Neto', uf='MA'),
]

# Variável para controlar o próximo id
proximo_id = max(c.id for c in cidades) + 1 if cidades else 1

@app.get('/cidades')
def listar_cidades_dicts():
    return cidades_list

@app.get('/cidades2')
def listar_cidades_models():
    return cidades

@app.get('/cidades/{id}')
def cidades_detail(id: int):
    for cidade in cidades:
        if cidade.id == id:
            return cidade
    raise HTTPException(status_code=404, detail=f'Cidade não existe com id -> {id}')

@app.post('/cidades', status_code=201)
def cidades_create(nova_cidade: NovaCidade):
    global proximo_id
    cidade = Cidade(id=proximo_id, nome=nova_cidade.nome, uf=nova_cidade.uf)
    proximo_id += 1
    cidades.append(cidade)
    return cidade