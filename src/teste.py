from project_types.state_types import State
from prompt import system_prompt_template

state = State(
    messages=[],
    nome_do_lead=None,
    quantidade_de_quartos=None,
    com_suite=None,
    orcamento=10000,
    meio_de_contato="grsaiago@gmail.com",
)

print(system_prompt_template.render(state))
