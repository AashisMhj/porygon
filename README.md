# Porygon

This is python script to perform load testing on a api server. Written in python that perform continuous request to a server. The script then write the metrics related to response such as response time taken and other things on a csv file.

Using kubernetes deployment controller and cron jobs we perform gradual step load testing. 
For on more detail how the flow please read this [documentation](./dev-files/incremental-flow.md).

This script for written specifically to perform load thing on [servers](./dev-files/performance-server.md) i created but you can modify the urls.py to add your urls