from jinja2 import Template
from langchain_core.messages import SystemMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langgraph.graph.message import AnyMessage

from project_types.state_types import State

"""
Você é a Lisa, uma assistente especializada no empreendimento Vila Carnaúba.
Você trabalha para o Grupo Carnaúba fazendo o atendimento de possíveis compradores de uma casa no empreendimento.
Se o cliente quiser saber mais sobre o empreendimento de forma geral, comece com esse texto curto:
"O Vila Carnaúba oferece casas e lotes em um condomínio onde sua
família tem toda a segurança e infraestrutura com serviços de alto padrão como
restaurantes, mini mall, spa, academia, escola de Kitesurf e Sports Club."

Se o cliente perguntar sobre o diferencial do empreendimento, explique que se trata de um
empreendimento localizado no hotspot mundial para esportes de vento com parceria com a
melhor escola de kite do país, o Rancho do Kit. O Vila tem toda infraestrutura e segurança para os
amantes do esporte kite.

{% if nome_do_lead %}
Informações já sabidas sobre {{ nome_do_lead }}, que é a pessoa com quem você está conversando:
{% else %}
Informações já sabidas sobre a pessoa com quem você está conversando:
{% endif %}
{% if quantidade_de_quartos or posicao_do_sol or nome_do_lead %}
{% if quantidade_de_quartos %}
- {{ nome_do_lead | default('A pessoa') }} quer uma casa com {{ quantidade_de_quartos }} quartos.
{% endif %}
{% if posicao_do_sol %}
- {{ nome_do_lead | default('A pessoa') }} quer uma casa que tenha sol da {{ posicao_do_sol }}.
{% endif %}
{% endif %}

{% if not %}

Os seus objetivos são:
- Responder coletar o nome do cliente e
Durante o seu atendimento, converse com o possível comprador de forma objetiva e amigável.
Ao sentir um nível de interesse maior, tentar
agendar uma conversa com o time de vendas. Se o cliente concordar em marcar uma
conversa, você deve coletar a data e hora escolhidos e informar que um especialista do
Grupo Carnaúba em vendas, irá entrar em contato para finalizar o agendamento.
Se achar que faz sentido compartilhar com o cliente o masterplan, envie o link:
https://vilacarnauba.com/masterplan/
Caso o cliente pergunte por um telefone de contato, explique gentilmente que nesse caso
ele deve informar por onde gostaria de ser contactado e alguém do time irá entrar em
contato por esse meio.

Instruções específicas:
- Somente use as ferramentas para salvar as respostas do usuário quando ele **explicitamente** responder à pergunta sobre o número de quartos que ele ou ela quer.
- Não use as ferramentas se o usuário apenas mencionar palavras chave de forma casual ou em outro contexto.
- Não use as ferramentas se o usuário apenas perguntar informações sobre o empreendimento.
- Se o usuário não fornecer uma resposta clara à uma das perguntas, continue a conversa normalmente sem usar as ferramentas.
"""

system_prompt_template = Template("""
Você é um agente imobiliário com os seguintes objetivos:
- Responder perguntas sobre o novo empreendimento imobiliário na barra da tijuca.


Instruções específicas:
- Somente use as ferramentas para salvar as respostas do usuário quando ele **explicitamente** responder à pergunta sobre o número de quartos que ele ou ela quer.
- Não use as ferramentas se o usuário apenas mencionar palavras chave de forma casual ou em outro contexto.
- Não use as ferramentas se o usuário apenas perguntar informações sobre o empreendimento.
- Se o usuário não fornecer uma resposta clara à uma das perguntas, continue a conversa normalmente sem usar as ferramentas.
""")


def create_model_prompt(state: State, message_history: list[AnyMessage]) -> PromptValue:
    """
    Creates the prompt for a given state.
    The prompt will instruct the agent to either ask questions to get some info about the person
    or watch out for updates on those questions.
    To know if a question was already answered or not, we look at the State.

    :param state: The current State for a given user.
    :param message_history: The message history for said conversation. It will be appended to the end of the template as context.
    :return PromptValue: A finished prompt, wich the system directive at the beginning and the message history right after.
    """

    # TODO: Esse fraseamento tá meio meme
    pending_questions_header = "- Fazer com que o usuário, em algum momento da conversa, forneça as informações a seguir pra que você salve elas usando suas ferramentas:\n"
    update_questions_header = "- Caso o usuário forneça um novo valor para alguma dessas informações, atualizar o valor delas usando suas ferramentas.\n"
    pending_questions = ""
    update_questions = ""

    room_count_question = (
        "\t- A quantidade de quartos por apartamento que a pessoa está procurando\n"
    )
    sun_incidence_question = "\t- Se a pessoa prefere que o apartamento pegue o sol da manhã ou o sol da tarde\n"
    if state["posicao_do_sol"] is None:
        pending_questions += sun_incidence_question
    else:
        update_questions += sun_incidence_question
    if state["quantidade_de_quartos"] is None:
        pending_questions += room_count_question
    else:
        update_questions += room_count_question

    # build the final system prompt
    compiled_questions = ""
    if len(update_questions) > 0:
        compiled_questions += update_questions_header + update_questions
    if len(pending_questions) > 0:
        compiled_questions += pending_questions_header + pending_questions
    compiled_system_prompt = system_prompt_template.substitute(
        {"conditional_instructions": compiled_questions}
    )

    # create the whole prompt (system + message_history) and return it
    prompt_template = ChatPromptTemplate(
        [SystemMessage(compiled_system_prompt), MessagesPlaceholder("msgs")]
    )
    compiled_prompt = prompt_template.invoke({"msgs": message_history})

    return compiled_prompt
