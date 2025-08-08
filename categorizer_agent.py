
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from config import llm


def calculate_confidence(output: str, task: str, valid_domains=None) -> float:
    """
    Calculates a confidence score based on output.
    Returns a score between 0 (low confidence) and 1 (high confidence).
    """
    confidence = 0.5  # Default baseline confidence

    # Score based on length of the response (more detailed = more confident)
    if len(output) > 100:
        confidence += 0.2  # Increase confidence for longer responses

    # Task-specific checks for categorization
    if task == 'categorization' and valid_domains:
        if output.strip() in valid_domains:
            confidence += 0.3  # Increase confidence if the category is recognized
        else:
            confidence -= 0.2  # Decrease if not in the list of valid categories

    return min(max(confidence, 0), 1)  # Ensure confidence is between 0 and 1


@tool
def categorize(summary: str, existing_categories: str) -> str:
    """
    Assigns the summary to one of the provided existing categories.
    Output only the category name from the existing list.
    """
    categories = existing_categories.split(",") if existing_categories else []
    cat_str = ", ".join(categories)

    prompt = (
        f"Available categories: {cat_str}\n\n"
        "Read the case study summary below and output ONLY the most suitable category name from the existing list.\n"
        "- Be brief (1–2 words)\n"
        "- Match exactly one category from the list\n"
        "- Do NOT create new categories\n"
        "**IMPORTANT: Output only the category name — no project titles, no description, no explanation, no client name, no sentence, and no multi-line output.**\n\n"
        "Case Study Summary:\n"
        f"{summary}"
    )

    output = llm.invoke([
        {"role": "system", "content": "You are an expert case study categorizer."},
        {"role": "user", "content": prompt}
    ])
    return output.content.strip()


tools = [categorize]

valid_categories = [
    "Digital Transformation",
    "Data Migration",
    "Data Governance",
    "Data Quality",
    "Data Security",
    "Data Analytics", 
    "Data Integration",
    "Master Data Management",
]
# from some_module import AgentExecutor, valid_categories, calculate_confidence  # Adjust imports accordingly

def run_categorization_agent(summary: str, existing_categories: list = None) -> dict:
    """
    Categorize the summary and return category and confidence score.
    """
    existing_categories = existing_categories or valid_categories  # Use default valid categories if not provided

    # Create a string of existing categories (for possible use in the agent or for categorization logic)
    existing_categories_str = ", ".join(existing_categories)

    # Get categorization result using AgentExecutor (or similar logic)
    categorization_result = AgentExecutor.invoke({
        "text": summary,
        "existing_categories": existing_categories_str
    })

    # Extract the category from the result (adjust as needed based on the output of AgentExecutor)
    category = categorization_result.get("output", "Unknown")  # Assuming 'output' contains the categorized result

    # Calculate confidence score for the categorization (adjust the calculation as needed)
    category_confidence = calculate_confidence(category, "categorization", valid_categories)

    # Return category and confidence score
    return {
        "category": category,
        "category_confidence": category_confidence  # Return the confidence score
    }

# Helper function (you can adjust this based on your requirements)
def calculate_confidence(category: str, task: str, valid_categories: list) -> float:
    """
    Simple confidence score calculation. You can improve this by using a model or a more complex algorithm.
    """
    if category in valid_categories:
        # Example: If the category is valid, return a high confidence score (e.g., 0.9).
        return 0.9
    else:
        # Otherwise, return a low confidence score (e.g., 0.6).
        return 0.6

# def run_categorization_agent(summary):
#     """
#     Categorize the case study and return category and domain along with confidence scores.
#     """
#     # Placeholder for actual categorization logic
#     category = "Sample Category"  # Replace with actual category extraction logic
#     domain = "Sample Domain"  # Replace with actual domain extraction logic

#     # Confidence scores, which should be calculated in your logic
#     category_confidence = 0.85  # Set appropriate confidence logic here
#     domain_confidence = 0.90  # Set appropriate confidence logic here

#     return {
#         "category": category,
#         "domain": domain,
#         "category_confidence": category_confidence,
#         "domain_confidence": domain_confidence,
#     }



# def run_categorization_agent(summary: str, existing_categories: list = None) -> dict:
#     existing_categories = existing_categories or valid_categories
    
#     existing_categories_str = ", ".join(existing_categories)

#     # Get categorization result
#     category = AgentExecutor.invoke({
#         "text": summary,
#         "existing_categories": existing_categories_str
#     })["output"]

    # Calculate confidence score for categorization
    # category_confidence = calculate_confidence(category, 'categorization', valid_categories)

    # return {
    #     "category": category,
    #     "confidence_score": category_confidence
    # }
