from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template = ChatPromptTemplate(
    [("system", "You are a helpful assistant"), MessagesPlaceholder("msgs")]
)

prompt_template = ChatPromptTemplate(
    [
        (
            "system",
            "You are a real estate agent trying to sell a new condo on a neighbourhood called 'Barra Da Tijuca'. The cost of a house is 10.000 USD, but you can go as lower as 7.000 USD. Try your best to negotiate the value with the person.",
        ),
        MessagesPlaceholder("msgs"),
    ]
)
