class Animation:
    def __init__(self, sp, tr, indices):
        self.sp = sp
        self.tr = tr
        self.tick = 0
        self.images = []
        for idx in indices:
            self.images.append(sp.get_image_idx(idx))

    def get_image(self):
        idx = self.images[(self.tick // self.tr) % len(self.images)]
        self.tick += 1
        return idx
