import numpy as np
import numpy.typing as npt
import matplotlib
import matplotlib.pyplot as plt
import numba


@numba.jit(nopython=True)
def get_mandelbrot_iterations(c: complex, iterations: int = 5000) -> int:
    """Returns 0 if `c` in mandelbrot set, otherwise returns number of iterations.

    Args:
        c: number to check.
        iterations: max number of iterations.
    """

    z = complex(0)
    for i in range(iterations):
        z = z**2 + c
        if abs(z) > 2:
            return i
    return 0


@numba.jit(nopython=True, parallel=True)
def create_mandelbrot(
    x: float = 0,
    y: float = 0,
    scale: float = 1,
    width: float = 4,
    height: float = 4,
    resolution: tuple[int, int] = (1000, 1000),
    iterations: int = 1000,
) -> npt.NDArray:
    """Creates mandelbrot image (numpy array of pixel colors).

    Args:
        x: x of center.
        y: y of center.
        scale: how much times to scale.
        width: plot width in units.
        height: plot height in units.
        resolution: image size.
    """
    res_x, res_y = resolution

    # Zoom
    width /= scale
    height /= scale

    half_width = width / 2
    x_start = x - half_width
    x_end = x + half_width

    half_height = height / 2
    y_start = y + half_height
    y_end = y - half_height

    cx = np.linspace(x_start, x_end, res_x)
    cy = np.linspace(y_start, y_end, res_y)
    cy = cy * 1j
    image_array = np.empty((len(cx), len(cy)))

    for ix in range(len(cx)):
        for iy in range(len(cy)):
            c = cx[ix] + cy[iy]
            v = get_mandelbrot_iterations(c, iterations=iterations)
            image_array[ix, iy] = v

    return image_array.T


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Mandelbrot plotter.")
    parser.add_argument("-x", type=float, default=0, help="x of center")
    parser.add_argument("-y", type=float, default=0, help="y of center")
    parser.add_argument("-W", "--width", type=float, default=4, help="plot width")
    parser.add_argument("-H", "--height", type=float, default=4, help="plot height")
    parser.add_argument(
        "-s", "--scale", type=float, default=1, help="how much to scale"
    )
    parser.add_argument(
        "-i", "--iterations", type=int, default=1000, help="number of iterations"
    )
    parser.add_argument(
        "-iw", "--image-width", type=int, default=1000, help="image width"
    )
    parser.add_argument(
        "-ih", "--image-height", type=int, default=1000, help="image height"
    )
    parser.add_argument("-c", "--color-map", default="magma", help="color map")
    args = parser.parse_args()

    image = create_mandelbrot(
        x=args.x,
        y=args.y,
        scale=args.scale,
        width=args.width,
        height=args.height,
        iterations=args.iterations,
        resolution=(args.image_width, args.image_height),
    )

    matplotlib.use("qtagg")
    plt.imshow(image, cmap=args.color_map)
    plt.show()


if __name__ == "__main__":
    main()
