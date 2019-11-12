import matplotlib.pyplot as plt
import pandas as pd

from utils.plot.plot_rainbow import plot_rainbow

plt.style.use('seaborn-talk')


def plot_emissions(c=None):
    try:
        data = pd.read_excel('results/timeseries.xlsx').reset_index(
            drop=True)
    except:
        return 'No xlsx results found in `../results`. ' \
               'Run `results_to_xlsx` first.'

    data['tax'] = [int(i.split(f'-')[1].replace('USDtCO2', '')) if len(i.split(f'-')) > 1 else 0 for i in data.scenario]
    data['cost'] = [int(i.split(f'-')[0].replace('USDpMWh', '')) if len(i.split(f'-')) > 1 else 'none' for i in
                    data.scenario]

    if c:
        data = data[data.tax.isin(c)]

    base = data.loc[(data.tax == 0) & (data.cost == 'none')].copy()
    scenarios = data.loc[(data.cost != 'none')].copy()

    # Shale gas costs from MUSD/GWa to USD/GJ
    scenarios.loc[:, 'cost'] = [round(i / 8.76 / 3.6, 1) for i in
                                scenarios.loc[:, 'cost']]
    years = [2020, 2030, 2040, 2050]

    # TOTAL EMISSIONS in the shale gas and the no-shale gas scenarios
    df = scenarios.loc[scenarios.variable == 'Emissions|GHG'].copy().reset_index(drop=True).drop('variable',
                                                                                                 axis=1).dropna()
    plot_rainbow(df, 'tax', 'Total GHG Emissions [$MtCO_{2e}$]', 'Total GHG Emissions', years)

    # EMISSION REDUCTION in the no-shale-gas scenarios
    df[years] = df[years].subtract(base[[2020, 2030, 2040, 2050]].values[0], axis=1).copy()
    rel_mit = df.copy()
    rel_mit[years] = rel_mit[years].divide(base[years].values[0], axis=1) * 100

    rel_mit_ng = rel_mit[rel_mit.cost == rel_mit.cost.max()]
    plot_rainbow(rel_mit_ng, 'tax', 'GHG Emission Reduction [%]', 'GHG Emission Reduction', years, rel_NDC=True, lw=2.5)
