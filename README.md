# Swtch EV Charger for Home Assistant

A HACS custom integration for Swtch / Joint Tech EVL007 chargers using the charger's local API.

## Features

- UI config flow asks for:
  - IP address
  - Scan interval (seconds)
  - Timeout (seconds)
- Polls `http://<charger-ip>/api/GetChargingStationInfo`
- Creates sensors for:
  - Status
  - CP Status
  - Voltage
  - Current
  - Power
  - Meter Raw
  - Firmware
  - Mode
- Creates binary sensors for:
  - Online
  - Occupied
  - Connected
  - Active

## Installation with HACS

1. Create a new GitHub repository.
2. Upload the contents of this zip to the repository root.
3. In Home Assistant, open HACS.
4. Go to **Integrations**.
5. Open the menu in the top right and choose **Custom repositories**.
6. Add your GitHub repository URL as type **Integration**.
7. Install **Swtch EV Charger** from HACS.
8. Restart Home Assistant.
9. Go to **Settings -> Devices & Services -> Add Integration**.
10. Search for **Swtch EV Charger**.
11. Enter the charger IP address, scan interval, and timeout.

## Notes

- The charger JSON appears to use the key `availablity` instead of `availability`, so this integration uses the device's actual field name.
- If future firmware requires bearer token authentication, extend `api.py`.
- Scan interval and timeout can be changed later from the integration options.
