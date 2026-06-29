# home-assistant-automations

Automation blueprints for Home Assistant — motion that respects the room next door, circadian scenes, and “please don’t flood the basement.”

Installed here as a git submodule at `blueprints/automation/etokheim-automations/`.  
Script blueprints live in [home-assistant-scripts](https://github.com/etokheim/home-assistant-scripts).

**Tip:** For the motion-light family, set up **Neighbor extended motion status** first, then the lights automation.

---

## Neighbor extended motion status

Tracks motion in the room *and* the neighbor room, exposing a simple helper state (`Motion`, `Neighbor motion`, `Clear`, …) so your other automations know what is going on.

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Fneighbor_extended_motion_status.yaml)

---

## Neighbor extended motion lights

Classic version: turn lights on (or run actions) from motion here or next door, with timers and brightness-aware shutoff. Needs the motion status blueprint above.

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Fneighbor_extended_motion_lights.yaml)

---

## Neighbor extended motion activated lights V2.1

The upgraded motion-light blueprint: more configuration, clearer timers, illuminance thresholds, and the same “never stumble in the dark” goal — with fewer compromises.

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Fneighbor_extended_motion_lights_v2.yaml)

---

## Circadian rhythm lighting

Keeps your Scene Extrapolation scene on a loop so lighting follows the time of day — stops when you turn the room off or when modifiers say “not now.” Requires [Scene Extrapolation](https://github.com/etokheim/scene-extrapolation).

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Fcontinuously_activate_scene.yaml)

---

## Floor heating regulator

Predictive floor-heating control for regulators without their own sensor: nudges setpoints every few minutes using trend data so you hit target temp without overshooting.

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Ffloor_heating_regulator_automation.yaml)

---

## Fire detection

Smoke or heat climbing fast? Run your notifications, TTS, or shutdown actions when detectors say something is wrong.

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Ffire-detection.yaml)

> **Note:** The blueprint file in this repo may need YAML cleanup before import succeeds.

---

## Frost detection

House getting too cold? Fire your alerts when indoor temperatures drop below your threshold (with sensible exclusions you configure).

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Ffrost-detection.yaml)

---

## Leak detection

Water where it should not be? Parallel-friendly automation for leak sensors — notify, shut valves, flash lights: your call.

[![Add to Home Assistant](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fetokheim%2Fhome-assistant-automations%2Fblob%2Fmaster%2Fleak-detection.yaml)

---

## Easy updates for blueprints?

Every blueprint here includes a `source_url` pointing at this repo, so you can keep them fresh without manual copy-paste.

If you want one-click (or hands-off) updates from the UI, check out **[Blueprints Updater](https://github.com/luuquangvu/blueprints-updater)** by [luuquangvu](https://github.com/luuquangvu) — a really well-done HACS integration that tracks blueprint changes and updates them like any other Home Assistant update. I am not affiliated with the project; I just use it and think it is worth sharing.
