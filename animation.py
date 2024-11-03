class Animation:
    def __init__(self, sp, tr, indices):
        self.sp = sp
        self.tr = tr
        self.images = []
        for i in indices:
            self.images.append(sp.get_image_idx(i))

    def get_image(self, idx):
        return self.images[(idx // self.tr) % len(self.images)]
