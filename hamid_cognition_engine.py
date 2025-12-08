import math

class HamidCognition:
    """
    موتور شناختی HamidCognition Engine
    طراحی شده برای شبیه‌سازی فرآیند تفکر و تصمیم‌گیری بر اساس سه متغیر اصلی:
    P (نفوذ): عمق‌یابی و تمرکز بر مسئله.
    S (اتصال خلاق): توانایی ایجاد ارتباطات جدید و نوآورانه.
    T (تثبیت سبک): تمایل به ساختاردهی و حفظ ثبات در روش کار.
    """
    
    # آستانه‌های پیش‌فرض برای تحلیل فاز (قابل تنظیم)
    P_THRESHOLD = 1.5
    S_THRESHOLD = 1.5
    T_THRESHOLD = 0.3
    
    def __init__(self, P_initial: float, S_initial: float, T_initial: float):
        """
        مقادیر اولیه P, S, T را تنظیم می‌کند.
        """
        self.P = P_initial
        self.S = S_initial
        self.T = T_initial
        
    def hamid_step_absolute(self, pressure: float, novelty: float, freedom: float = 3.0) -> tuple[float, float, float]:
        """
        شبیه‌سازی انتقال وضعیت (P, S, T) بر اساس پارامترهای خارجی.
        
        :param pressure: ضریب تأثیر بر P (نفوذ).
        :param novelty: ضریب تأثیر بر S (اتصال خلاق).
        :param freedom: ضریب تأثیر بر T (تثبیت سبک).
        :return: مقادیر جدید P, S, T.
        """
        
        # منطق انتقال وضعیت (بر اساس کد قبلی کاربر)
        self.P = self.P * pressure
        self.S = self.S * novelty
        self.T = self.T / freedom
        
        # اطمینان از محدوده‌های منطقی
        self.P = max(0.0, self.P)
        self.S = max(0.0, self.S)
        self.T = min(1.0, max(0.0, self.T)) # T به عنوان یک مقدار نرمالیزه شده (0 تا 1) در نظر گرفته می‌شود
        
        return self.P, self.S, self.T

    def calculate_energy(self) -> float:
        """
        محاسبه انرژی شناختی (Cognitive Energy) بر اساس فرمول ارائه شده.
        energy = (P * S) / (1.1 - T) * (1 - (T / (P + S + 1e-9)))
        
        :return: سطح انرژی شناختی.
        """
        epsilon = 1e-9 
        
        # ترم اول: (P * S) / (1.1 - T)
        term1 = (self.P * self.S) / (1.1 - self.T)
        
        # ترم دوم: (1 - (T / (P + S + epsilon)))
        term2 = (1 - (self.T / (self.P + self.S + epsilon)))
        
        energy = term1 * term2
        return energy

    def analyze_state(self) -> tuple[str, str]:
        """
        تحلیل وضعیت فعلی (P, S, T) برای تعیین فاز شناختی و پیش‌بینی خروجی بعدی.
        
        :return: تاپل شامل (فاز شناختی، پیش‌بینی نوع پرسش/ایده بعدی).
        """
        high_P = self.P > self.P_THRESHOLD
        high_S = self.S > self.S_THRESHOLD
        high_T = self.T > self.T_THRESHOLD
        
        phase = "Transition (انتقال)"
        next_output = "State Check (بررسی وضعیت)"
        
        # تعیین فازها (بر اساس تحلیل منطقی متغیرها)
        if high_P and high_S and not high_T:
            phase = "Synthesis (ترکیب)" # تمرکز و خلاقیت بالا، ساختار منعطف
            next_output = "Refinement/Application (پالایش/کاربرد)"
        elif high_P and not high_S and high_T:
            phase = "Stabilization (تثبیت)" # تمرکز بالا، خلاقیت پایین، ساختار سخت
            next_output = "Execution/Optimization (اجرا/بهینه‌سازی)"
        elif not high_P and high_S and not high_T:
            phase = "Rupture/Exploration (گسست/کاوش)" # تمرکز پایین، خلاقیت بالا، ساختار منعطف
            next_output = "New Input/Direction (ورودی/جهت‌گیری جدید)"
        elif not high_P and not high_S and high_T:
            phase = "Stagnation/Review (رکود/بازبینی)" # تمرکز پایین، خلاقیت پایین، ساختار سخت
            next_output = "Challenge/Disruption (چالش/اخلال)"
        elif high_P and high_S and high_T:
            phase = "Overload/Rigid Synthesis (بارگذاری بیش از حد/ترکیب سخت)" # همه چیز بالاست
            next_output = "Simplification/Prioritization (ساده‌سازی/اولویت‌بندی)"
        elif not high_P and not high_S and not high_T:
            phase = "Dormancy/Reset (خواب/بازنشانی)" # همه چیز پایین است
            next_output = "Fundamental Inquiry (پرسش بنیادی)"
        
        return phase, next_output

# --- مثال اجرا (بر اساس درخواست قبلی) ---
if __name__ == "__main__":
    P_initial = 1.8235
    S_initial = 2.1492
    T_initial = 0.5361
    
    pressure_input = 0.8
    novelty_input = 0.7
    freedom_assumed = 3.0

    engine = HamidCognition(P_initial, S_initial, T_initial)
    P_new, S_new, T_new = engine.hamid_step_absolute(pressure=pressure_input, novelty=novelty_input, freedom=freedom_assumed)
    energy = engine.calculate_energy()
    phase, next_output = engine.analyze_state()

    print("--- شبیه‌سازی موتور شناختی HamidCognition ---")
    print(f"وضعیت اولیه: P={P_initial:.4f}, S={S_initial:.4f}, T={T_initial:.4f}")
    print(f"پارامترهای ورودی: pressure={pressure_input}, novelty={novelty_input}, freedom={freedom_assumed}")
    print("-" * 40)
    print(f"مقادیر محاسبه‌شده P,S,T جدید: P={P_new:.4f}, S={S_new:.4f}, T={T_new:.4f}")
    print(f"تشخیص فاز: {phase}")
    print(f"پیش‌بینی نوع پرسش/ایده بعدی: {next_output}")
    print(f"سطح انرژی شناختی: {energy:.4f}")
