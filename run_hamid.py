import json
import time
import random
from datetime import datetime

# --- 1. HamidCognition Engine Class (Embedded for Self-Contained Script) ---

class HamidCognition:
    """
    موتور شناختی HamidCognition Engine (نسخه سبک برای Termux)
    P: نفوذ، S: اتصال خلاق، T: تثبیت سبک
    """
    
    P_THRESHOLD = 1.5
    S_THRESHOLD = 1.5
    T_THRESHOLD = 0.3
    
    def __init__(self, P_initial: float, S_initial: float, T_initial: float):
        self.P = P_initial
        self.S = S_initial
        self.T = T_initial
        
    def hamid_step_absolute(self, pressure: float, novelty: float, freedom: float = 3.0) -> tuple[float, float, float]:
        """ منطق انتقال وضعیت """
        self.P = self.P * pressure
        self.S = self.S * novelty
        self.T = self.T / freedom
        
        self.P = max(0.0, self.P)
        self.S = max(0.0, self.S)
        self.T = min(1.0, max(0.0, self.T))
        
        return self.P, self.S, self.T

    def calculate_energy(self) -> float:
        """ محاسبه انرژی شناختی """
        epsilon = 1e-9 
        term1 = (self.P * self.S) / (1.1 - self.T)
        term2 = (1 - (self.T / (self.P + self.S + epsilon)))
        energy = term1 * term2
        return energy

    def analyze_state(self) -> tuple[str, str]:
        """ تحلیل وضعیت و تعیین فاز """
        high_P = self.P > self.P_THRESHOLD
        high_S = self.S > self.S_THRESHOLD
        high_T = self.T > self.T_THRESHOLD
        
        phase = "Transition (انتقال)"
        next_output = "State Check (بررسی وضعیت)"
        
        if high_P and high_S and not high_T:
            phase = "Synthesis (ترکیب)"
            next_output = "Refinement/Application (پالایش/کاربرد)"
        elif high_P and not high_S and high_T:
            phase = "Stabilization (تثبیت)"
            next_output = "Execution/Optimization (اجرا/بهینه‌سازی)"
        elif not high_P and high_S and not high_T:
            phase = "Rupture/Exploration (گسست/کاوش)"
            next_output = "New Input/Direction (ورودی/جهت‌گیری جدید)"
        elif not high_P and not high_S and high_T:
            phase = "Stagnation/Review (رکود/بازبینی)"
            next_output = "Challenge/Disruption (چالش/اخلال)"
        elif high_P and high_S and high_T:
            phase = "Overload/Rigid Synthesis (بارگذاری بیش از حد/ترکیب سخت)"
            next_output = "Simplification/Prioritization (ساده‌سازی/اولویت‌بندی)"
        elif not high_P and not high_S and not high_T:
            phase = "Dormancy/Reset (خواب/بازنشانی)"
            next_output = "Fundamental Inquiry (پرسش بنیادی)"
        
        return phase, next_output

# --- 2. شبیه‌سازی و تولید JSON ---

def simulate_and_generate_json(steps: int = 10, output_filename: str = "hamid_cognition_history.json"):
    """
    اجرای شبیه‌سازی موتور شناختی و ذخیره تاریخچه در قالب JSON.
    """
    
    # مقادیر اولیه
    P_initial, S_initial, T_initial = 1.8235, 2.1492, 0.5361
    engine = HamidCognition(P_initial, S_initial, T_initial)
    
    history = []
    
    print(f"--- شروع شبیه‌سازی {steps} مرحله‌ای روی Termux ---")
    
    for i in range(steps):
        # شبیه‌سازی داده‌های ورودی (pressure, novelty, freedom)
        # در یک سناریوی واقعی، این مقادیر از یک فایل CSV یا API خوانده می‌شوند.
        pressure = random.uniform(0.7, 1.1)
        novelty = random.uniform(0.6, 1.2)
        freedom = random.uniform(2.5, 3.5)
        
        # اجرای گام شناختی
        P_new, S_new, T_new = engine.hamid_step_absolute(pressure, novelty, freedom)
        energy = engine.calculate_energy()
        phase, next_output = engine.analyze_state()
        
        # ثبت وضعیت
        step_data = {
            "step": i + 1,
            "timestamp": datetime.now().isoformat(),
            "input_params": {"pressure": pressure, "novelty": novelty, "freedom": freedom},
            "P": round(P_new, 4),
            "S": round(S_new, 4),
            "T": round(T_new, 4),
            "energy": round(energy, 4),
            "phase": phase,
            "next_output": next_output
        }
        history.append(step_data)
        
        print(f"مرحله {i+1}: P={P_new:.4f}, S={S_new:.4f}, T={T_new:.4f}, فاز: {phase}")
        time.sleep(0.1) # تأخیر کوچک برای شبیه‌سازی زمان پردازش
        
    # ساختار نهایی JSON
    final_json = {
        "metadata": {
            "engine_version": "HamidLite_Termux_v1.0",
            "start_time": history[0]["timestamp"],
            "end_time": history[-1]["timestamp"],
            "initial_state": {"P": P_initial, "S": S_initial, "T": T_initial}
        },
        "history": history
    }
    
    # ذخیره JSON
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ تاریخچه شناختی با موفقیت در فایل '{output_filename}' ذخیره شد.")
    return output_filename

# --- 3. تابع Placeholder برای انتقال به محیط پردازش سنگین ---

def transfer_to_cloud(json_file_path: str):
    """
    تابع Placeholder برای انتقال فایل JSON به Google Colab یا VPS.
    در Termux، می‌توان از ابزارهایی مانند `curl`، `scp` یا `rclone` استفاده کرد.
    """
    print("\n--- اتصال به محیط پردازش سنگین (اختیاری) ---")
    print(f"فایل آماده انتقال: {json_file_path}")
    
    # در اینجا منطق انتقال واقعی قرار می‌گیرد. مثال:
    # 1. انتقال به سرور VPS با SCP (نیاز به نصب openssh در Termux):
    # os.system(f"scp {json_file_path} user@your_vps_ip:/path/to/upload/")
    
    # 2. انتقال به Google Drive برای استفاده در Colab (نیاز به نصب rclone در Termux):
    # os.system(f"rclone copy {json_file_path} gdrive:HamidCognitionData/")
    
    print("💡 منطق انتقال به ابر در حال حاضر یک Placeholder است.")
    print("پس از انتقال، پردازش سنگین (مانند backtest کامل) روی سرور انجام می‌شود.")
    print("خروجی نهایی باید به صورت معکوس به Termux منتقل شود.")
    print("--- پایان Placeholder ---")


# --- 4. اجرای اصلی ---

if __name__ == "__main__":
    # 1. اجرای موتور سبک و تولید JSON
    output_file = simulate_and_generate_json(steps=20)
    
    # 2. اتصال به محیط پردازش سنگین (اختیاری)
    transfer_to_cloud(output_file)
    
    print("\n--- چرخه عملیاتی Termux تکمیل شد ---")
    print("برای اجرای واقعی انتقال به ابر، دستورات `curl` یا `scp` را در تابع `transfer_to_cloud` جایگزین کنید.")
