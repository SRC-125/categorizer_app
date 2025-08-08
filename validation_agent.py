# import os
# import json
# import time

# from config import llm

# # === Constants ===
# METADATA_PATH = "metadata.json"
# VALIDATION_FILE = "validation_results.json"
# MAX_RETRIES = 3
# RETRY_DELAY = 2  # seconds

# # === Tool 1: Confidence Estimation ===
# def estimate_confidence_score_tool(field_name: str, field_value: str, case_text: str) -> float:
#     prompt = f"""
#     You are a confidence evaluator.
#     Evaluate how well the following value fits the field based on the case study:
#     - Field: {field_name}
#     - Value: {field_value}
#     Case Study Text:
#     {case_text[:3000]}
#     Output a number between 0 and 1 (e.g., 0.85). No explanation.
#     """

#     for attempt in range(MAX_RETRIES):
#         try:
#             result = llm.invoke([
#                 {"role": "system", "content": "Return only the confidence score as a float."},
#                 {"role": "user", "content": prompt}
#             ])
#             return float(result.content.strip())
#         except Exception as e:
#             print(f"[Retry {attempt+1}] Failed to get score for {field_name}: {e}")
#             time.sleep(RETRY_DELAY)
#     return 0.0  # fallback score if all retries fail

# # === Tool 2: Metadata Reader ===
# def read_metadata(metadata_path: str) -> dict:
#     if not os.path.exists(metadata_path):
#         print(f"⚠️ Metadata file '{metadata_path}' not found.")
#         return {}
    
#     try:
#         with open(metadata_path, "r") as f:
#             return json.load(f)
#     except Exception as e:
#         print(f"❌ Error reading metadata: {e}")
#         return {}

# # === Tool 3: Save Validation Results ===
# def write_validation_results(results: dict, output_path: str):
#     try:
#         with open(output_path, "w") as f:
#             json.dump(results, f, indent=2)
#         print(f"✅ Validation results written to: {output_path}")
#     except Exception as e:
#         print(f"❌ Failed to write validation results: {e}")

# # === Self-Healing Agent ===
# def agent_run_validation(metadata_path: str, output_path: str) -> dict:
#     metadata = read_metadata(metadata_path)
#     if not metadata:
#         print("❌ No metadata found. Skipping validation.")
#         return {}

#     validation_results = {}

#     for file_name, data in metadata.items():
#         try:
#             case_text = data.get("summary", "")
#             validation_results[file_name] = {}

#             for field in ["category", "domain", "technology_used"]:
#                 field_value = data.get(field, "")
#                 if not field_value:
#                     print(f"⚠️ Missing value for '{field}' in file: {file_name}")
#                     confidence = 0.0
#                 else:
#                     confidence = estimate_confidence_score_tool(field, field_value, case_text)
                
#                 validation_results[file_name][field] = {
#                     "value": field_value,
#                     "confidence": round(confidence, 4)
#                 }
#         except Exception as e:
#             print(f"❌ Failed to process file '{file_name}': {e}")
#             continue  # skip to next file

#     write_validation_results(validation_results, output_path)
#     return validation_results

# # # === Run the Agent ===


# # # validation metadata
# # VALIDATION_FILE = "validation_results.json"

# # # Tool 1: Agent to Estimate Confidence Score
# # def estimate_confidence_score_tool(field_name: str, field_value: str, case_text: str) -> float:
# #     """
# #     Tool to calculate the confidence score for a field based on case study.
# #     This is a modular tool invoked by the agent.
# #     """
# #     prompt = f"""
# #     You are a confidence evaluator.
# #     Evaluate how well the following value fits the field based on the case study:
# #     - Field: {field_name}
# #     - Value: {field_value}
# #     Case Study Text:
# #     {case_text[:3000]}
# #     Output a number between 0 and 1 (e.g., 0.85). No explanation.
# #     """
# #     try:
# #         result = llm.invoke([  # This is the tool invocation to estimate the confidence score
# #             {"role": "system", "content": "Return only the confidence score as a float."},
# #             {"role": "user", "content": prompt}
# #         ])
# #         return float(result.content.strip())
# #     except Exception as e:
# #         print(f"Error invoking tool for confidence score: {e}")
# #         return 0.0  # Default to 0.0 in case of any failure

# # # Tool 2: Reading Metadata
# # def read_metadata(metadata_path: str) -> dict:
# #     """
# #     Tool to read metadata from a given file path. It is a modular action.
# #     """
# #     if not os.path.exists(metadata_path):
# #         raise FileNotFoundError(f"{metadata_path} not found!")
    
# #     with open(metadata_path, "r") as f:
# #         metadata = json.load(f)
# #     return metadata

# # # Tool 3: Writing Validation Results
# # def write_validation_results(validation_results: dict, output_path: str):
# #     """
# #     Tool to write validation results to a JSON file.
# #     """
# #     with open(output_path, "w") as f:
# #         json.dump(validation_results, f, indent=2)
# #     print(f"Validation results written to {output_path}")

# # # Agent to Run the Full Validation Process
# # def agent_run_validation(metadata_path: str, output_path: str) -> dict:
# #     """
# #     Agent that orchestrates the validation process using various tools.
# #     """
# #     # Step 1: Read metadata (Tool 2)
# #     metadata = read_metadata(metadata_path)
    
# #     # Step 2: Initialize validation results
# #     validation_results = {}
    
# #     # Step 3: Iterate over metadata and apply tools to estimate confidence
# #     for file_name, data in metadata.items():
# #         case_text = data.get("summary", "")
# #         validation_results[file_name] = {}
        
# #         # Use Tool 1 (Confidence Score Estimation) for each field
# #         for field in ["category", "domain", "technology_used"]:
# #             field_value = data.get(field, "")
# #             score = estimate_confidence_score_tool(field, field_value, case_text)
# #             validation_results[file_name][field] = {
# #                 "value": field_value,
# #                 "confidence": round(score, 4)
# #             }
    
# #     # Step 4: Write the validation results to file (Tool 3)
# #     write_validation_results(validation_results, output_path)
    
# #     return validation_results


# # # Example usage of the agent
# # metadata_path = "metadata.json"
# # output_path = "validation_results.json"
# # validation_results = agent_run_validation(metadata_path, output_path)
# # print(validation_results)

# # agent_run_validation(metadata_path=METADATA_FILE, output_path=VALIDATION_FILE)
import os
import json
import time

from config import llm  # Make sure llm is defined in config.py

# === Constants ===
METADATA_PATH = "metadata.json"
VALIDATION_FILE = "validation_results.json"
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds


# === Tool 1: Confidence Estimation with Robust Prompt ===
def estimate_confidence_score_tool(field_name: str, field_value: str, case_text: str) -> float:
    prompt = f"""
You are a confidence evaluator. Your job is to assess how accurately the field value matches the case study content.

Field: {field_name}
Value: {field_value}

Case Study Content:
{case_text[:3000]}

Instructions:
- If the field value is explicitly mentioned or clearly supported, give a high score (0.8 to 1.0).
- If it's implied but not exact, give a moderate score (0.4 to 0.7).
- If it's missing, vague, or unrelated, give a low score (0.0 to 0.3).
- Be conservative in your judgment.
- Do NOT output anything except a float number between 0 and 1.

Output:
"""

    for attempt in range(MAX_RETRIES):
        try:
            result = llm.invoke([
                {"role": "system", "content": "Return only the confidence score as a float between 0 and 1."},
                {"role": "user", "content": prompt}
            ])
            score = float(result.content.strip())

            # Avoid constant 1.0 bias unless very confident
            if score == 1.0:
                score = 0.99

            return round(score, 4)

        except Exception as e:
            print(f"[Retry {attempt+1}] Error scoring '{field_name}': {e}")
            time.sleep(RETRY_DELAY)

    return 0.0  # fallback score on failure


# === Tool 2: Read Metadata ===
def read_metadata(metadata_path: str) -> dict:
    if not os.path.exists(metadata_path):
        print(f"⚠️ Metadata file '{metadata_path}' not found.")
        return {}

    try:
        with open(metadata_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error reading metadata: {e}")
        return {}


# === Tool 3: Write Validation Results ===
def write_validation_results(results: dict, output_path: str):
    try:
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✅ Validation results saved to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to write validation results: {e}")


# === Self-Healing Validation Agent ===
def agent_run_validation(metadata_path: str, output_path: str) -> dict:
    metadata = read_metadata(metadata_path)
    if not metadata:
        print("❌ No metadata found. Skipping validation.")
        return {}

    validation_results = {}

    for file_name, data in metadata.items():
        try:
            case_text = data.get("summary", "")
            validation_results[file_name] = {}

            for field in ["category", "domain", "technology_used"]:
                field_value = data.get(field, "")
                if not field_value:
                    print(f"⚠️ Missing value for '{field}' in file: {file_name}")
                    confidence = 0.0
                else:
                    confidence = estimate_confidence_score_tool(field, field_value, case_text)

                validation_results[file_name][field] = {
                    "value": field_value,
                    "confidence": confidence
                }

        except Exception as e:
            print(f"❌ Error processing file '{file_name}': {e}")
            continue

    write_validation_results(validation_results, output_path)
    return validation_results


