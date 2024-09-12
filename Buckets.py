import random

class Buckets():
    def __init__(self):
        self.generated_number = 0
        self.start_liters = 2
        self.speed = 0
        self.zero_speed_time = 300_000  # 300 секунд
        self.max_speed_time = 1  # 0.3 секунды
        self.full_buckets = []
        self.buckets = []
        self.tick_time = 0
        # self.generate_buckets()
        # self.create_tick()

    def generate_buckets(self):
        for i in range(10):
            self.buckets.append([i, self.start_liters])
        return self.buckets

    def calculate_tick_time(self):
        return int(self.zero_speed_time / (1 + (self.speed / 10) ** 4))


    def add_water_to_bucket(self, bucket_i):
        self.buckets[bucket_i][1] += 1
        return self.buckets

    def check_bucket(self, bucket_i):
        if self.buckets[bucket_i][1] == 10:
            return False
        return True
