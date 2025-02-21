from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompt_values import PromptValue
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langgraph.graph.message import AnyMessage
import string

from project_types.state_types import State

system_prompt_template = string.Template("""
Você é um agente imobiliário com os seguintes objetivos:
- Responder perguntas sobre o novo empreendimento imobiliário na barra da tijuca.
${conditional_instructions}

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

    print("O VALOR DE STATE É: ", state)

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
