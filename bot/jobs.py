import logging, random, time
from lxml import html
from tqdm import trange
from requests.sessions import Session
from models.character import Character
from models.worldmap import WorldMap
from models.payment import Payment


class Jobs:

    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        global rsession
        rsession = Session()

    @classmethod
    def headers(self):
        headers = dict()
        headers['Upgrade-Insecure-Requests'] = '1'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        return headers


    @classmethod
    def login(self, server_url, endpoint, username, password):
        # https://s26-br.battleknight.gameforge.com/main/login/leandrovieira92@gmail.com/26197421d65208d057f7b2dcf682979b?kid=&gfsid&servername=null&serverlanguage=null
        r = rsession.get(f'{server_url}/{endpoint}/{username}/{password}?kid=&gfsid&servername=null&serverlanguage=null', headers=self.headers())
        tree = html.fromstring(r.content)
        news = tree.xpath('//*[@id="playerNews"]/h3/text()')
        if news:
            logging.info(f"O jogador ('{username}') logou com sucesso")


    @classmethod
    def load_character(self, server_url, endpoint):
        r = rsession.get(f'{server_url}/{endpoint}', headers=self.headers())
        tree = html.fromstring(r.content)

        character_lvl = tree.xpath('//*[@id="userLevel"]/span/text()')
        character_silver = tree.xpath('//*[@id="silverCount"]/text()')

        character_base_str = tree.xpath('//*[@id="attrBaseStrength"]/text()')
        character_item_str = tree.xpath('//*[@id="attrItemStrength"]/text()')

        character_base_dex = tree.xpath('//*[@id="attrBaseDexterity"]/text()')
        character_item_dex = tree.xpath('//*[@id="attrItemDexterity"]/text()')

        character_base_end = tree.xpath('//*[@id="attrBaseEndurance"]/text()')
        character_item_end = tree.xpath('//*[@id="attrItemEndurance"]/text()')

        character_base_lck = tree.xpath('//*[@id="attrBaseLuck"]/text()')
        character_item_lck = tree.xpath('//*[@id="attrItemLuck"]/text()')

        character_base_wpn = tree.xpath('//*[@id="attrBaseWeapon"]/text()')
        character_item_wpn = tree.xpath('//*[@id="attrItemWeapon"]/text()')

        character_base_def = tree.xpath('//*[@id="attrBaseShield"]/text()')
        character_item_def = tree.xpath('//*[@id="attrItemShield"]/text()')

        character_hp = tree.xpath('//*[@id="attrCurrentHealth"]/text()')
        character_max_hp = tree.xpath('//*[@id="attrMaxHealth"]/text()')

        character_karma = tree.xpath('//*[@id="trAttrTableKarma"]/text()')
        character_dmg = tree.xpath('//*[@id="attrTableDamage"]/text()')
        character_armour = tree.xpath('//*[@id="attrTableArmor"]/text()')
        character_offensive = tree.xpath('//*[@id="attrTableOffensive"]/text()')
        character_defensive = tree.xpath('//*[@id="attrTableDefensive"]/text()')

        if character_base_str:
            attributes = f"Carregando atributos:\n\
            Level: {character_lvl[0].strip()}\n\
            Prata: {character_silver[0].strip()}\n\
            Força: {character_base_str[0].strip()} {character_item_str[0].strip()}\n\
            Aptidão: {character_base_dex[0].strip()} {character_item_dex[0].strip()}\n\
            Constituição: {character_base_end[0].strip()} {character_item_end[0].strip()}\n\
            Sorte: {character_base_lck[0].strip()} {character_item_lck[0].strip()}\n\
            Habilidade com Armas: {character_base_wpn[0].strip()} {character_item_wpn[0].strip()}\n\
            Arte defensiva: {character_base_def[0].strip()} {character_item_def[0].strip()}\n\
            Pontos de vida: {character_hp[0].strip()} {character_max_hp[0].strip()}\n\
            Karma: {character_karma[0].strip()}\n\
            Danos: {character_dmg[0].strip()}\n\
            Armadura: {character_armour[0].strip()}\n\
            Possibilidade de Sucesso: {character_offensive[0].strip()}\n\
            Possibilidade de Defesa: {character_defensive[0].strip()}".replace('    ', '')
            logging.info(attributes)
        
        char = Character(
            level=int(character_lvl[0].strip()),
            silver=int(character_silver[0].strip())
        )
        return char


    @classmethod
    def go_to_mission(self, server_url, endpoint, character):
        logging.info('O jogador irá fazer uma missão aleatória baseada no level')
        
        r = rsession.get(f'{server_url}/{endpoint}', headers=self.headers())
        tree = html.fromstring(r.content)

        work_payment = tree.xpath('//*[@id="encashLink"]/span')
        if work_payment:
            Payment.get_reward(rsession, server_url, character)

        progress_bar = tree.xpath('//*[@id="progressbarEnds"]/span/text()')
        if progress_bar:
            logging.info(f'O jogador deverá esperar para iniciar uma missão, tempo restante: {progress_bar[0].strip()}')
            return

        mapbase = tree.xpath('//*[@id="mapBase"]')

        if mapbase:
            worldmap = WorldMap(character.level)
            worldmap_objs = []
            for region in worldmap.load_map():
                region_obj = tree.xpath(f'//*[@id="{region}"]')
                if region_obj:
                    worldmap_objs.append({'obj': region_obj[0], 'name': region})
            
            selected_mission = random.choice(worldmap_objs)
            mission_type = ['Good', 'Evil']
            selected_mission_type = random.choice(mission_type)

            logging.info(f'Selecionando missão aleatória no local {selected_mission["name"]} do tipo {selected_mission_type}')

            payload = dict()
            payload['chooseMission'] = selected_mission["name"]
            payload['missionArt'] = 'small'
            payload['missionKarma'] = selected_mission_type
            payload['buyRubies'] = 0
            
            r = rsession.post(f'{server_url}/{endpoint}', headers=self.headers(), data=payload)
            tree = html.fromstring(r.content)
            
            check_combat = tree.xpath('//*[@id="tabsnavi"]/ul/li/span[2]/h3/text()')
            if check_combat:
                result = tree.xpath('//*[@id="mainContent"]/div[2]/div[1]/div[2]/div/h1/em/text()')
                if result:
                    logging.info(f'Resultado do combate: {result[0].strip()}')
                    
                    past_silver = character.silver
                    new_silver = tree.xpath('//*[@id="silverCount"]/text()')[0]
                    character.silver = int(new_silver)
                    
                    logging.info(f'O jogador possuia {past_silver} de prata e agora possui: {character.silver}')
                    
                    logging.info(f'Aguardando a missão ser finalizada para continuar')
                    for _ in trange(150):
                        time.sleep(1) 
            else:
                logging.info('O personagem não possui mais pontos de missão, os pontos de missão regeneram-se em 10 por hora')
                return


    @classmethod
    def go_to_work(self, server_url, endpoint, character):
        logging.info('O jogador irá realizar um trabalho aleatório')
        
        r = rsession.get(f'{server_url}/{endpoint}', headers=self.headers())
        tree = html.fromstring(r.content)

        progress_bar = tree.xpath('//*[@id="progressbarEnds"]/span/text()')
        if progress_bar:
            logging.info(f'O jogador deverá esperar para iniciar um trabalho, tempo restante: {progress_bar[0].strip()}')
            return

        works = ['good', 'evil', 'natural']
        timers = [1, 2, 3, 4, 5, 6, 7, 8]

        selected_work = random.choice(works)
        selected_time = random.choice(timers)

        logging.info(f'Selecionando trabalho e tempo aleatório: {selected_work} - {selected_time * 900}s')

        payload = dict()
        payload['side'] = selected_work
        payload['hours'] = selected_time
        
        r = rsession.post(f'{server_url}/{endpoint}', headers=self.headers(), data=payload)
        tree = html.fromstring(r.content)

        logging.info(f'Aguardando o trabalho ser finalizado')
        for _ in trange(900 * selected_time):
            time.sleep(1)
        
        r = rsession.get(f'{server_url}/{endpoint}', headers=self.headers())
        Payment.get_reward(rsession, server_url, character)
