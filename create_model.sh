#!/usr/bin/env bash
set -e

# Ensure training data exists
if [ ! -f training_data.jsonl ]; then
  echo "training_data.jsonl not found. Run: python generate_training_data.py"
  exit 1
fi

# Merge dataset into Modelfile (simple embedding)
# We’ll inline the JSONL into the Modelfile using a placeholder replacement
# (You can use more robust templating; this keeps it simple.)
DATASET_CONTENT=$(awk '{printf "%s\\n", $0}' training_data.jsonl)

# Create a temp Modelfile with dataset injected
sed "s|{{ training_data }}|$DATASET_CONTENT|g" Modelfile > Modelfile.built

# Create the model called 'abdpain'
ollama create abdpain -f Modelfile.built

echo
echo "Model 'abdpain' created. Test it with:"
echo "  ollama run abdpain \"What are common causes of abdominal pain in adults?\""
