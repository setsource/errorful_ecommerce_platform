#!/bin/bash

echo "Paste your folder structure below (Ctrl+D to end input):"

# Read multiline input
input=$(</dev/stdin)

# Remove box drawing characters and comments
clean_input=$(echo "$input" | sed -E 's/[├└│─]+//g' | sed 's/#.*//')

# Get root folder
root_dir=""
while IFS= read -r line; do
  trimmed=$(echo "$line" | sed 's/^[ \t]*//;s/[ \t]*$//')
  [[ -n "$trimmed" ]] && root_dir="$trimmed" && break
done <<< "$clean_input"

# Normalize root
root_dir="${root_dir%/}"
echo "Root directory detected: $root_dir"

# Create root dir
mkdir -p "$root_dir"
declare -a path_stack=("$root_dir")
declare -A created_dirs=()
created_dirs["$root_dir"]=1

# Process lines
while IFS= read -r raw_line; do
  # Clean line
  stripped=$(echo "$raw_line" | sed -E 's/[├└│─]+//g' | sed 's/#.*//' | sed 's/^[ \t]*//;s/[ \t]*$//')
  [[ -z "$stripped" ]] && continue

  # Calculate indent level (assume 4-space or tab indent)
  indent=$(echo "$raw_line" | grep -o '^[[:space:]]*' | wc -c)
  level=$((indent / 4))

  # Trim path_stack to current level
  path_stack=("${path_stack[@]:0:$((level + 1))}")
  path_stack[$((level + 1))]="$stripped"

  # Build full path
  full_path=$(IFS=/ ; echo "${path_stack[*]}")
  full_path=$(echo "$full_path" | sed 's|//*|/|g')

  # Heuristic: if next line is indented more, it's a directory; otherwise file
  peek_next=$(echo "$clean_input" | grep -A1 "$raw_line" | tail -n1)
  next_indent=$(echo "$peek_next" | grep -o '^[[:space:]]*' | wc -c)
  is_dir=false
  if (( next_indent > indent )); then
    is_dir=true
  elif [[ "$stripped" == */ ]]; then
    is_dir=true
  fi

  # Create file or directory
  if $is_dir; then
    mkdir -p "$full_path"
    echo "Created directory: $full_path"
    created_dirs["$full_path"]=1
  else
    dir_path=$(dirname "$full_path")
    mkdir -p "$dir_path"
    created_dirs["$dir_path"]=1
    touch "$full_path"
    echo "Created file: $full_path"
  fi
done <<< "$clean_input"

# Add .gitkeep to empty directories
for dir in "${!created_dirs[@]}"; do
  if [ -d "$dir" ] && [ -z "$(ls -A "$dir")" ]; then
    touch "$dir/.gitkeep"
    echo "Added .gitkeep to empty directory: $dir"
  fi
done

echo "✅ Folder structure with .gitkeep created successfully."

