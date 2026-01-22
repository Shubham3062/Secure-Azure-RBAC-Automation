import json
import os
import sys
from datetime import datetime

APPROVED_FOLDER = "access-requests/approved/"
ROLE_CATALOG_FILE = "role-catalog/roles.json"
POLICY_FILE = "policies/access-policy.json"

# Load role catalog
with open(ROLE_CATALOG_FILE) as f:
    roles = json.load(f)

# Load policy rules
with open(POLICY_FILE) as f:
    policies = json.load(f)

def validate_request(file_path):
    with open(file_path) as f:
        req = json.load(f)

    errors = []

    # Extract relevant fields
    role_key = req["access"]["role_key"]
    environment = req["access"]["environment"]
    duration = req["access"]["duration_days"]
    employee_type = req["requester"]["employee_type"]
    justification = req.get("justification", "")

    # Check role exists
    if role_key not in roles:
        errors.append(f"Role key '{role_key}' does not exist in role catalog.")

    # Employee type checking
    allowed_roles = policies["employee_type_rules"].get(employee_type, {}).get("allowed_roles", [])
    if role_key not in allowed_roles:
        errors.append(f"Employee type '{employee_type}' cannot request role '{role_key}'.")

    # Duration limit
    max_duration = policies["employee_type_rules"].get(employee_type, {}).get("max_duration_days", 0)
    if duration > max_duration:
        errors.append(f"Duration {duration} exceeds max allowed {max_duration} days for '{employee_type}'.")

    # Environment checking
    allowed_env_roles = policies["environment_rules"].get(environment, {}).get("allowed_roles", [])
    if role_key not in allowed_env_roles:
        errors.append(f"Role '{role_key}' not allowed in environment '{environment}'.")

    # Justification required
    if policies.get("justification_required", True) and not justification.strip():
        errors.append("Justification is required but missing.")

    # Output
    if errors:
        print(f"Validation failed for {file_path}:")
        for e in errors:
            print(f"   - {e}")
        return False
    else:
        print(f"Validation passed for {file_path}")
        return True

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else APPROVED_FOLDER
    all_passed = True
    for filename in os.listdir(folder):
        if filename.endswith(".json"):
            path = os.path.join(folder, filename)
            if not validate_request(path):
                all_passed = False

    if not all_passed:
        sys.exit(1) 
