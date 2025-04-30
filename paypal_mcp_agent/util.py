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

"""Utilities such as MCP declaration cleansing, and ADK initial state callback."""

import json
import os
import requests

from google.adk.agents.callback_context import CallbackContext

# 
# KNOWN ISSUE 2025/04/29: 
# 
# MCP Schema requires post-processing to function with Gemini.
# - Removed any_of by promoting its first type to be a definitive parameter type.
# - Removed other anxillary items like { "type": "null" } and { "not": {} }
# 
def schema_cleansing(schema: dict):
    if 'additionalProperties' in schema:
        schema.pop('additionalProperties', None)
    if "$schema" in schema:
        schema.pop("$schema", None)
    if "type" in schema:
        match schema["type"]:
            case "object":
                elements = list(schema["properties"].items())
                for name, decl in elements:
                    if name == "transaction_id" and "anyOf" in schema["properties"][name]: 
                        schema["properties"][name].pop("anyOf", None)
                        schema["properties"][name].update({ "type": "string" })
                    if name == "notes":
                        schema["properties"][name] = { "type": "string" }
                    elif name == "shippingAddress":
                        anylist = schema["properties"]["shippingAddress"]["anyOf"]
                        schema["properties"]["shippingAddress"] = anylist[0]
                    elif schema_cleansing(decl):
                        schema["properties"].pop(name, None)
            case "array":
                schema_cleansing(schema["items"])
            case "null":
                return True
    elif "anyOf" in schema:
        elements = list(schema["anyOf"])
        for element in elements:
            if schema_cleansing(element):
                schema["anyOf"].remove(element)
        if "default" in schema:
            schema.pop("default", None)
        if "description" in schema:
            schema.pop("description", None)            
    elif "not" in schema:
        return True
    return False


def parse_tools_decl(tools: list):
    for tool in tools:
        print( tool.mcp_tool.name )
        decl = tool.mcp_tool.inputSchema
        # print("BEFORE", decl)
        schema_cleansing(decl)
        # if tool.mcp_tool.name in ["accept_dispute_claim", "get_dispute", "list_disputes" ]:
        print("AFTER", tool.mcp_tool.inputSchema)   
    return tools 


def get_access_token():
    base_url = "https://api-m.sandbox.paypal.com"
    token_url = f"{base_url}/v1/oauth2/token"
    try:
        client_id = os.getenv("PAYPAL_CLIENT_ID")
        secret = os.getenv("PAYPAL_SECRET")        
        response = requests.post(
            token_url,
            headers={"Accept": "application/json"},
            data={"grant_type": "client_credentials"},
            auth=(client_id, secret)
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Failed to obtain access token from PayPal") from e
        
    print("PayPal Response Headers: %s", json.dumps(dict(response.headers), indent=2))

    token_data = response.json()
    if "access_token" not in token_data:
        raise ValueError("Access token not found in PayPal response")

    expires = int(token_data["expires_in"]) / 3600
    print(f"\nToken expires in {expires:.2f} hours.\n")

    return token_data["access_token"]
    

def load_user_profile(callback_context: CallbackContext):
    if "user_profile" not in callback_context.state:
        callback_context.state["user_profile"] = {
                "patterns": "floral",
                "colors": ["pastel", "light", "understateed"],
                "sizes": {
                    "top": "12/L",
                    "dress": "12/L",
                    "bottom": "14/L"
                }
            }
    if "orders" not in callback_context.state:        
        callback_context.state["orders"] = [ # Change to adapt to your PayPal sandbox
                {
                    "order_id": "2RH052419P314283P", 
                    "item_name": "Dido Dog Toy",
                },
                # {   
                #     "order_id": "2T655979VB686215G",
                #     "item_name": "Floral Mermaid Summer Dress"
                # }
            ]
