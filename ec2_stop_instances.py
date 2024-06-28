import boto3
import schedule
import time

def stop_ec2_instances():
    # Importação e Configuração do Cliente EC2
    ec2 = boto3.client('ec2')

    # Filtragem de Instâncias com a Tag stop_ec2 e Estado running
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:stop_ec2',
                'Values': ['true']
            },
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )

    # Coleta de IDs das Instâncias que Devem Ser Paradas
    instances_to_stop = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances_to_stop.append(instance['InstanceId'])

    # Parada das Instâncias
    if instances_to_stop:
        print(f"Parando as instâncias: {instances_to_stop}")
        ec2.stop_instances(InstanceIds=instances_to_stop)
        print("Solicitação para parar instâncias enviada com sucesso.")
    else:
        print("Nenhuma instância com a tag 'stop_ec2' em estado 'running' encontrada.")

# Agendamento da Execução do Script às 18h
schedule.every().day.at("18:00").do(stop_ec2_instances)

print("Script de agendamento iniciado. O script será executado às 18h todos os dias.")

while True:
    schedule.run_pending()
    time.sleep(1)
