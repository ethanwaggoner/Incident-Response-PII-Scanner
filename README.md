# Overview

Let’s say you get an alert that a client’s PC is infected by malware and is sending command and control traffic to a suspicious IP address. After isolating the affected PC, one of your first questions should be: Was any sensitive data compromised? One step in this process is to check if the PC contained PII. The stolen PII could be used in identity theft, and it is important if not required to notify any of the effected people. 

This scanner is an application designed to search for Personally Identifiable Information (PII) within various file types in a specified directory. The application allows users to customize the scanning configurations, add custom search patterns, and view the results.

## Features

    - Scan a chosen directory for PII
    - Configure scan settings
    - Add custom search patterns
    - View scan results
    - Export results


## Usage

    - Choose the directory you want to scan for PII
    - Select the desired file types and PII types to include in the scan
    - (Optional) Add custom search patterns using regex
    - Click "Run Scan" and wait for the scan to complete
    - Review the results in the "Results" section
## Installation

``` pip install -r requirements.txt ```
    
## Screenshots

![image](![image](https://user-images.githubusercontent.com/74027222/232165892-4bdcd91a-1224-45a7-8d11-e7d7c3a94c74.png)


## Authors

- [@ethanwaggoner](https://www.github.com/ethanwaggoner)
