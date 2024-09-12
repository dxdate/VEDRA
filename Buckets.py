import random

class Buckets():
    def __init__(self):
        self.start_liters = 1
        self.speed = 0
        self.zero_speed_time = 300_000
        self.max_speed_time = 1
        self.buckets = []
        self.tick_time = 0

    def generate_buckets(self):
        for i in range(10):
            self.buckets.append([i, self.start_liters])
        return self.buckets

    def calculate_tick_time(self):
        return int(self.zero_speed_time / (1 + (self.speed / 10) ** 4))


    def add_water_to_bucket(self, bucket_i):
        self.buckets[bucket_i][1] += 1
        return self.buckets

    def remove_water_from_bucket(self, bucket_i):
        self.buckets[bucket_i][1] -= 1
        return self.buckets

    def check_bucket_full(self, bucket_i):
        if self.buckets[bucket_i][1] == 10:
            return False
        return True

    def check_bucket_empty(self, bucket_i):
        if self.buckets[bucket_i][1] == 0:
            return True
        return False
