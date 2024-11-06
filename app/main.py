import library.config  # noqa
from library.suite.nuke_temperature import nuke_temperature_suite
from library.utils.init_logs import init_logs


def main():
    init_logs()

    for params, answer in nuke_temperature_suite.execute_lazy():
        print(params, answer)


if __name__ == "__main__":
    main()
