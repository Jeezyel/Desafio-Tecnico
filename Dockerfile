# Etapa 1: Definir a imagem base
FROM python:3.9-slim

# Etapa 2: Definir o diretório de trabalho no contêiner
WORKDIR /app

# Etapa 3: Copiar os arquivos de dependência (requirements.txt)
COPY requirements.txt ./

# Etapa 4: Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar os arquivos específicos da aplicação
COPY AppRedes.py .
COPY netbox_integration.py .
COPY netBox_Integration_2.py .
COPY simulated_snmp_data.json .

# Etapa 6: Expor a porta 5000 para acesso à API Flask
EXPOSE 5000

# Etapa 7: Definir o comando para rodar a aplicação
CMD ["python", "AppRedes.py"]
