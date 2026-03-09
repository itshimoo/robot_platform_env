#!/usr/bin/env bash
# Runs automatically on every `pixi run` or `pixi shell`
set -e

export RMW_IMPLEMENTATION="${RMW_IMPLEMENTATION:-rmw_zenoh_cpp}"
export ZENOH_CONFIG_OVERRIDE="transport/shared_memory/enabled=false"

# Connect to running sim container's Zenoh router
# Override by setting AIC_ROUTER_ADDR or R1_ROUTER_ADDR in ~/.r1rc
R1_ROUTER="${R1_ROUTER_ADDR:-localhost:7447}"
export ZENOH_CONFIG_OVERRIDE="${ZENOH_CONFIG_OVERRIDE};connect/endpoints=[\"tcp/${R1_ROUTER}\"]"
