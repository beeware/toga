import toga
from toga.style import Pack
from matplotlib.figure import Figure
import numpy as np
from toga.constants import COLUMN


def sample_histogram():
    np.random.seed(19680801)

    # example data
    mu = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution
    x = mu + sigma * np.random.randn(437)

    num_bins = 50

    f = Figure(figsize=(5, 4), dpi=100)
    ax = f.add_subplot(1, 1, 1)

    # the histogram of the data
    n, bins, patches = ax.hist(x, num_bins, density=1)

    # add a 'best fit' line
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    ax.plot(bins, y, '--')
    ax.set_xlabel('Smarts')
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

    return f


class ExampleChartApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.chart = toga.Chart(style=Pack(flex=1))

        self.main_window.content = toga.Box(
            children=[
                self.chart,
            ],
            style=Pack(direction=COLUMN)
        )

        self.chart.draw(sample_histogram())

        self.main_window.show()


def main():
    return ExampleChartApp('Chart', 'org.pybee.widgets.chart')


if __name__ == '__main__':
    main().main_loop()
