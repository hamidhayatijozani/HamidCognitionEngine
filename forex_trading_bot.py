import pandas as pd
import numpy as np
import json
from datetime import datetime

# --- 1. Trading Bot Class and Strategy Implementation ---

class ForexTradingBot:
    """
    موتور معاملات خودکار فارکس با استراتژی SMA Cross.
    """
    
    def __init__(self, short_window=10, long_window=30, initial_capital=10000, risk_per_trade=0.01):
        self.short_window = short_window
        self.long_window = long_window
        self.capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.trades = []
        self.equity_curve = [initial_capital]
        self.position = 0  # 1 for long, -1 for short, 0 for flat
        self.entry_price = 0
        self.stop_loss = 0
        self.take_profit = 0
        self.trade_id_counter = 1

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        محاسبه میانگین متحرک ساده (SMA) و تولید سیگنال‌های خرید/فروش.
        """
        data['SMA_Short'] = data['Close'].rolling(window=self.short_window).mean()
        data['SMA_Long'] = data['Close'].rolling(window=self.long_window).mean()
        
        # سیگنال خرید: SMA کوتاه از SMA بلند عبور کند (از پایین به بالا)
        data['Signal'] = 0
        data.loc[data['SMA_Short'] > data['SMA_Long'], 'Signal'] = 1
        
        # سیگنال فروش: SMA بلند از SMA کوتاه عبور کند (از پایین به بالا)
        data.loc[data['SMA_Short'] < data['SMA_Long'], 'Signal'] = -1
        
        # موقعیت معاملاتی: سیگنال را به موقعیت تبدیل می‌کند (فقط در لحظه کراس)
        data['Position'] = data['Signal'].diff()
        
        return data.dropna()

    def execute_trade(self, row: pd.Series, index: int, data: pd.DataFrame):
        """
        اجرای منطق معاملات شامل ورود، خروج، Stop Loss و Take Profit.
        """
        current_price = row['Close']
        
        # --- 1. مدیریت موقعیت باز (SL/TP) ---
        if self.position != 0:
            trade_status = "OPEN"
            
            # بررسی Stop Loss
            if self.position == 1 and current_price <= self.stop_loss:
                trade_status = "SL_HIT"
            elif self.position == -1 and current_price >= self.stop_loss:
                trade_status = "SL_HIT"
            
            # بررسی Take Profit
            elif self.position == 1 and current_price >= self.take_profit:
                trade_status = "TP_HIT"
            elif self.position == -1 and current_price <= self.take_profit:
                trade_status = "TP_HIT"
                
            if trade_status != "OPEN":
                # محاسبه سود/زیان
                pnl = (current_price - self.entry_price) * self.position * self.trade_size
                self.capital += pnl
                self.equity_curve.append(self.capital)
                
                # ثبت معامله
                self.trades.append({
                    "id": self.trade_id_counter,
                    "entry_time": str(self.trades[-1]['entry_time']),
                    "exit_time": str(row['Timestamp']),
                    "type": "LONG" if self.position == 1 else "SHORT",
                    "entry_price": self.entry_price,
                    "exit_price": current_price,
                    "pnl": round(pnl, 2),
                    "status": trade_status,
                    "capital_after": round(self.capital, 2)
                })
                self.position = 0
                self.trade_id_counter += 1
                
        # --- 2. ورود به موقعیت جدید ---
        
        # سیگنال خرید (ورود به لانگ)
        if row['Position'] == 1 and self.position == 0:
            self.position = 1
            self.entry_price = current_price
            
            # محاسبه اندازه معامله (بر اساس ریسک ثابت)
            # فرض می‌کنیم 1% از سرمایه را ریسک می‌کنیم و SL 0.001 است.
            stop_loss_level = current_price * 0.999
            risk_amount = self.capital * self.risk_per_trade
            self.stop_loss = stop_loss_level
            
            # محاسبه اندازه لات (ساده شده)
            price_diff_sl = abs(current_price - self.stop_loss)
            if price_diff_sl == 0: price_diff_sl = 1e-5 # جلوگیری از تقسیم بر صفر
            self.trade_size = risk_amount / price_diff_sl
            
            # تنظیم SL و TP
            self.stop_loss = current_price * 0.999 # 0.1% SL
            self.take_profit = current_price * 1.002 # 0.2% TP (نسبت ریسک به ریوارد 1:2)
            
            self.trades.append({
                "id": self.trade_id_counter,
                "entry_time": str(row['Timestamp']),
                "type": "LONG",
                "entry_price": self.entry_price,
                "stop_loss": round(self.stop_loss, 5),
                "take_profit": round(self.take_profit, 5),
                "trade_size": round(self.trade_size, 2),
                "status": "OPEN"
            })

        # سیگنال فروش (ورود به شورت)
        elif row['Position'] == -1 and self.position == 0:
            self.position = -1
            self.entry_price = current_price
            
            # محاسبه اندازه معامله
            stop_loss_level = current_price * 1.001
            risk_amount = self.capital * self.risk_per_trade
            self.stop_loss = stop_loss_level
            
            price_diff_sl = abs(current_price - self.stop_loss)
            if price_diff_sl == 0: price_diff_sl = 1e-5
            self.trade_size = risk_amount / price_diff_sl
            
            # تنظیم SL و TP
            self.stop_loss = current_price * 1.001 # 0.1% SL
            self.take_profit = current_price * 0.998 # 0.2% TP (نسبت ریسک به ریوارد 1:2)
            
            self.trades.append({
                "id": self.trade_id_counter,
                "entry_time": str(row['Timestamp']),
                "type": "SHORT",
                "entry_price": self.entry_price,
                "stop_loss": round(self.stop_loss, 5),
                "take_profit": round(self.take_profit, 5),
                "trade_size": round(self.trade_size, 2),
                "status": "OPEN"
            })
            
        # در صورت باز بودن موقعیت، SL/TP را با قیمت فعلی چک می‌کنیم
        elif self.position != 0:
            # اگر موقعیت باز است، فقط SL/TP را در هر کندل چک می‌کنیم
            pass
            
        # در صورت بسته بودن موقعیت و عدم وجود سیگنال جدید، کاری نمی‌کنیم
        else:
            pass
            
        # ثبت وضعیت سرمایه در هر گام (برای رسم Equity Curve)
        if not self.equity_curve or self.equity_curve[-1] != self.capital:
            self.equity_curve.append(self.capital)


# --- 2. Backtesting Module ---

def backtest_strategy(data: pd.DataFrame, bot: ForexTradingBot) -> dict:
    """
    اجرای بک‌تست روی داده‌های تاریخی.
    """
    print("--- شروع بک‌تست استراتژی SMA Cross ---")
    
    # تولید سیگنال‌ها
    data = bot.generate_signals(data)
    
    # اجرای معاملات
    for index, row in data.iterrows():
        bot.execute_trade(row, index, data)
        
    # بستن موقعیت باز نهایی در صورت وجود
    if bot.position != 0:
        final_pnl = (data.iloc[-1]['Close'] - bot.entry_price) * bot.position * bot.trade_size
        bot.capital += final_pnl
        bot.equity_curve.append(bot.capital)
        bot.trades.append({
            "id": bot.trade_id_counter,
            "entry_time": bot.trades[-1]['entry_time'],
            "exit_time": str(data.iloc[-1]['Timestamp']),
            "type": "LONG" if bot.position == 1 else "SHORT",
            "entry_price": bot.entry_price,
            "exit_price": data.iloc[-1]['Close'],
            "pnl": round(final_pnl, 2),
            "status": "CLOSED_END",
            "capital_after": round(bot.capital, 2)
        })
        bot.position = 0
        
    print("--- بک‌تست با موفقیت به پایان رسید ---")
    
    # ساخت گزارش نهایی
    report = {
        "initial_capital": bot.equity_curve[0],
        "final_capital": bot.capital,
        "total_pnl": bot.capital - bot.equity_curve[0],
        "trades_count": len([t for t in bot.trades if t.get('status') != 'OPEN']),
        "trades_log": bot.trades,
        "equity_curve": bot.equity_curve
    }
    return report

# --- 3. Dashboard and Reporting ---

def generate_dashboard(report: dict):
    """
    ایجاد داشبورد ساده برای نمایش سود/زیان و آمار کلیدی.
    """
    print("\n==================================================")
    print("📊 داشبورد نتایج بک‌تست (EUR/USD - 1m SMA Cross)")
    print("==================================================")
    
    initial_cap = report['initial_capital']
    final_cap = report['final_capital']
    total_pnl = report['total_pnl']
    
    # محاسبه آمار معاملات
    closed_trades = [t for t in report['trades_log'] if t.get('status') != 'OPEN']
    winning_trades = [t for t in closed_trades if t['pnl'] > 0]
    losing_trades = [t for t in closed_trades if t['pnl'] <= 0]
    
    win_rate = len(winning_trades) / len(closed_trades) if closed_trades else 0
    
    print(f"سرمایه اولیه: {initial_cap:,.2f} $")
    print(f"سرمایه نهایی: {final_cap:,.2f} $")
    print(f"سود/زیان کل: {total_pnl:,.2f} $ ({total_pnl / initial_cap * 100:.2f}%)")
    print("-" * 40)
    print(f"تعداد کل معاملات: {len(closed_trades)}")
    print(f"معاملات برنده: {len(winning_trades)}")
    print(f"معاملات بازنده: {len(losing_trades)}")
    print(f"نرخ برد (Win Rate): {win_rate:.2%}")
    print("==================================================")
    
    # ذخیره لاگ معاملات در JSON
    with open("trade_log.json", "w", encoding="utf-8") as f:
        json.dump(report['trades_log'], f, indent=4, ensure_ascii=False)
    
    print("\n✅ لاگ کامل معاملات در trade_log.json ذخیره شد.")
    print("✅ منحنی سرمایه (Equity Curve) در گزارش نهایی موجود است.")


# --- 4. Placeholder for Data Loading (3 Months of 1-Minute Data) ---

def load_simulated_data(symbol="EURUSD", timeframe="1m", months=3) -> pd.DataFrame:
    """
    تابع Placeholder برای بارگذاری داده‌های تاریخی (شبیه‌سازی شده).
    در یک سناریوی واقعی، این داده‌ها از Binance API یا یک دیتابیس دانلود می‌شوند.
    """
    print(f"--- بارگذاری داده‌های شبیه‌سازی شده ({symbol}, {timeframe}, {months} ماه) ---")
    
    # شبیه‌سازی 3 ماه داده 1 دقیقه‌ای (تقریباً 129,600 کندل)
    num_candles = 1000 # برای اجرای سریع بک‌تست، تعداد را کم می‌کنیم
    
    # ایجاد Timestamp
    start_time = datetime(2025, 1, 1)
    timestamps = pd.to_datetime([start_time + pd.Timedelta(minutes=i) for i in range(num_candles)])
    
    # شبیه‌سازی قیمت (حرکت تصادفی با یک روند ملایم)
    np.random.seed(42)
    base_price = 1.0700
    price_changes = np.random.normal(0, 0.0001, num_candles).cumsum()
    close_prices = base_price + price_changes
    
    # ایجاد داده‌های OHLCV
    data = pd.DataFrame({
        'Timestamp': timestamps,
        'Open': close_prices - np.random.uniform(0.00005, 0.0001, num_candles),
        'High': close_prices + np.random.uniform(0.00005, 0.0001, num_candles),
        'Low': close_prices - np.random.uniform(0.0001, 0.0002, num_candles),
        'Close': close_prices,
        'Volume': np.random.randint(100, 1000, num_candles)
    })
    
    print(f"✅ {len(data)} کندل شبیه‌سازی شده بارگذاری شد.")
    return data

# --- 5. Main Execution ---

if __name__ == "__main__":
    # 1. بارگذاری داده‌های شبیه‌سازی شده
    historical_data = load_simulated_data()
    
    # 2. ایجاد ربات معاملاتی
    bot = ForexTradingBot(short_window=10, long_window=30)
    
    # 3. اجرای بک‌تست
    backtest_report = backtest_strategy(historical_data, bot)
    
    # 4. نمایش داشبورد
    generate_dashboard(backtest_report)
    
    # 5. Placeholder برای اتصال به Binance API (برای اجرای زنده)
    print("\n--- اتصال به Binance API (Placeholder) ---")
    print("برای اجرای زنده، باید از یک کتابخانه مانند python-binance برای دریافت داده‌های لحظه‌ای و ارسال دستورات استفاده شود.")
    print("این اسکریپت در حال حاضر فقط بک‌تست را انجام می‌دهد.")
