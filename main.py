import argparse
import logging

import invokust

from setting import BASE_URL
from task_models.catalogue_tests import CatalogueUser

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start load testing')
    parser.add_argument('--num_users', default=50, type=int, help='Number of users to create')
    parser.add_argument('--spawn_rate', default=10, type=int, help='spawn rate')
    parser.add_argument('--run_time', default='5m', type=str,
                        help='Run time limit. Set as str value, e.g. 30s, 10m, 24h, etc')
    args = parser.parse_args()

    if BASE_URL is None:
        logger.error(f"Base URL is not defined, check if you set valid value to BASE_URL param.\n"
                     f"current base_url value: {BASE_URL}")

    else:
        settings = invokust.create_settings(
            classes=[CatalogueUser],
            host=BASE_URL,
            num_users=args.num_users,
            spawn_rate=args.spawn_rate,
            run_time=args.run_time
        )

        load_test = invokust.LocustLoadTest(settings)
        load_test.run()
        load_test.stats()
