import json

# 기존 JSON 파일 읽기
with open('measurement_data/240805_164000combined.json', 'r') as file:
    data = json.load(file)

# 변환된 형식의 데이터 생성
beacon_data = {
    "gateways": []
}

for gatewayMac, beacons in data.items():
    gateway_entry = {
        "gatewayMac": gatewayMac,
        "beacons": []
    }
    for mac, info in beacons.items():
        beacon_entry = {
            "mac": mac,
            "earlyTimestamp": info["early_timestamp"],
            "lateTimestamp": info["late_timestamp"]
        }
        gateway_entry["beacons"].append(beacon_entry)
    beacon_data["gateways"].append(gateway_entry)

# 변환된 JSON 데이터 출력 (선택 사항)
print(json.dumps(beacon_data, indent=4))
