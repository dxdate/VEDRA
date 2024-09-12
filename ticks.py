def test(self, num, bad_num):
    if not len(self.buckets) == 0:
        if random.random() <= self.bad_num_chance:
            if bad_num == num:
                self.label_bad_num.setText(f"Аварийная лампа! Ведра сопадают, пропускаем!")
            elif self.Buckets.check_bucket_empty(bad_num % len(self.buckets)):
                self.label_bad_num.setText(f"Аварийная лампа! Ведро пустое, пропускаем!")
                self.label_generated_number.setText(f"Gen num: {str(num)}  Buc i: {str((num + 1) % len(self.buckets))}")
                self.Buckets.add_water_to_bucket(num % len(self.buckets))
            else:
                self.label_bad_num.setText(f"Аварийная лампа! Из ведра {str((bad_num + 1) % len(self.buckets))} выбежал литр(")
                self.Buckets.remove_water_from_bucket(bad_num % len(self.buckets))
                self.label_generated_number.setText(f"Gen: {str(num)}  Добавили в ведро: {str((num + 1) % len(self.buckets))}")
                self.Buckets.add_water_to_bucket(num % len(self.buckets))
        else:
            self.label_bad_num.setText(f"Все работает без ошибок:)")

            self.label_generated_number.setText(f"Gen: {str(num)}  Добавили в ведро: {str((num + 1) % len(self.buckets))}")
            self.Buckets.add_water_to_bucket(num % len(self.buckets))
        if not self.Buckets.check_bucket_full(num % len(self.buckets)):
            self.hide_bucket(num % len(self.buckets))
        self.fill_buckets_text()

