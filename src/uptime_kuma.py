import requests
from icecream import ic


def push_health_check(web_address: str) -> None:
    try:
        requests.get(web_address, verify=False)
    except Exception as e:
        ic(f'Error in push_health_check: {e}')
        ic(f'web_address: {web_address}')


def main():
    pass


if __name__ == '__main__':
    main()
