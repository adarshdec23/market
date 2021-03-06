from config import sharpe as sharpe
from config import main as main
import numpy as np
from core.database import stockdata
import pickle


class SharpeCompany:
    def __init__(self):
        self.returns = []
        self.results = None
        self.symbol = None

    def set_company(self, symbol):
        link = stockdata.StockData()
        link.sfrom('2007-01-01')
        link.sto('2016-01-20')
        self.symbol = symbol
        self.results = link.get_sdata(symbol)
        self.returns = []  # Reset for a new company

    def get_latest_open(self):
        last_values = self.results[-1]
        with open(main.path+'upinkai/company_clf/'+self.symbol, 'rb') as file:
            load_var = pickle.load(file)
            ans = load_var['svr'].predict(load_var['minMaxFeatures'].transform(last_values))
            return load_var['minMaxPred'].inverse_transform(ans)[0]

    def calculate_returns(self):
        latest = self.results[-1][3]
        close_prices = []
        for i in range(1, sharpe.company_sample_times):
            close_prices.append(float(self.results[-i * sharpe.company_sample_frequency][3]))
        self.returns = [(float(latest) - old_close)*100/old_close for old_close in close_prices]

    def get_company_risk(self, sharpe_ratio):
        if sharpe_ratio <= 0.2:
            return 'high'
        elif 0.2 < sharpe_ratio <= 0.58:
            return 'moderate'
        else:
            return 'low'

    def get_ratio(self):
        self.calculate_returns()
        np_returns = np.array(self.returns)
        std = np_returns.std()
        mean = np_returns.mean()
        sharpe_ratio = (mean - sharpe.risk_free_rate)/std
        risk = self.get_company_risk(sharpe_ratio)
        return dict(
            sharpe=sharpe_ratio,
            mean=mean,
            std=std,
            risk=risk.capitalize(),
        )

    def get_all_company_ratios(self):
        link = stockdata.StockData()
        all_companies = link.get_all_companies()
        company_risks = []
        for row in all_companies:
            risk_builder = list(row)
            self.set_company(row[2])
            risk_builder.append(self.get_ratio())
            company_risks.append(risk_builder)
        return company_risks
