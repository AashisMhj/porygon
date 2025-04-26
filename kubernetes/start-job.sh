#!/bin/bash

# Define your job settings as an array of "url_index parallelism"
job=(
  "1 0"
  "3 0"
  "5 0"
  "7 0"
  "1 1"
  "3 1"
  "5 1"
  "7 1"
  "1 2"
  "3 2"
  "5 2"
  "7 2"
  "1 3"
  "3 3"
  "5 3"
  "7 3"
  "1 4"
  "3 4"
  "5 4"
  "7 4"
  "1 5"
  "3 5"
  "5 5"
  "7 5"
  "1 6"
  "3 6"
  "5 6"
  "7 6"
)

# Loop through each job config
for job in "${jobs[@]}"; do
  # Split into URL_INDEX and PARALLELISM
  set -- $job
  URL_INDEX=$2
  PARALLELISM=$1

  echo "Running job with URL_INDEX=$URL_INDEX and PARALLELISM=$PARALLELISM"

  # Replace placeholders and apply the job
  cat job.yaml \
    | sed "s/{{URL_INDEX}}/$URL_INDEX/g" \
    | sed "s/{{PARALLELISM}}/$PARALLELISM/g" | kubectl apply -f -

  # Wait 10 seconds
  echo "Waiting 5 minutes..."
  sleep 300

  # Delete the job
  echo "Deleting job..."
  kubectl delete job porygon-request-job

  # Wait a little before starting next job (optional)
  sleep 10
done
