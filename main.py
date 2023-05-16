from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest, InviteToChannelRequest
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsRecent
from time import sleep

api_id = 0       # Your API ID
api_hash = '0'  # Your API HASH
phone_number = ''
client = TelegramClient('session_name', api_id, api_hash)


async def main():
    await client.start(phone_number)
    print("Client conectado com sucesso!")

    # Obtenha o grupo de origem
    source_group = await client.get_entity('')

    # Obtenha todos os participantes do grupo de origem
    offset = 0
    limit = 190
    all_participants = []
    while True:
        participants = await client(GetParticipantsRequest(
            channel=source_group,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)

    # Obtenha o grupo de destino
    target_group = await client.get_entity('')

    # Adicione cada usuário do grupo de origem ao grupo de destino
    for user in all_participants:
        try:
            await client(InviteToChannelRequest(target_group.id, [user]))
            print(f"Usuário {user.first_name} adicionado com sucesso!")
            sleep(60)
        except:
            print(f"Erro ao adicionar usuário {user.first_name}")
            sleep(60)

    await client.disconnect()

with client:
    client.loop.run_until_complete(main())
