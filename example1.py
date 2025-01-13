import taichi as ti
import numpy as np

from simple_relief_mapper import SimpleReliefMapper
from height import simplex_height_map


def run(renderer: SimpleReliefMapper):
    window = ti.ui.Window(name='Example 1', res=renderer.get_shape(), fps_limit=60, pos=(0, 0))
    gui = window.get_gui()
    canvas = window.get_canvas()
    azimuth = 45.0 # light source horizontal direction, degrees
    altitude = 45.0 # light source vertical direction, degrees
    classic = True
    zoom = 1.0
    spp = 1
    light_source_width = 0.0
    while window.running:
        with gui.sub_window("Sub Window", 0.1, 0.1, 0.8, 0.3):
            classic = gui.checkbox("classic mode", classic)
            gui.text(f"azimuth: {azimuth:.0f} degrees")
            altitude = gui.slider_float("altitude (deg)", altitude, 0, 89)
            zoom = gui.slider_float("zoom", zoom, 0.1, 10.0)
            spp = gui.slider_int("samples per pixel", spp, 1, 16)
            light_source_width = gui.slider_float("light source width (degrees)", light_source_width, 0.0, 5.0)

        dx, dy, dz = renderer.get_direction(azimuth, altitude)
        renderer.render(dx, dy, dz, classic, zoom, spp=spp, lsw=light_source_width)
        canvas.set_image(renderer.get_image())
        window.show()

        # the following rotates the azimuth between 0 and 360 degrees, with increments of 1 degree per step
        azimuth = (azimuth + 1) % 360


def example_map_1(n):
    """A height map generated from simplex noise with dimension n.
    In the middle, a small plateau is defined with
    height 0, and inside that plateau a tower
    of height n is placed.
    :param n: map dimension
    :return: a 2D height map in the form of a numpy array.
    """
    octaves = int(np.log2(n))
    z = simplex_height_map(dim=n, octaves=octaves, amplitude=n, seed=42)
    z = np.float32(z)

    # middle plateau
    z[n // 2 - n // 8:n // 2 + n // 8, n // 2 - n // 8:n // 2 + n // 8] = 0

    # middle tower
    z[n // 2 - n // 32:n // 2 + n // 32, n // 2 - n // 32:n // 2 + n // 32] = n
    return z


def main(n):
    # define height map
    z = example_map_1(n)

    # initialize renderer
    renderer = SimpleReliefMapper(height_map=z, cell_size=1.0)

    # run app
    run(renderer)


if __name__ == "__main__":
    main(n=512)
