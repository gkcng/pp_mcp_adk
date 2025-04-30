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

"""Functions implementation and lists for MCP tools selection."""

import base64

from google.genai import types

from google.adk.tools.tool_context import ToolContext


def image_to_base64(image_path):
    """
    Loads an image from the given path and encodes it to Base64.

    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The Base64 encoded string of the image, or None if an error occurs.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            return encoded_string.decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return None
    except Exception as e:
         print(f"An error occurred: {e}")
         return None


async def product_search(product_characteristics: str, tool_context: ToolContext):
    """Returns a few product recommendation base on desirable product characteristics. 
    Args:
        product_characteristics - a detailed description of desirable product characteristics. 

    Respnose:
        A list of matched items containing item's name, cost, and currency.
    """
    # tool_context.actions.skip_summarization = True    
    tool_context.save_artifact(filename="recommendation_1", artifact=
                               types.Part(inline_data=types.Blob(data=image_to_base64("paypal_mcp_agent/images/dress1.png"), mime_type="image/png")))
    tool_context.save_artifact(filename="recommendation_2", artifact=
                               types.Part(inline_data=types.Blob(data=image_to_base64("paypal_mcp_agent/images/dress4.png"), mime_type="image/png")))
    tool_context.save_artifact(filename="recommendation_3", artifact=
                               types.Part(inline_data=types.Blob(data=image_to_base64("paypal_mcp_agent/images/dress3.png"), mime_type="image/png")))
    return {"result": [
            {
                "currencyCode": "USD",
                "itemCost": 250,
                "name": "Floral Fit-and-Flare Summer Dress",
            },
            {
                "currencyCode": "USD",
                "itemCost": 220,
                "name": "Floral Mermaid Summer Dress ",
            },
            {
                "currencyCode": "USD",
                "itemCost": 150,
                "name": "Cherry Blossom Florals Summer Dress",
            },                
        ]
    }

pp_mcp_apis=[
  'orders.create',
  'orders.get',
  'orders.capture',
  'shipment.create',
  'shipment.get',  
  'subscriptions.create',
  'subscriptions.show',
  'subscriptions.cancel'
]


subscription_apis=[
    "create_subscription", 
    "show_subscription_details", 
    "cancel_subscription"
]


orders_apis=[
    "create_order", 
    "get_order", 
    "capture_order", 
    "create_shipment", 
    "get_shipment_tracking"
]
