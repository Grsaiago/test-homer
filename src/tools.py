from langchain_core.tools import tool


@tool
def atualizar_quartos(quantidade_de_quartos: int) -> str:
    """Atualiza a informação de quantos quartos o usuário vai querer no apto que ele ou ela está procurando"""

    print(f"A quantidade de quartos que o usuário quer é: {quantidade_de_quartos}")
    return "A quantidade de quartos para este usuário foi alterada com sucesso"
