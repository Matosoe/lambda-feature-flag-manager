FROM public.ecr.aws/lambda/python:3.11

# Copiar requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Instalar dependências
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Copiar código da aplicação
COPY src/ ${LAMBDA_TASK_ROOT}/src/
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Handler da Lambda
CMD ["lambda_function.lambda_handler"]
