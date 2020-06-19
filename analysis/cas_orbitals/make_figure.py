import matplotlib.pyplot as plt

anion_im_paths = [f"anion/Anion_NO_{i}.PNG" for i in [148, 149, 150, 151]]
dianion_im_paths = [f"dianion/Dianion_NO_{i}.PNG" for i in [148, 149, 150, 151]]
labels = ["HONO-1", "HONO", "LUNO", "LUNO+1"]


def plot_nos(paths: list):
    for i, pi in enumerate(paths):
        plt.subplot(2, 2, i + 1)
        img = plt.imread(pi)
        # print(img.shape)
        plt.imshow(img[:800, :1000, :])  # Crop out Jmol watermark
        plt.text(0, 1, labels[i], bbox={"alpha": 1.0})
        plt.axis("off")
    plt.tight_layout()


plt.figure()
plot_nos(anion_im_paths)
plt.savefig("anion_nos.png", dpi=900)


plt.figure()
plot_nos(dianion_im_paths)
plt.savefig("dianion_nos.png", dpi=900)
