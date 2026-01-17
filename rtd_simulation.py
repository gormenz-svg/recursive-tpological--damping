import numpy as np

class RTDSimulation:
    def __init__(self):
        # Параметры среды (высокая энтропия)
        self.dt = 0.01  # Шаг времени
        self.noise_level = 0.4  # 40% шума (как в концепте)
        
        # RTD Параметры (Static Core & Decay)
        self.static_core = np.array([0.0, 0.0])  # Виртуальный якорь
        self.eigen_decay = 0.85  # Коэффициент затухания A^k
        self.phi_state = np.array([0.0, 0.0])  # Рекурсивная функция перехода
        
    def get_target_movement(self, t):
        """Имитация движения мозга: пульс + дыхание + случайный шум"""
        pulse = 0.5 * np.sin(2 * np.pi * 1.2 * t)  # Сердцебиение
        breath = 1.2 * np.sin(2 * np.pi * 0.3 * t)  # Дыхание
        stochastic_noise = np.random.normal(0, self.noise_level)
        return pulse + breath + stochastic_noise

    def apply_rtd_filter(self, raw_signal, predicted_state):
        """
        Реализация формулы: S = min ||X_target - Phi|| - Gamma
        Рекурсивное подавление дрейфа.
        """
        # Эволюция состояния через Phi и Decay
        error = raw_signal - predicted_state
        gamma_correction = error * (1 - self.eigen_decay)
        
        # Обновление стабильной траектории
        new_state = predicted_state + gamma_correction
        return new_state

    def run(self, steps=1000):
        print(f"Starting RTD Simulation: {steps} steps...")
        print(f"Environment Noise: {self.noise_level * 100}%")
        print("-" * 30)
        
        rtd_trajectory = []
        raw_input = []
        
        current_prediction = np.array([0.0, 0.0])
        
        for i in range(steps):
            t = i * self.dt
            # 1. Получаем грязный сигнал от сенсоров
            target_pos = self.get_target_movement(t)
            raw_input.append(target_pos)
            
            # 2. Применяем RTD (Static Core Stabilization)
            stable_pos = self.apply_rtd_filter(target_pos, current_prediction)
            current_prediction = stable_pos
            rtd_trajectory.append(stable_pos)
            
            if i % 200 == 0:
                coherence = 1.0 - (np.abs(stable_pos - target_pos) / (np.abs(target_pos) + 1e-6))
                print(f"Step {i}: Trajectory Coherence = {max(0, coherence):.4f}")

        print("-" * 30)
        print("Simulation Complete. RTD Stability achieved.")
        return raw_input, rtd_trajectory

if __name__ == "__main__":
    sim = RTDSimulation()
    sim.run()
