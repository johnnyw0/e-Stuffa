# Projeto Estufa Inteligente - Monitoramento de Temperatura e Umidade

Este projeto implementa um sistema de monitoramento para uma estufa, coletando dados de temperatura e umidade de dispositivos IoT, processando-os e visualizando-os em tempo real. A arquitetura é baseada em componentes do ecossistema FIWARE, garantindo interoperabilidade e escalabilidade.

## Tecnologias Utilizadas

* **Docker & Docker Compose**: Orquestração e gerenciamento dos contêineres para todos os serviços.
* **FIWARE Orion Context Broker**: Componente central para gerenciamento de contexto, responsável por manter o estado dos dispositivos e suas informações.
* **FIWARE IoT Agent for UltraLight 2.0 (IOTA-UL)**: Agente IoT que permite a conexão de dispositivos usando o protocolo UltraLight 2.0 e traduz suas mensagens para o padrão NGSI do Orion Context Broker.
* **Mosquitto**: Broker MQTT, utilizado para a comunicação assíncrona entre os dispositivos IoT e o IoT Agent.
* **FIWARE Cygnus**: Conector de persistência de dados que assina as atualizações de contexto do Orion e as envia para um banco de dados externo (MySQL, neste caso).
* **MongoDB**: Banco de dados NoSQL utilizado pelo Orion Context Broker e pelo IoT Agent para persistir seus dados internos.
* **MySQL**: Banco de dados relacional utilizado pelo Cygnus para armazenar os dados históricos de temperatura e umidade dos sensores.
* **Grafana**: Plataforma de visualização e análise de dados, conectada ao MySQL para criar dashboards interativos com os dados históricos.
* **Dummy Device (Python)**: Um dispositivo simulado, desenvolvido em Python, que envia dados de temperatura e umidade via MQTT para o sistema.

## Arquitetura do Projeto

A arquitetura do projeto é composta pelos seguintes serviços:

1.  **`mongo-db`**: Banco de dados MongoDB, servindo como backend para o Orion Context Broker e o IoT Agent.
2.  **`orion`**: O Orion Context Broker, responsável por gerenciar o contexto (estado) dos sensores da estufa.
3.  **`mosquitto`**: O broker MQTT, atuando como o ponto de entrada para as mensagens dos sensores (dispositivos dummy).
4.  **`iot-agent-ul`**: O IoT Agent for UltraLight 2.0, que recebe as mensagens dos sensores via MQTT, as traduz para o formato NGSI e as envia para o Orion.
5.  **`dummy-device`**: Um dispositivo simulado (escrito em Python) que gera e envia dados de temperatura e umidade para o `mosquitto`.
6.  **`mysql-db`**: Banco de dados MySQL, onde o Cygnus persistirá os dados históricos dos sensores.
7.  **`cygnus`**: O Cygnus NGSI, que se inscreve nas atualizações de contexto do Orion e armazena esses dados no `mysql-db`.
8.  **`grafana`**: A plataforma Grafana, que se conecta ao `mysql-db` para visualizar os dados históricos de temperatura e umidade em dashboards personalizáveis.

```mermaid
graph TD
    A[Dummy Device (Python)] -- MQTT --> B(Mosquitto)
    B -- MQTT --> C(IoT Agent UL)
    C -- NGSI --> D(Orion Context Broker)
    D -- Subscription --> E(Cygnus)
    E -- Persist Data --> F(MySQL DB)
    F -- Data Source --> G(Grafana)
    D -- Internal Data --> H(MongoDB)
    C -- Internal Data --> H
