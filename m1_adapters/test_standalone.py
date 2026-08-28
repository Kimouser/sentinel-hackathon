import redis


def test_redis_handoff():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()

        test_key = 'cam:test:latest_frame'
        r.set(test_key, 'fake_jpeg_payload')
        retrieved = r.get(test_key)

        if retrieved == 'fake_jpeg_payload':
            print('PASS: M1 frame handoff to Redis works.')
        else:
            print('FAIL: Redis returned unexpected data.')

    except redis.ConnectionError:
        print('FAIL: Could not connect to Redis on port 6379. Is the container running?')


if __name__ == '__main__':
    test_redis_handoff()