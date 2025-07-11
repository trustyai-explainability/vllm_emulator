# vLLM Emulator

Emulates a vLLM-served LLM, providing mock `/v1/completions` and `/v1/chat/completions` endpoints

## Run locally

```bash
pip3 install -r requirements.txt
fastapi dev vllm_emulator.py
```

then you can curl the "model" as if it were an LLM, e.g.,:

```bash
curl --request POST \
  --url http://localhost:8000/v1/chat/completions \
  --header 'Content-Type: application/json' \
  --data '{
  "model": "vllm-runtime-cpu-fp16",
  "messages": [
    {
      "role": "user",
      "content": "What is the opposite of down?"
    }
  ],
  "temperature": 0,
  "logprobs": true,
  "max_tokens": 500
}'
```

For the `model` argument, any string is accepted by the endpoint.

## OpenShift Usage

```bash
oc apply -f deployment.yaml
```

This creates a service and route that can be used inside lm-eval, e.g.:

```yaml
apiVersion: trustyai.opendatahub.io/v1alpha1
kind: LMEvalJob
metadata:
  name: evaljob
spec:
  model: local-completions
  taskList:
    taskNames:
      - arc_easy
  logSamples: true
  batchSize: "1"
  allowOnline: true
  allowCodeExecution: false
  outputs:
    pvcManaged:
      size: 5Gi
  modelArgs:
    - name: model
      value: emulatedModel
    - name: base_url
      value: http://vllm-emulator-service:8000/v1/completions
    - name: num_concurrent
      value: "1"
    - name: max_retries
      value: "3"
    - name: tokenized_requests
      value: "False"
    - name: tokenizer
      value: ibm-granite/granite-guardian-3.1-8b # this isn't used, but we need some valid value here
```
