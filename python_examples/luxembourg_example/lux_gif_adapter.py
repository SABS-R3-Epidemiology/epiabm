import glob
from PIL import Image

animation_path = ("simulation_outputs/")
fp_in = animation_path + "image" + "*d_log.png"
fp_out = animation_path + "voronoi_log_animation.gif"

img, *imgs = [Image.open(f).convert("RGB")
              for f in sorted(glob.glob(fp_in))]

img.save(fp=fp_out,
         format="GIF",
         append_images=imgs,
         save_all=True,
         duration=50,
         loop=0,
         optimise=True,
         )
