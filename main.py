from amo_class import Amocrm

if __name__ == '__main__':
    payload = {
        'USER_LOGIN': 'Service@aspex.kz',
        'USER_HASH': '8875b2ad63b166a2ad9efe660831c252d9c90a7c',
    }
    headers = {
        'X-Requested-With': 'XMLHttpRequest'
    }
    params = {

    }
    subdomain = 'certitdev'
    mirror = 'z1'
    f = Amocrm(payload=payload, subdomain=subdomain, mirror=mirror)
    data = f.get_events(params=params, headers=headers, url='events/list/page/1')
    print(data.json())