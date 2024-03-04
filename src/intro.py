import platform


def get_intro(docker_repo: str,
              current_version: str,
              github_readme: str,
              uptime_kuma_url: str,
              uptime_kuma_check: str) -> str:

    intro_msg = "Completed importing environment variables. No errors.\n\n"
    intro_msg = intro_msg + f"Github repository: {docker_repo}:{current_version}\n"
    intro_msg = intro_msg + f"Python version: {platform.python_version()}\n"
    intro_msg = intro_msg + f"System platform: {platform.system()}\n"
    intro_msg = intro_msg + f"Documentation: {github_readme}\n\n\n"

    intro_msg = intro_msg + f"System checks health via UpTime-kuma every {uptime_kuma_check}\n"
    intro_msg = intro_msg + f"UpTime-kuma url: {uptime_kuma_url} seconds\n\n"

    intro_msg = intro_msg + "Starting main loop that check lectio messageing is working\n"
    intro_msg = intro_msg + '**************************************************************************************\n\n'
    return intro_msg


def main():
    pass


if __name__ == '__main__':
    main()
