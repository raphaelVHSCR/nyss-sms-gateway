# Script Instructions for Rasperry PI setup with Huawei UMTS Stick

> The object is to setup the the umts stick in a way that if there is LAN/Wifi internet available it will take precedence over the internet provided by the LTE stick

1. Install **usb-modeswitch**. This switches the huawei stick in the correct mode
2. Install ifmetric to change the metric of the eth1 interface
```shell
sudo apt install usb-modeswitch
sudo apt install ifmetric
sudo ifmetric eth1 500
```
3. Change the DNS server because huawei overwrites the "correct" settings. Change the file /etc/resolv.conf. This is often necessary.

Write a script that does this on startup

