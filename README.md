# HamidCognitionEngine Simulation

> **Repository status:** Historical simulation lineage.
>
> The current canonical research and provenance record is **[HamidCognition-Unified](https://github.com/hamidhayatijozani/HamidCognition-Unified)**. This repository preserves an earlier inferred simulation of P/S/T transition logic and should be cited as a historical artifact.

## جایگاه پژوهشی

این repository برای بررسی منطق شبیه‌سازی و تاریخچهٔ مدل مفید است. عبارت `inferred` در این نسخه مهم است: منطق ثبت‌شده باید به‌عنوان implementation/simulation تاریخی خوانده شود، نه به‌عنوان اثبات تجربی مدل شناختی.

## Simulation Logic (Inferred)

The recorded transition function is:

- `P_new = P_old * pressure`
- `S_new = S_old * novelty`
- `T_new = T_old / freedom`

The recorded cognitive-energy expression is:

`energy = (P * S) / (1.1 - T) * (1 - (T / (P + S + 1e-9)))`

## Historical execution record

The original README records an example execution with initial state `P=1.8235, S=2.1492, T=0.5361`, parameters `pressure=0.8, novelty=0.7, freedom=3.0`, and resulting values. These are historical recorded outputs and should not be presented as an independently reproduced benchmark without a corresponding execution fingerprint.

## Citation

برای استناد به این artifact، نام `HamidCognitionEngine` و commit/path دقیق را ذکر کنید. برای وضعیت فعلی تحقیق و رابطهٔ lineage از `HamidCognition-Unified` استفاده کنید.

**Canonical research record:** https://github.com/hamidhayatijozani/HamidCognition-Unified

**Originator:** Hamid Hayati Jozani
