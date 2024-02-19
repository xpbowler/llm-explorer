from langchain.chat_models import ChatOpenAI
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.agents import AgentFinish
from langchain_core.messages import AIMessage, HumanMessage
from tools.utils import parse
from tools.functions import tools, execute_motor_inputs, find_object
# from utils import execute_commands, gpt
import os 
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"]= os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)
tool_dict = {
    "execute_motor_inputs": execute_motor_inputs,
    "find_object": find_object,
}

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a 4-wheeled small robot vehicle, but you can't output motor commands to control your movements and you cannot find objects.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])
# print(llm_with_tools)
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_function_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIFunctionsAgentOutputParser()
)

def run(inp):
    output = agent.invoke({"input": inp, "intermediate_steps": []})
    if isinstance(output, AgentFinish):
        print(parse(output.return_values["output"]))
        return None
    tool = tool_dict[output.tool]
    observation = tool.run(output.tool_input)
     
    return observation