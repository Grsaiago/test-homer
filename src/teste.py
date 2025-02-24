from db.models import Temperaturadolead
from project_types.state_types import State
from prompt import system_prompt_template

state: State = {
    "messages": [],
    "nome_do_lead": "Gabriel",
    "quantidade_de_quartos": 4,
    "orcamento": 10000,
    "bairro": None,
    "temperatura_do_lead": Temperaturadolead.QUENTE,
    "data_e_hora_da_chamada": None,
}

print(system_prompt_template.render(state))
