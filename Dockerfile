FROM registry.access.redhat.com/ubi9/ubi:latest

COPY *.py app/
COPY requirements.txt app/
COPY bigrams.json app/

WORKDIR app
RUN dnf install -y \
        gcc \
        gcc-c++ \
        make \
        redhat-rpm-config && \
    dnf clean all

# install python
RUN dnf install -y jq python3.12 python3.12-devel python3.12-pip unzip && \
    dnf clean all && \
    python3.12 -m pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "vllm_emulator:app", "--host", "0.0.0.0", "--port", "8000"]