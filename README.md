# Galaxy MeTTa Analysis

This project uses [PeTTa](https://github.com/patham9/PeTTa) for high-performance MeTTa execution.

## Setup

1. **Clone PeTTa** into the project root:
   ```bash
   git clone https://github.com/patham9/PeTTa
   ```
   **Note:** The `PeTTa` folder should be located in the root directory of this project (alongside `src`, `data`, etc.).

2. **Install Python Dependencies**:
   Ensure you have a virtual environment set up and active, then install the required packages (including `janus_swi` for PeTTa):
   ```bash
   pip install -r requirements.txt
   pip install janus_swi
   ```
   *(Note: You must have SWI-Prolog installed on your system for `janus_swi` to work.)*

## Usage

Run the final report generation script:
```bash
python src/python/final_report.py
```
