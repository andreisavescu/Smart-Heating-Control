# Smart Heating Monitor

A monitoring-only fork of [Smart Heating Control](https://github.com/sandreialexandru/Smart-Heating-Control) for Home Assistant.

It retains the upstream room model, thermal learning, schedules, weather awareness, diagnostics, sensors and Lovelace card, while treating existing heating devices as **read-only inputs**.

## Safety boundary

This integration is for observation and analysis only.

- Reads configured relay/switch states to determine room heat demand.
- Reads thermostat and temperature sensor states.
- Calculates room demand, heating runtime, thermal behaviour and schedule decisions.
- **Never** turns relays or switches on or off.
- **Never** changes climate modes or target temperatures.
- **Never** starts, stops or adjusts the boiler.
- **Never** writes TRV calibration values.

For room-demand inputs, **availability is the signal**: any valid state (including `on` or `off`) means demand; `unknown` or `unavailable` means no demand. The original configuration options and entities are retained for compatibility with the upstream architecture. Options that would cause device control are informational only in this fork. Do not install this alongside the original integration using the same `advanced_climate` domain.

## Install with HACS

1. In Home Assistant, open **HACS → Integrations → ⋮ → Custom repositories**.
2. Add `https://github.com/andreisavescu/Smart-Heating-Control` and select **Integration**.
3. Install **Smart Heating Monitor** and restart Home Assistant.
4. Add **Smart Heating Monitor** from **Settings → Devices & services → Add integration**.

This is a custom repository until a tagged release is published.

## Upstream

Based on Smart Heating Control by [sandreialexandru](https://github.com/sandreialexandru). The upstream project is licensed under the MIT License; its license and copyright notices are retained in this fork.

