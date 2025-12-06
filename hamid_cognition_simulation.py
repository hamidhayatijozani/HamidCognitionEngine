import math

class HamidCognition:
    """
    A simulation of the HamidCognition Engine based on the provided documentation.
    The core logic (state transition, phase determination, and energy calculation)
    is inferred from the variable meanings and the structure of the user's previous code snippet.
    """
    
    def __init__(self, P_initial, S_initial, T_initial):
        self.P = P_initial
        self.S = S_initial
        self.T = T_initial
        
        # Thresholds for phase determination (inferred)
        self.P_THRESHOLD = 1.5
        self.S_THRESHOLD = 1.5
        self.T_THRESHOLD = 0.3
        
    def hamid_step_absolute(self, pressure, novelty, freedom=3.0):
        """
        Simulates the state transition (P, S, T) based on external parameters.
        Logic is inferred from the user's previous code structure.
        """
        self.P = self.P * pressure
        self.S = self.S * novelty
        self.T = self.T / freedom
        
        # Ensure P, S, T remain non-negative and T is capped for stability
        self.P = max(0.0, self.P)
        self.S = max(0.0, self.S)
        self.T = min(1.0, max(0.0, self.T)) # T is often a normalized value (0 to 1)
        
        return self.P, self.S, self.T

    def calculate_energy(self):
        """
        Calculates the Cognitive Energy using the formula from the user's previous code.
        energy = (P * S) / (1.1 - T) * (1 - (T / (P + S + 1e-9)))
        """
        # Use a small epsilon to prevent division by zero in the denominator of the second term
        epsilon = 1e-9 
        
        # First term: (P * S) / (1.1 - T)
        term1 = (self.P * self.S) / (1.1 - self.T)
        
        # Second term: (1 - (T / (P + S + epsilon)))
        term2 = (1 - (self.T / (self.P + self.S + epsilon)))
        
        energy = term1 * term2
        return energy

    def analyze_state(self):
        """
        Analyzes the current (P, S, T) state to determine the cognitive phase and 
        predict the next cognitive output type. Logic is inferred from the meaning
        of P (Focus), S (Novelty), and T (Structure).
        """
        high_P = self.P > self.P_THRESHOLD
        high_S = self.S > self.S_THRESHOLD
        high_T = self.T > self.T_THRESHOLD
        
        phase = "Undefined"
        next_output = "Undefined"
        
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
        else:
            phase = "Transition (انتقال)"
            next_output = "State Check (بررسی وضعیت)"
            
        return phase, next_output

# --- Simulation Execution ---

# 1. Initial values (from the user's previous code snippet)
P_initial = 1.8235
S_initial = 2.1492
T_initial = 0.5361

# 2. Input parameters for the simulation
pressure_input = 0.8
novelty_input = 0.7
freedom_assumed = 3.0 # Assumed from the user's previous code

# 3. Initialize and run the simulation
engine = HamidCognition(P_initial, S_initial, T_initial)
P_new, S_new, T_new = engine.hamid_step_absolute(pressure=pressure_input, novelty=novelty_input, freedom=freedom_assumed)
energy = engine.calculate_energy()
phase, next_output = engine.analyze_state()

# 4. Print results in the requested format
print(f"P_initial = {P_initial:.4f}, S_initial = {S_initial:.4f}, T_initial = {T_initial:.4f}")
print(f"pressure = {pressure_input}, novelty = {novelty_input}, freedom = {freedom_assumed}")
print("-" * 30)
print(f"مقادیر محاسبه‌شده P,S,T جدید: P={P_new:.4f}, S={S_new:.4f}, T={T_new:.4f}")
print(f"تشخیص فاز: {phase}")
print(f"پیش‌بینی نوع پرسش/ایده بعدی: {next_output}")
print(f"سطح انرژی شناختی: {energy:.4f}")
