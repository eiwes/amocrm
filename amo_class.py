import logging
from session_with_base_url import SessionWithBaseUrl


class Amocrm:
    OK = 200
    LOGS = 'actions.log'

    logging.basicConfig(filename='actions.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

    def __init__(self, payload, subdomain, mirror):
        self.__payload = payload
        self.__subdomain = subdomain
        self.__auth = False
        self._lasterror = ''
        self.__baseurl = f'https://{self.__subdomain}.amocrm.ru/'
        self.__mirror = mirror

        self.__make_auth()
        if self.get_auth_status():
            with open(self.LOGS, 'r') as f:
                actions = f.readlines()
        else:
            with open(self.LOGS, 'r') as f:
                actions = f.readlines()
            self.__second_auth()

    def __second_auth(self):
        self.__baseurl = f'https://{self.__subdomain}.{self.__mirror}.amocrm.ru/'
        if self.get_auth_status():
            logging.info('Авторизация на зеркале успешна')
        else:
            logging.error('Ошибка авторизации на зеркале')
            return 403


    def get_auth_status(self):
        if self.status_code == self.OK:
            self.__auth = True
            return True
        return False

    def get_error_message(self):
        with open(self.LOGS, 'r') as f:
            errors = f.readlines()
            if len(errors) > 0:
                return errors[-1]
            return 'No errors'

    def __make_auth(self):
        try:
            self.session = SessionWithBaseUrl(self.__baseurl)
            response = self.__post_request(url = 'private/api/auth.php', payload=self.__payload, retries=2)
            self.status_code = response.status_code
            if self.status_code == self.OK:
                logging.info('Успешная авторизация')
        except Exception as e:
            self.status_code = -1  # If you wrote incorrect url or url is not responsible
            logging.error('Ошибка первичной авторизации')
            self.__second_auth()
            print (self.get_error_message())

    def __post_request(self, url, payload, retries=1):
        response = self.session.request('post', url, data=payload)
        if response.status_code != self.OK:
            logging.error('Ошибка запроса POST')
            print(self.get_error_message())
            retries -= 1
            if retries == 0:
                return None
            logging.info('Повторный POST запрос')
            return self.__post_request(self, url, payload, retries)
        else:
            return response

    def __get_request(self, url, headers, params):
        if self.__auth:
            logging.info('Успешный запрос GET')
            return self.session.request('get', url, params=params, headers=headers)
        else:
            logging.info('Ошибка запроса GET')
            print(self.get_error_message())
            return self.status_code

    def get_events(self, url, params, headers):
        return self.__get_request(url, params=params, headers=headers)


