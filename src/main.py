from fastapi import FastAPI
from fhirtypepkg import main

app = FastAPI()

@app.get("/getdata")
async def get_data(endpoint: str, firstname: str, lastname: str, npi: int):
    result = main.search_practitioner(family_name=lastname, given_name=firstname, npi=npi)
    return result


@app.get("/matchdata")
async def match_data():
    return {"sample": "this is your matched data"}


@app.get("/consensusresult")
async def get_consensus_result():
    return {"sample": "this is consensusresult yeah"}