import dataclasses
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

@dataclasses.dataclass
class timebar:
    start: float
    stop: float
    row: int=0

    def __init__(self, start: str, stop: str, row: int=0, category: int=None,label: str=""):
        self.start = mdates.datestr2num(start)
        self.stop = mdates.datestr2num(stop)
        self.row = row
        if category is None:
            self.category = row
        else:
            self.category = category
        self.label=label

grad = np.atleast_2d(np.linspace(1,0,256))

def gannt(
    ax
    ,bars
    ,color_range = 0.83
    ,cmaps = ["Purples","Blues","Greens","Oranges","Reds"]
    ,spacing = 0.2
    ,xticks="years"
    ,datelines='below'
    ,box=False
    ,date_fmt=None):

    lim = ax.get_xlim()+ax.get_ylim()
    bar_rects = [ax.barh(-bar.row, bar.stop - bar.start, left=bar.start, height=(1-spacing), align='center')[0] for bar in bars]


    #from https://stackoverflow.com/questions/38830250/how-to-fill-matplotlib-bars-with-a-gradient
    ax = bar_rects[0].axes
    lim = ax.get_xlim()+ax.get_ylim()
    for bar_rect,bar in zip(bar_rects,bars):
        bar_rect.set_zorder(1)
        bar_rect.set_facecolor("none")
        x,y = bar_rect.get_xy()
        w, h = bar_rect.get_width(), bar_rect.get_height()
        cmap = cmaps[bar.category]
        ax.imshow(grad, extent=[x,x+w,y,y+h], aspect="auto", zorder=0.6,cmap=cmap,vmin=0,vmax=1./color_range)

        ax.text(x+w,y+h/2,bar.label,family='sans-serif',va='center',ha='right')
    ax.axis(lim)


    ax.get_yaxis().set_visible(False)
    ax.xaxis_date()

    if date_fmt is not None:
        if not isinstance(date_fmt,mdates.DateFormatter):
            date_fmt = mdates.DateFormatter(date_fmt)

    if xticks=="years":
        years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        if date_fmt is None:
            date_fmt = mdates.DateFormatter('%Y')
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(date_fmt)
        ax.xaxis.set_minor_locator(months)
    elif xticks=="months":
        months = mdates.MonthLocator()  # every month
        days = mdates.DayLocator()  # every day
        if date_fmt is None:
            date_fmt = mdates.DateFormatter('%b')
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(date_fmt)
        ax.xaxis.set_minor_locator(days)
    else:
        raise ValueError("xticks must be 'months' or 'years'")

    if not box:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

    if datelines is not None:
        ax.grid(True,axis='x',ls='--')
        if datelines=="below":
            ax.set_axisbelow(True)

fig, ax = plt.subplots(figsize=(8,3),constrained_layout=True) 
bars = [
        timebar("2020-01-01","2020-06-01",0,0,"Time in lieu")
        ,timebar("2020-06-01","2021-01-01",0,1,"Time in loo")
        ,timebar("2020-03-01","2020-09-01",1,0,"Procrasti[TODO]")
        ,timebar("2020-04-01","2021-08-01",2,2,"Observing time (N/A)")
        ,timebar("2019-09-01","2022-03-01",3,3,"Removing semicolons")
        ,timebar("2020-09-01","2021-02-01",4,0,"...nation")
        ]
gannt(ax,bars)
fig.savefig("devel.pdf")