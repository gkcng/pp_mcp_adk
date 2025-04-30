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


"""Define the simple subagents of the Paypal Retail Agent"""

from google.genai import types

from google.adk.agents.llm_agent import LlmAgent
from google.adk.tools.mcp_tool import MCPTool
from google.adk.tools.agent_tool import AgentTool

from paypal_mcp_agent import prompt
from paypal_mcp_agent.tools import product_search, subscription_apis, orders_apis

# shopper_profile=LlmAgent(
#    name="external_shopper_profile"
# )

def create_rec_agent():
    return LlmAgent(
        model="gemini-2.0-flash-001", 
        name='recommendation_agent',
        description="Make product suggestions base on an understanding of desires from text or images",
        instruction=prompt.RECOMMENDATIOIN_INSTR,
        tools=[product_search], # AgentTool(agent=shopper_profile)
        generate_content_config=types.GenerateContentConfig(temperature=0.3),        
    )

def create_subscription_handler(tools: list[MCPTool]):
    return LlmAgent(
        model="gemini-2.0-flash-001", 
        name='subscription_handler',
        description="Helps customers with their product subscriptions via the PayPal API",
        tools=[t for t in tools if t.mcp_tool.name in subscription_apis],
        generate_content_config=types.GenerateContentConfig(temperature=0.3),        
    )

def create_order_handler(tools: list[MCPTool]):
    return LlmAgent(
        model="gemini-2.0-flash-001", 
        name='orders_handler',
        description="Helps customers with their product orders and shipments via the PayPal API",
        instruction=prompt.ORDERS_INSTR,
        tools=[t for t in tools if t.mcp_tool.name in orders_apis],
        generate_content_config=types.GenerateContentConfig(temperature=0.3),        
    )   
