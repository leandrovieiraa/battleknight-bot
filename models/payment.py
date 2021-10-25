import logging, time
from lxml import html


class Payment:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    @classmethod
    def get_reward(self, rsession, server_url, character):
        headers = dict()
        headers['Upgrade-Insecure-Requests'] = '1'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36'
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'

        payload = dict()
        payload['paycheck'] = 'encash'

        r = rsession.post(f'{server_url}/market/work', headers=headers, data=payload)
        r = rsession.get(f'{server_url}/market/work', headers=headers)
        tree = html.fromstring(r.content)
        
        past_silver = character.silver
        new_silver = tree.xpath('//*[@id="silverCount"]/text()')[0]
        character.silver = int(new_silver)
        
        logging.info(f'O jogador possuia {past_silver} de prata e agora possui: {character.silver}')
