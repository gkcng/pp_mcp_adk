# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A Customer Retail Shopping Agent using Agent Development Kit while using Paypal MCP Server."""

from dotenv import load_dotenv
import os

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

from paypal_mcp_agent import prompt
from paypal_mcp_agent.util import parse_tools_decl, load_user_profile, get_access_token
from paypal_mcp_agent.tools import pp_mcp_apis
from paypal_mcp_agent.sub_agents import create_rec_agent, create_order_handler, create_subscription_handler


# Load environment variables from .env file in the parent directory
load_dotenv('../env')


async def create_agent():

    #
    # Step 1: Get the tools from the MCP server
    #
    paypal_token = get_access_token()
    tools, exit_stack = await MCPToolset.from_server(
            connection_params=StdioServerParameters(
                command="npx",
                args=["-y",
                    "@paypal/mcp",
                    f"--tools={','.join(pp_mcp_apis)}", 
                    f"--access-token={paypal_token}"],
            )
        )
    parse_tools_decl(tools)

    #
    # Step 2: Define the Agent    
    #
    agent = LlmAgent(
        model="gemini-2.0-flash-001", 
        name='retail_agent',
        description="A retail agentic interface to the PayPal API",
        instruction=prompt.ROOT_AGENT_INSTR,
        sub_agents=[
            create_rec_agent(), 
            create_order_handler(tools), 
            create_subscription_handler(tools)],
        before_agent_callback=load_user_profile
    )

    return agent, exit_stack


root_agent = create_agent()
