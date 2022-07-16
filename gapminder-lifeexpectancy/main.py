# %%
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.widgets import Slider

sns.set_style('darkgrid')

# import matplotlib as mpl
# mpl.use('Qt5Agg')
# %%
# Load datasets
gapminder = pd.read_csv('dataset/gapminder_full.csv')

# %%
# Preliminary information
print(gapminder.shape)
print(gapminder.info())
print(gapminder.describe())
print(gapminder[['country', 'continent']].describe())

# Missing values?
print(gapminder.isnull().sum(axis=0))
# %%
# Plot distribution of population
plt.hist(x=gapminder['population'], bins=50)
# plt.xlim(0,0.2e9)
plt.show()

# %%
# Set Bin values into discrete intervals
bins = [0, 0.25e8, 0.50e8, 0.75e8, 1e8, 1.25e8, 1.5e8, 1.75e8, 2e8, 6e8, np.max(gapminder['population'])]
sizes = (np.arange(1, len(bins)) * 10).tolist()
gapminder['pop_bins'] = pd.cut(x=gapminder['population'], bins=bins,
                               labels=sizes,
                               include_lowest=True)
print(gapminder['pop_bins'].describe())
# %%
# initialize matplotlib figure
fig, ax = plt.subplots(figsize=(10, 6))
# adjust the subplots region to leave some space for the sliders and buttons
fig.subplots_adjust(bottom=0.25)
# define an axes area and draw a slider in it
my_slider_ax = fig.add_axes([0.25, 0.1, 0.65, 0.03])
# generate slider with initial value
my_slider = Slider(ax=my_slider_ax, label='Year',
                   valmin=gapminder['year'].min(),
                   valmax=gapminder['year'].max(),
                   valinit=gapminder['year'].min(),
                   valstep=5)


# define an action for when the slider's value changes
def slider_action(val):
    # the figure is updated when the slider is changed
    update_plot(np.round(val))


# link slider_action function to slider object
my_slider.on_changed(slider_action)


# define how to update the plot
def update_plot(year):
    # clear the axis before the plot is redrawn
    ax.clear()
    sns.scatterplot(x='gdp_cap',
                    y='life_exp',
                    data=gapminder[gapminder['year'] == year],
                    hue='continent',
                    size='pop_bins',
                    sizes=sizes,
                    alpha=0.5,
                    legend=False,
                    ax=ax)
    # Labels, Limits
    ax.set_title('Title')
    #     ax.set_xlim(-10, gapminder['gdp_cap'].max()*1.1)
    ax.set_xlim(100, 6e4)
    ax.set_ylim(25, gapminder['life_exp'].max() * 1.1)
    ax.set_xscale('symlog')
    #     ax.set_yscale('log')

    ax.text(x=5.5, y=0.5, s=year, fontsize='x-large',
            ha='center', va='center')
    #     ax.text(x=5.5, y=0.5, s=year, fontsize='x-large',
    #             ha='center', va='center', transform=ax.transAxes)
    #     ax.legend(loc='lower right')

    # # keep the axis limits constant for better visibility of the changes
    # ax.set_ylim(0, np.max(df.my_value.values))
    # update figure
    fig.canvas.draw_idle()


# draw initial plot with default intensity
update_plot(gapminder['year'].min())

# display figure
plt.show()